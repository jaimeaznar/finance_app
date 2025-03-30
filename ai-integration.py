import os
import openai
from flask import Flask, request, jsonify

# Initialize OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

# This function would be part of your Flask application
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with OpenAI API integration"""
    data = request.json
    user_message = data.get('message', '')
    chat_history = data.get('history', [])
    
    # Prepare the financial context from your data
    financial_context = get_financial_context()  # You'd implement this function
    
    # Create the prompt with financial context
    system_prompt = f"""
    You are a financial assistant for SMEs in Chile. You have access to the following financial data:
    
    Cash Balance: ${financial_context['cash_balance']}M
    Revenue: ${financial_context['monthly_revenue']}M per month
    Expenses: ${financial_context['monthly_expenses']}M per month
    
    Your role is to provide financial advice, analyze trends, and suggest optimizations.
    Always provide specific, actionable advice based on the financial data.
    """
    
    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or another appropriate model
            messages=[
                {"role": "system", "content": system_prompt},
                # Include previous conversation history
                *[{"role": msg["role"], "content": msg["content"]} for msg in chat_history],
                # Add the current user message
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract the AI's response
        ai_message = response.choices[0].message.content
        
        # Generate relevant recommendations based on the user's question
        recommendations = generate_recommendations(user_message, financial_context)
        
        return jsonify({
            "text": ai_message,
            "recommendations": recommendations
        })
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return jsonify({
            "text": "I'm sorry, I encountered an error processing your request. Please try again.",
            "recommendations": []
        }), 500

def get_financial_context():
    """Get relevant financial data for the AI context"""
    # In a real application, you would fetch this from your database
    # For the demo, we'll use the generated data
    
    with open('data/chilean_sme_financial_data.json', 'r') as f:
        financial_data = json.load(f)
    
    with open('data/ai_recommendations.json', 'r') as f:
        recommendations = json.load(f)
    
    # Get the most recent financial data
    latest_month = financial_data["monthly_data"][-1]
    
    return {
        "cash_balance": recommendations["financial_metrics"]["cash_balance"],
        "monthly_revenue": latest_month["income_statement"]["revenue"],
        "monthly_expenses": latest_month["income_statement"]["operating_expenses"] + latest_month["income_statement"]["cost_of_goods_sold"],
        "accounts_receivable": latest_month["balance_sheet"]["accounts_receivable"],
        "accounts_payable": latest_month["balance_sheet"]["accounts_payable"],
        "inventory": latest_month["balance_sheet"]["inventory"],
        "current_ratio": latest_month["financial_ratios"]["current_ratio"],
        "profit_margin": latest_month["financial_ratios"]["profit_margin"]
    }

def generate_recommendations(user_message, financial_context):
    """Generate tailored recommendations based on user query and financial data"""
    recommendations = []
    
    # Simple rule-based recommendation system
    # In a real application, this could be much more sophisticated
    
    if any(word in user_message.lower() for word in ["cash", "cashflow", "cash flow", "liquidity"]):
        if financial_context["accounts_receivable"] > financial_context["monthly_revenue"] * 0.8:
            recommendations.append({
                "type": "cash_flow",
                "title": "Reduce Accounts Receivable",
                "description": f"Your accounts receivable (${ financial_context['accounts_receivable'] }M) are quite high compared to monthly revenue. Consider offering early payment discounts.",
                "potential": round(financial_context["accounts_receivable"] * 0.2 * 1000, 0),
                "action": "Create payment plan"
            })
    
    if any(word in user_message.lower() for word in ["expense", "cost", "spending"]):
        recommendations.append({
            "type": "expense",
            "title": "Expense Optimization",
            "description": "Analyzing your expense patterns reveals potential savings in operational costs.",
            "potential": round(financial_context["monthly_expenses"] * 0.05 * 1000, 0),
            "action": "View expense breakdown"
        })
    
    if any(word in user_message.lower() for word in ["forecast", "predict", "future"]):
        recommendations.append({
            "type": "forecast",
            "title": "Financial Forecast",
            "description": "Based on current trends, we project steady growth over the next quarter.",
            "action": "View detailed forecast"
        })
        
    # Always include at least one recommendation if none matched
    if not recommendations:
        recommendations.append({
            "type": "cash_flow",
            "title": "Cash Flow Health Check",
            "description": f"Your current ratio is {financial_context['current_ratio']}. A monthly review can identify optimization opportunities.",
            "action": "Run health check"
        })
    
    return recommendations
