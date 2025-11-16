"""Main Flask application for Snap2Dish."""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user
from werkzeug.utils import secure_filename
from config import config
from models import db, User, Recipe
from auth import auth_bp, init_oauth
from services import ImageAnalysisService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Initialize OAuth if configured
if app.config['GOOGLE_CLIENT_ID'] and app.config['GOOGLE_CLIENT_SECRET']:
    oauth, google = init_oauth(app)
    app.extensions['oauth'] = oauth
    app.extensions['google'] = google

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Initialize image analysis service
image_service = ImageAnalysisService(
    app.config['GITHUB_TOKEN'],
    app.config['GITHUB_MODEL_ENDPOINT']
)


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return User.query.get(int(user_id))


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render the home page."""
    recipes = []
    if current_user.is_authenticated:
        recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(
            Recipe.created_at.desc()
        ).limit(10).all()
    return render_template('index.html', recipes=recipes)


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    """Handle image upload and analysis."""
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(filepath)
        
        # Analyze the image
        analysis_result = image_service.analyze_food_image(filepath)
        
        # Save to database
        recipe = Recipe(
            user_id=current_user.id,
            dish_name=analysis_result['dish_name'],
            ingredients=analysis_result['ingredients'],
            instructions=analysis_result['instructions'],
            image_path=filename,
            cuisine_type=analysis_result['cuisine_type']
        )
        db.session.add(recipe)
        db.session.commit()
        
        flash(f'Successfully identified: {analysis_result["dish_name"]}', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
    
    flash('Invalid file type. Please upload an image.', 'error')
    return redirect(url_for('index'))


@app.route('/recipe/<int:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    """Display recipe details."""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user owns this recipe
    if recipe.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    return render_template('recipe.html', recipe=recipe)


@app.route('/my-recipes')
@login_required
def my_recipes():
    """Display all user's recipes."""
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(
        Recipe.created_at.desc()
    ).all()
    return render_template('my_recipes.html', recipes=recipes)


@app.route('/api/recipe/<int:recipe_id>')
@login_required
def api_recipe(recipe_id):
    """API endpoint for recipe details."""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(recipe.to_dict())


@app.route('/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    """Delete a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Delete the image file if it exists
    if recipe.image_path:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], recipe.image_path)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(recipe)
    db.session.commit()
    
    flash('Recipe deleted successfully', 'success')
    return redirect(url_for('my_recipes'))


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
