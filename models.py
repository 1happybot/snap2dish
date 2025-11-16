"""Database models for Snap2Dish application."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    profile_pic = db.Column(db.String(200))
    google_id = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Recipe(db.Model):
    """Recipe model for storing identified dishes and recipes."""
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dish_name = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    image_path = db.Column(db.String(300))
    cuisine_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recipe {self.dish_name}>'
    
    def to_dict(self):
        """Convert recipe to dictionary."""
        return {
            'id': self.id,
            'dish_name': self.dish_name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'image_path': self.image_path,
            'cuisine_type': self.cuisine_type,
            'created_at': self.created_at.isoformat()
        }
