# Contributing to Snap2Dish 🤝

Thank you for your interest in contributing to Snap2Dish! We welcome contributions from the community and are excited to have you on board. This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be kind, considerate, and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/snap2dish.git
   cd snap2dish
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/1happybot/snap2dish.git
   ```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher
- Git
- Virtual environment tool (venv)

### Installation Steps

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development dependencies** (for linting and testing):
   ```bash
   pip install flake8 black isort bandit pytest pytest-flask pytest-cov
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Set up the database**:
   ```bash
   createdb snap2dish
   flask init-db
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

## How to Contribute

### Finding an Issue

- Check the [Issues](https://github.com/1happybot/snap2dish/issues) page for open issues
- Look for issues labeled `good first issue` or `help wanted` if you're new
- Comment on the issue to let others know you're working on it

### Creating a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Use descriptive branch names:
- `feature/add-search-functionality`
- `fix/login-redirect-bug`
- `docs/update-installation-guide`

## Code Style Guidelines

We maintain consistent code style across the project. Please follow these guidelines:

### Python Code Style

- **PEP 8**: Follow [PEP 8](https://pep8.org/) style guide
- **Line Length**: Maximum 127 characters per line
- **Formatting**: Use `black` for automatic code formatting
- **Import Sorting**: Use `isort` with black profile
- **Linting**: Code must pass `flake8` checks

### Running Code Quality Tools

Before committing, ensure your code passes all checks:

```bash
# Format code with black
black .

# Sort imports
isort --profile black .

# Run flake8 linting
flake8 . --max-line-length=127 --exclude=venv,__pycache__,.git,uploads

# Run security checks
bandit -r . --exclude ./venv,./uploads
```

### Docstrings

Use clear docstrings for functions and classes:

```python
def analyze_image(image_path: str) -> Dict[str, any]:
    """
    Analyze a food image and return dish information.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing dish_name, ingredients, and instructions
        
    Raises:
        ValueError: If image_path is invalid
    """
    pass
```

### Comments

- Write self-documenting code where possible
- Add comments for complex logic or business rules
- Keep comments concise and up-to-date

## Testing

### Running Tests

Always run tests before submitting a pull request:

```bash
# Run all tests
pytest test_app.py -v

# Run with coverage report
pytest test_app.py --cov=. --cov-report=html

# Run specific test
pytest test_app.py::test_function_name -v
```

### Writing Tests

- Add tests for new features
- Ensure tests are isolated and don't depend on each other
- Use descriptive test names that explain what is being tested
- Follow existing test patterns in `test_app.py`

Example test structure:

```python
def test_feature_name(client):
    """Test that feature works correctly."""
    # Arrange
    data = {'key': 'value'}
    
    # Act
    response = client.post('/endpoint', data=data)
    
    # Assert
    assert response.status_code == 200
    assert 'expected' in response.data.decode()
```

## Submitting Changes

### Before Submitting

1. **Ensure all tests pass**:
   ```bash
   pytest test_app.py -v
   ```

2. **Run linting and formatting**:
   ```bash
   black .
   isort --profile black .
   flake8 . --max-line-length=127 --exclude=venv,__pycache__,.git,uploads
   ```

3. **Run security checks**:
   ```bash
   bandit -r . --exclude ./venv,./uploads
   ```

4. **Update documentation** if needed

5. **Commit your changes** with a clear message:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

### Commit Message Guidelines

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Add detailed description after a blank line if needed

Examples:
```
Add user profile image upload feature

- Implement image upload endpoint
- Add file validation
- Update user model with profile_image field
```

### Creating a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference any related issues (e.g., "Fixes #123")
   - Describe what changes were made and why
   - Include screenshots for UI changes

3. **Wait for review**:
   - Respond to feedback promptly
   - Make requested changes in new commits
   - Be open to suggestions and discussions

### Pull Request Template

Use this template for your PR description:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Related Issue
Fixes #(issue number)

## Changes Made
- List of changes
- Another change

## Testing
- [ ] All tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Reporting Bugs

Found a bug? Help us fix it!

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with the following:
   - Clear, descriptive title
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots or error messages if applicable

### Bug Report Template

```markdown
**Description**
A clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- Browser: [e.g., Chrome 120]

**Screenshots**
Add screenshots if applicable
```

## Feature Requests

Have an idea for a new feature?

1. **Check existing issues** for similar requests
2. **Create a feature request issue**:
   - Describe the feature and its benefits
   - Explain the use case
   - Suggest implementation approach (optional)

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Problem it Solves**
What problem does this feature address?

**Proposed Solution**
How would you like it to work?

**Alternatives Considered**
Any alternative solutions you've considered?

**Additional Context**
Any other context or screenshots
```

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Issues**: Check the [Issues](https://github.com/1happybot/snap2dish/issues) page
- **Documentation**: Refer to the [README.md](README.md)

## Recognition

Contributors will be recognized in our project! Thank you for making Snap2Dish better! 🎉

---

**Happy Contributing! 🚀**

Made with ❤️ by the Snap2Dish community
