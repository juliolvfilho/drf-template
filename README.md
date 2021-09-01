# drf-template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

My project template to start projects with Django REST framework

### Description

- Django 3.2 (Python 3.8 recommended)
- Django Rest Framework 3.12
- Removed all non-essential apps and middleware
- Flake8 + Black (linter and formatter)
- Default Throttling (prevents a user from making the same API call twice in a very short period)


### Setup

1. Clone this repository
   ```sh
   git clone https://github.com/juliolvfilho/drf-template my-new-project-name
   ```
2. Reset git
   ```sh
   cd my-new-project-name
   rm -rf .git
   git init .
   git add -A && git commit -m "Clone drf-template"
   ```
3. Prepare your Python environment
   
    3.1 Example using [pyenv](https://github.com/pyenv/pyenv) (recommended)
    ```sh
    # Install the desired Python version (if you haven't already)
    pyenv install 3.8.7
    # Create a virtualenv using the desired Python version
    pyenv virtualenv 3.8.7 my-new-project-env
    # Set the virtual environment inside the project directory
    pyenv local my-new-project-env
    ```
    
    3.2 Example using [python3-venv](https://docs.python.org/3/library/venv.html)
    ```sh
    # Create a virtual environment from the system's Python version
    python3 -m venv .env
    # Activate the virtual environment
    source .env/bin/activate
    ```
4. Install dependencies
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
