# Snap2Dish 📸🍽️

A modern web platform where users can upload photos of food and instantly identify dishes with AI-powered recipe generation.

## Features

- 📸 **Photo Upload**: Upload images of any food dish
- 🤖 **AI-Powered Recognition**: Uses GitHub Models API to identify dishes
- 📖 **Recipe Generation**: Get detailed ingredients and cooking instructions
- 🔐 **Google OAuth**: Secure social login with Google
- 💾 **Recipe Storage**: Save and manage your discovered recipes
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS
- 🗄️ **PostgreSQL Database**: Robust data storage with SQLAlchemy ORM
- ✅ **Unit Tests**: Comprehensive test coverage

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Google OAuth 2.0 (Flask-Login + Authlib)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **AI/ML**: GitHub Models API (GPT-4o Vision)
- **Testing**: pytest, pytest-flask

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Google OAuth credentials
- GitHub Personal Access Token (for Models API)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/1happybot/snap2dish.git
   cd snap2dish
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   createdb snap2dish
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost:5432/snap2dish
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   GITHUB_TOKEN=your-github-token
   ```

6. **Initialize the database**
   ```bash
   flask init-db
   ```

## Getting API Credentials

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://localhost:5000/auth/callback` (for development)
   - Your production URL + `/auth/callback`
6. Copy the Client ID and Client Secret to your `.env` file

### GitHub Token Setup

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token (classic)
3. Select scopes: `repo` (for accessing GitHub Models)
4. Copy the token to your `.env` file as `GITHUB_TOKEN`

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Running Tests

```bash
pytest test_app.py -v
```

For coverage report:
```bash
pytest test_app.py --cov=. --cov-report=html
```

## Usage

1. **Sign In**: Click "Sign in with Google" to authenticate
2. **Upload Photo**: Click "Choose Image" and select a food photo
3. **Get Recipe**: Click "Analyze & Get Recipe" to identify the dish
4. **View Details**: See the dish name, ingredients, and cooking instructions
5. **Manage Recipes**: Access all your saved recipes from "My Recipes"

## Project Structure

```
snap2dish/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── auth.py                # Authentication logic
├── services.py            # Image analysis service
├── config.py              # Configuration settings
├── test_app.py            # Unit tests
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── recipe.html
│   └── my_recipes.html
├── static/                # Static files
│   ├── css/
│   └── js/
└── uploads/               # Uploaded images storage
```

## API Endpoints

- `GET /` - Home page
- `POST /upload` - Upload and analyze image
- `GET /recipe/<id>` - View recipe details
- `GET /my-recipes` - View all user recipes
- `POST /delete/<id>` - Delete a recipe
- `GET /api/recipe/<id>` - Get recipe JSON
- `GET /auth/login` - Google OAuth login
- `GET /auth/callback` - OAuth callback
- `GET /auth/logout` - Logout

## Security Features

- CSRF protection
- Secure password hashing
- OAuth 2.0 authentication
- File upload validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on:

- Development setup
- Code style guidelines
- Testing requirements
- Pull request process
- Bug reporting and feature requests

Quick start:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- GitHub Models API for AI-powered image analysis
- Tailwind CSS for the beautiful UI
- Flask community for excellent documentation
- OpenAI for GPT-4o Vision model

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Made with ❤️ by the Snap2Dish team
