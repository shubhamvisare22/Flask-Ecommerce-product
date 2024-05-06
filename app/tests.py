import unittest
import json
from routes import app, db  # Import the Flask app and SQLAlchemy instance 'db'
from models import User, Product

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 201)

        # Check if user is added to the database
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)

    def test_login(self):
        data = {'username': 'testuser', 'password': 'password123'}
        self.app.post('/register', json=data)
        response = self.app.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_create_product(self):
        # Register a user
        user_data = {'username': 'testuser', 'password': 'password123'}
        self.app.post('/register', json=user_data)

        # Login to get access token
        login_data = {'username': 'testuser', 'password': 'password123'}
        login_response = self.app.post('/login', json=login_data)
        access_token = json.loads(login_response.data)['access_token']

        # Create a product with the access token
        product_data = {'title': 'Test Product', 'description': 'Test Description', 'price': 10.0}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.post('/products', json=product_data, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_get_all_products(self):
        # Register a user
        user_data = {'username': 'testuser', 'password': 'password123'}
        self.app.post('/register', json=user_data)

        # Login to get access token
        login_data = {'username': 'testuser', 'password': 'password123'}
        login_response = self.app.post('/login', json=login_data)
        access_token = json.loads(login_response.data)['access_token']

        # Create a product with the access token
        product_data = {'title': 'Test Product', 'description': 'Test Description', 'price': 10.0}
        headers = {'Authorization': f'Bearer {access_token}'}
        self.app.post('/products', json=product_data, headers=headers)

        # Get all products
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', json.loads(response.data))

    def test_update_product(self):
        # Register a user
        user_data = {'username': 'testuser', 'password': 'password123'}
        self.app.post('/register', json=user_data)

        # Login to get access token
        login_data = {'username': 'testuser', 'password': 'password123'}
        login_response = self.app.post('/login', json=login_data)
        access_token = json.loads(login_response.data)['access_token']

        # Create a product with the access token
        product_data = {'title': 'Test Product', 'description': 'Test Description', 'price': 10.0}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.post('/products', json=product_data, headers=headers)
        product_id = json.loads(response.data)['id']

        # Update the product
        updated_data = {'title': 'Updated Product', 'description': 'Updated Description', 'price': 20.0}
        response = self.app.put(f'/products/{product_id}', json=updated_data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        # Register a user
        user_data = {'username': 'testuser', 'password': 'password123'}
        self.app.post('/register', json=user_data)

        # Login to get access token
        login_data = {'username': 'testuser', 'password': 'password123'}
        login_response = self.app.post('/login', json=login_data)
        access_token = json.loads(login_response.data)['access_token']

        # Create a product with the access token
        product_data = {'title': 'Test Product', 'description': 'Test Description', 'price': 10.0}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.post('/products', json=product_data, headers=headers)
        product_id = json.loads(response.data)['id']

        # Delete the product
        response = self.app.delete(f'/products/{product_id}', headers=headers)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
