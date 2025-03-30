from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import json
import random
from datetime import datetime, timedelta
import requests  # For AI service API calls

# Import our data generator
from financial_data_model import ChileanSMEFinancialDataGenerator

app = Flask(__name__)

# Initialize OpenAI API (you'll need to replace with your actual API key in production)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

# Load or generate data on startup
def load_or_generate_data():
    # Check if data files exist
    if (os.path.exists('data/chilean_sme_financial_data.json') and 
        os.path.exists('data/financing_data.json') and 
        os.path.exists('data/ai_recommendations.json')):
        
        # Load existing data
        with open('data/chilean_sme_financial_data.json', 'r') as f:
            financial_data = json.load(f)
        
        with open('data/financing_data.json', 'r') as f:
            financing_data = json.load(f)
            
        with open('data/ai_recommendations.json', 'r') as f:
            ai_recommendations = json.load(f)
    else:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Generate new data
        generator = ChileanSMEFinancialDataGenerator()
        financial_data = generator.generate_all_data()
        financing_data = generator.create_financing_data()
        ai_recommendations = generator.generate_ai_recommendations()
        
        # Save to files
        with open('data/chilean_sme_financial_data.json', 'w') as f:
            json.dump(financial_data, f, indent=2)
        
        with open('data/financing_data.json', 'w') as f:
            json.dump(financing_data, f, indent=2)
            
        with open('data/ai_recommendations.json', 'w') as f:
            json.dump(ai_recommendations, f, indent=2)
    
    return financial_data, financing_data, ai_recommendations

# Global data store
financial_data, financing_data, ai_recommendations = load_or_generate_data()

# --------------- Routes ---------------

@app.route('/')
def index():
    """Main dashboard / AI Chat page"""
    return render_template('index.html', 
                          recommendations=ai_recommendations,
                          user_name="David Smith",
                          company_name="Company A")

@app.route('/plugins')
def plugins():
    """Plug-in store page"""
    plugin_categories = [
        {
            "name": "Email Integration",
            "description": "Connect to your email",
            "icon": "email_icon.png",
            "installed": True
        },
        {
            "name": "Google Sheets Integration",
            "description": "Connect to your Google Sheets account",
            "icon": "sheets_icon.png",
            "installed": True
        },
        {
            "name": "Speech-to-Text (STT)",
            "description": "Connect to Speech-to-Text service",
            "icon": "speech_icon.png",
            "installed": True
        },
        {
            "name": "Slack",
            "description": "Connect to your Slack account",
            "icon": "slack_icon.png",
            "installed": False
        },
        {
            "name": "Factorit",
            "description": "Connect to your Factorit account to handle invoices",
            "icon": "factorit_icon.png",
            "installed": False
        },
        {
            "name": "Outlook",
            "description": "Connect to your Outlook account",
            "icon": "outlook_icon.png",
            "installed": True
        },
        {
            "name": "Gmail",
            "description": "Connect to your Gmail account",
            "icon": "gmail_icon.png",
            "installed": True
        }
    ]
    
    return render_template('plugins.html', 
                          plugin_categories=plugin_categories,
                          user_name="David Smith",
                          company_name="Company A")

@app.route('/financial-options')
def financial_options():
    """Financial options page"""
    return render_template('financial_options.html',
                          financing_data=financing_data,
                          user_name="David Smith",
                          company_name="Company A")

@app.route('/dashboard')
def dashboard():
    """Portfolio dashboard page"""
    # Get the most recent financial data for the dashboard
    latest_monthly = financial_data["monthly_data"][-1]
    
    portfolio_info = {
        "roi": 23.54,  # Example ROI percentage
        "open_contracts": sum(1 for item in financing_data["financing_history"] if item["status"] != "Closed"),
        "total_value": sum(item["amount"] for item in financing_data["financing_history"]),
        "active_investments": random.randint(3, 8),
        "contract_data": financing_data["financing_history"]
    }
    
    return render_template('dashboard.html',
                          portfolio=portfolio_info,
                          monthly_data=latest_monthly,
                          user_name="Elizabeth Jones",  # Different user for this view based on screenshots
                          company_name="Company XYZ")  # Different company for this view based on screenshots

@app.route('/financing-request/<request_id>')
def financing_request(request_id):
    """Financing request form page"""
    return render_template('financing_request.html',
                          request_id=request_id,
                          user_name="David Smith",
                          company_name="Company A")

@app.route('/investment-options')
def investment_options():
    """Investment options page"""
    return render_template('investment_options.html',
                          investment_options=financing_data["investment_options"],
                          user_name="Elizabeth Jones",
                          company_name="Company XYZ")

# --------------- API Endpoints ---------------

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with AI integration"""
    data = request.json
    user_message = data.get('message', '')
    
    # In a real application, you would call your AI service here
    # This is a placeholder for the demo
    
    # Simple rule-based responses for demo purposes
    if "cashflow" in user_message.lower() or "cash flow" in user_message.lower():
        response = {
            "text": "Based on your current financial data, I recommend optimizing your cash flow by invoicing clients earlier. Your accounts receivable are currently at 60 days on average, which is quite high. Reducing this to 45 days could improve your cash position by approximately 25%.",
            "recommendations": [
                {
                    "type": "cash_flow",
                    "title": "Invoice Earlier",
                    "action": "Create invoice templates"
                }
            ]
        }
    elif "expenses" in user_message.lower():
        response = {
            "text": "Your highest increasing expenses this month are marketing costs (up 12%) and software subscriptions (up 8%). I recommend reviewing your SaaS subscriptions for any unused services that could be cancelled.",
            "recommendations": [
                {
                    "type": "cost_cutting",
                    "title": "Review Subscriptions",
                    "action": "View subscription list"
                }
            ]
        }
    elif "predict" in user_message.lower() or "forecast" in user_message.lower():
        response = {
            "text": "Based on your current trends, in 30 days your financial position is projected to improve by 5.2%. Your cash reserves should increase to approximately $10.92M with sustained revenue growth at 3.8% monthly.",
            "recommendations": [
                {
                    "type": "planning",
                    "title": "Review 90-day forecast",
                    "action": "View forecast"
                }
            ]
        }
    else:
        response = {
            "text": "I can help analyze your financial data and provide recommendations for optimizing cash flow, managing expenses, and forecasting future performance. What specific aspect of your finances would you like to explore?",
            "recommendations": []
        }
    
    return jsonify(response)

@app.route('/api/financial-data')
def get_financial_data():
    """API endpoint to get financial data"""
    return jsonify(financial_data)

@app.route('/api/recommendations')
def get_recommendations():
    """API endpoint to get AI recommendations"""
    return jsonify(ai_recommendations)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
