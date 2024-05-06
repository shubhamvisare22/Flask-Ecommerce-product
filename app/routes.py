from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, Product
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

# JWT settings
jwt = JWTManager(app)

# Pagination settings
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10


def validate_product_data(data):
    """Validate product data."""
    required_fields = ['title', 'description', 'price']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        elif not data[field]:
            return False, f"Empty value for field: {field}"
    return True, None


class ProductsAPI(MethodView):
    decorators = [jwt_required()]

    def get(self):
        page = request.args.get('page', DEFAULT_PAGE, type=int)
        per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)

        products = Product.query.paginate(page=page, per_page=per_page)

        product_list = [product.to_dict() for product in products.items]

        next_page_url = None
        if products.has_next:
            next_page_url = f"http://127.0.0.1:5000/products?page={products.next_num}"

        return jsonify({
            "total_pages": products.pages,
            "current_page": products.page,
            "total_items": products.total,
            "products": product_list,
            "next_page_url": next_page_url
        })

    def post(self):
        data = request.get_json()

        is_valid, error_msg = validate_product_data(data)
        if not is_valid:
            return jsonify({"status": False, "msg": error_msg}), 400

        try:
            new_product = Product(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                user_id=get_jwt_identity()  # Get user id from JWT token
            )

            db.session.add(new_product)
            db.session.commit()

            return jsonify(new_product.to_dict()), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"status": False, "msg": "Failed to create product. Title may already exist."}), 500

        except Exception as e:
            return jsonify({"status": False, "msg": f"An error occurred while creating the product: {str(e)}"}), 500


class ProductAPI(MethodView):
    decorators = [jwt_required()]

    def put(self, id):
        product = Product.query.filter_by(id=id, user_id=get_jwt_identity()).first()
        if not product:
            return jsonify({"status": False, "msg": "Product not found or unauthorized."}), 404

        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')

        if not any((title, description, price)):
            return jsonify({"status": False, "msg": "No data provided for update."}), 400

        try:
            if title:
                product.title = title
            if description:
                product.description = description
            if price:
                product.price = price

            db.session.commit()
            return jsonify(product.to_dict()), 200

        except Exception as e:
            return jsonify({"status": False, "msg": f"An error occurred while updating the product: {str(e)}"}), 500

    def delete(self, id):
        product = Product.query.filter_by(id=id, user_id=get_jwt_identity()).first()
        if not product:
            return jsonify({"status": False, "msg": "Product not found or unauthorized."}), 404

        try:
            db.session.delete(product)
            db.session.commit()
            return '', 204
        except Exception as e:
            return jsonify({"status": False, "msg": f"An error occurred while deleting the product: {str(e)}"}), 500


class UserAPI(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"status": False, "msg": "Missing username or password"}), 400

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"status": False, "msg": "Username already exists"}), 409

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": True, "msg": "User registered successfully"}), 201


class LoginAPI(MethodView):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"status": False, "msg": "Missing username or password"}), 400

        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return jsonify({"status": False, "msg": "Invalid username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200


app.add_url_rule('/products', view_func=ProductsAPI.as_view('products'))
app.add_url_rule('/products/<int:id>', view_func=ProductAPI.as_view('product'))
app.add_url_rule('/register', view_func=UserAPI.as_view('register'))
app.add_url_rule('/login', view_func=LoginAPI.as_view('login'))

if __name__ == '__main__':
    app.run(debug=True)
