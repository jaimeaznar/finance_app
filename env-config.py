# .env file (not to be committed to version control)
FLASK_APP=app.py
FLASK_ENV=development
OPENAI_API_KEY=your-openai-api-key-here

# Add this to app.py to load environment variables
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# You can then access environment variables like this
openai_api_key = os.environ.get("OPENAI_API_KEY")
