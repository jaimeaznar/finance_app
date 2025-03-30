# SME Financial Management App

A demo application for SMEs to help them manage their financials and find financing options.

## Features

- **AI Assistant**: Get financial advice and recommendations based on your business data
- **Financial Options**: View and manage financing opportunities
- **Investment Options**: Explore investment opportunities
- **Portfolio Dashboard**: Track your financial investments
- **Integrations**: Connect with third-party services

## Tech Stack

- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Backend**: Python (Flask)
- **AI Integration**: Configured for OpenAI API integration

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sme-financial-app.git
   cd sme-financial-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   OPENAI_API_KEY=your-openai-api-key  # Replace with your actual OpenAI API key if using AI integration
   ```

6. Run the application:
   ```
   flask run
   ```

7. Access the application at `http://localhost:5000`

## Deployment

### Deploying to Heroku

1. Create a Heroku account if you don't have one: [https://signup.heroku.com/](https://signup.heroku.com/)

2. Install Heroku CLI: [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

3. Log in to Heroku from the terminal:
   ```
   heroku login
   ```

4. Create a new Heroku app:
   ```
   heroku create sme-financial-app
   ```

5. Add environment variables:
   ```
   heroku config:set OPENAI_API_KEY=your-openai-api-key
   ```

6. Deploy the application:
   ```
   git push heroku main
   ```

7. Open the deployed app:
   ```
   heroku open
   ```

### Deploying to DigitalOcean App Platform

1. Create a DigitalOcean account if you don't have one

2. In the DigitalOcean dashboard, click on "Apps" in the left sidebar

3. Click "Create App" and select "GitHub" as the source

4. Select your repository and branch

5. Configure the app:
   - Select the Python environment
   - Set the run command to `gunicorn app:app`
   - Add environment variables (OPENAI_API_KEY, etc.)

6. Click "Next" and then "Create Resources"

7. Once deployed, you can access your app via the provided URL

## Project Structure

```
sme-financial-app/
├── app.py                  # Main Flask application
├── financial_data_generator.py  # Data generation script
├── data/                   # Generated financial data
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── index.html          # Main dashboard / AI Chat page
│   ├── financial_options.html  # Financial options page
│   ├── investment_options.html  # Investment options page
│   ├── dashboard.html      # Portfolio dashboard page
│   ├── plugins.html        # Integrations/plugins page
│   └── financing_request.html  # Financing request form
├── requirements.txt        # Python dependencies
├── Procfile               # For Heroku deployment
└── README.md              # Project documentation
```

## Notes for Demo

This application is designed for demonstration purposes and uses generated dummy data. In a production environment, you would need to:

1. Implement proper authentication and security measures
2. Connect to real financial data sources
3. Enhance the AI integration with more sophisticated models
4. Add comprehensive error handling and logging
5. Implement proper database storage instead of file-based storage

## License

This project is licensed under the MIT License - see the LICENSE file for details.
