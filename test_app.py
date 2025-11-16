"""Unit tests for Snap2Dish application."""
import os
import pytest
import tempfile
from io import BytesIO
from PIL import Image
from app import app
from models import db, User, Recipe


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def authenticated_client(client):
    """Create an authenticated test client."""
    with app.app_context():
        user = User(
            email='test@example.com',
            name='Test User',
            google_id='test123'
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)
    
    return client


def create_test_image():
    """Create a test image for upload."""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io


class TestModels:
    """Test database models."""
    
    def test_user_creation(self, client):
        """Test creating a user."""
        with app.app_context():
            user = User(
                email='test@example.com',
                name='Test User',
                google_id='12345'
            )
            db.session.add(user)
            db.session.commit()
            
            retrieved_user = User.query.filter_by(email='test@example.com').first()
            assert retrieved_user is not None
            assert retrieved_user.email == 'test@example.com'
            assert retrieved_user.name == 'Test User'
    
    def test_recipe_creation(self, client):
        """Test creating a recipe."""
        with app.app_context():
            user = User(email='test@example.com', google_id='12345')
            db.session.add(user)
            db.session.commit()
            
            recipe = Recipe(
                user_id=user.id,
                dish_name='Pasta',
                ingredients='Pasta, Sauce',
                instructions='Cook pasta, add sauce',
                cuisine_type='Italian'
            )
            db.session.add(recipe)
            db.session.commit()
            
            retrieved_recipe = Recipe.query.filter_by(dish_name='Pasta').first()
            assert retrieved_recipe is not None
            assert retrieved_recipe.dish_name == 'Pasta'
            assert retrieved_recipe.user_id == user.id
    
    def test_recipe_to_dict(self, client):
        """Test recipe to_dict method."""
        with app.app_context():
            user = User(email='test@example.com', google_id='12345')
            db.session.add(user)
            db.session.commit()
            
            recipe = Recipe(
                user_id=user.id,
                dish_name='Pizza',
                ingredients='Flour, Cheese',
                instructions='Make dough, add toppings',
                cuisine_type='Italian'
            )
            db.session.add(recipe)
            db.session.commit()
            
            recipe_dict = recipe.to_dict()
            assert recipe_dict['dish_name'] == 'Pizza'
            assert 'id' in recipe_dict
            assert 'created_at' in recipe_dict


class TestRoutes:
    """Test application routes."""
    
    def test_index_not_authenticated(self, client):
        """Test index page for non-authenticated users."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Sign In to Get Started' in response.data
    
    def test_index_authenticated(self, authenticated_client):
        """Test index page for authenticated users."""
        response = authenticated_client.get('/')
        assert response.status_code == 200
        assert b'Upload Food Image' in response.data
    
    def test_upload_not_authenticated(self, client):
        """Test upload route requires authentication."""
        response = client.post('/upload', data={'file': (BytesIO(b'test'), 'test.png')})
        assert response.status_code == 302  # Redirect to login
    
    def test_upload_no_file(self, authenticated_client):
        """Test upload without file."""
        response = authenticated_client.post('/upload', data={}, follow_redirects=True)
        assert b'No file uploaded' in response.data
    
    def test_upload_valid_image(self, authenticated_client):
        """Test uploading a valid image."""
        img_io = create_test_image()
        data = {
            'file': (img_io, 'test.png')
        }
        response = authenticated_client.post('/upload', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        with app.app_context():
            recipes = Recipe.query.all()
            assert len(recipes) == 1
    
    def test_my_recipes_not_authenticated(self, client):
        """Test my recipes page requires authentication."""
        response = client.get('/my-recipes')
        assert response.status_code == 302  # Redirect to login
    
    def test_my_recipes_authenticated(self, authenticated_client):
        """Test my recipes page for authenticated users."""
        response = authenticated_client.get('/my-recipes')
        assert response.status_code == 200
        assert b'My Recipe Collection' in response.data
    
    def test_recipe_detail_not_authenticated(self, client):
        """Test recipe detail requires authentication."""
        response = client.get('/recipe/1')
        assert response.status_code == 302  # Redirect to login
    
    def test_recipe_detail_authenticated(self, authenticated_client):
        """Test recipe detail page."""
        # Create a recipe
        with app.app_context():
            user = User.query.first()
            recipe = Recipe(
                user_id=user.id,
                dish_name='Test Dish',
                ingredients='Test Ingredients',
                instructions='Test Instructions',
                cuisine_type='Test'
            )
            db.session.add(recipe)
            db.session.commit()
            recipe_id = recipe.id
        
        response = authenticated_client.get(f'/recipe/{recipe_id}')
        assert response.status_code == 200
        assert b'Test Dish' in response.data
    
    def test_delete_recipe(self, authenticated_client):
        """Test deleting a recipe."""
        # Create a recipe
        with app.app_context():
            user = User.query.first()
            recipe = Recipe(
                user_id=user.id,
                dish_name='To Delete',
                ingredients='Ingredients',
                instructions='Instructions',
                cuisine_type='Test'
            )
            db.session.add(recipe)
            db.session.commit()
            recipe_id = recipe.id
        
        response = authenticated_client.post(f'/delete/{recipe_id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Recipe deleted successfully' in response.data
        
        with app.app_context():
            deleted_recipe = Recipe.query.get(recipe_id)
            assert deleted_recipe is None
    
    def test_api_recipe(self, authenticated_client):
        """Test API endpoint for recipe details."""
        # Create a recipe
        with app.app_context():
            user = User.query.first()
            recipe = Recipe(
                user_id=user.id,
                dish_name='API Test Dish',
                ingredients='API Ingredients',
                instructions='API Instructions',
                cuisine_type='API'
            )
            db.session.add(recipe)
            db.session.commit()
            recipe_id = recipe.id
        
        response = authenticated_client.get(f'/api/recipe/{recipe_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['dish_name'] == 'API Test Dish'


class TestImageAnalysisService:
    """Test image analysis service."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from services import ImageAnalysisService
        service = ImageAnalysisService('test_token', 'test_endpoint')
        assert service.github_token == 'test_token'
        assert service.endpoint == 'test_endpoint'
    
    def test_mock_response(self):
        """Test mock response when no token is provided."""
        from services import ImageAnalysisService
        service = ImageAnalysisService(None, 'test_endpoint')
        
        # Create a temporary test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (100, 100), color='blue')
            img.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            result = service.analyze_food_image(tmp_path)
            assert 'dish_name' in result
            assert 'ingredients' in result
            assert 'instructions' in result
            assert 'cuisine_type' in result
        finally:
            os.unlink(tmp_path)


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_allowed_file(self):
        """Test allowed file function."""
        from app import allowed_file
        assert allowed_file('test.png') == True
        assert allowed_file('test.jpg') == True
        assert allowed_file('test.jpeg') == True
        assert allowed_file('test.gif') == True
        assert allowed_file('test.txt') == False
        assert allowed_file('test.pdf') == False
        assert allowed_file('test') == False
