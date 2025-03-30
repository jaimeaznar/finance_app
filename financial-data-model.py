import json
import random
import datetime
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

class ChileanSMEFinancialDataGenerator:
    """
    Generator for realistic financial data for a Chilean SME following IFRS standards.
    Generates two full years of financial data including balance sheets, income statements,
    and cash flow statements.
    """
    
    def __init__(self, company_name="Company A", industry="Technology", start_date="2023-01-01"):
        """Initialize the data generator with company details and timeframe."""
        self.company_name = company_name
        self.industry = industry
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = self.start_date + relativedelta(years=2) - relativedelta(days=1)
        
        # Initial financial constants (in millions of CLP)
        self.initial_assets = random.uniform(800, 1200)
        self.revenue_growth_rate = random.uniform(0.10, 0.25)  # 10-25% annual growth
        self.gross_margin = random.uniform(0.40, 0.60)  # 40-60% gross margin
        self.opex_ratio = random.uniform(0.25, 0.35)  # 25-35% of revenue
        self.tax_rate = 0.27  # Chile's corporate tax rate
        
        # Seasonality factors for monthly revenue (Jan=index 0)
        self.seasonality = [0.85, 0.80, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.10, 1.05, 1.30]
        
        # Storage for generated data
        self.monthly_data = []
        self.quarterly_data = []
        self.yearly_data = []
        
    def generate_all_data(self):
        """Generate all financial data for the specified timeframe."""
        self._generate_monthly_data()
        self._generate_quarterly_data()
        self._generate_yearly_data()
        return {
            "company_info": {
                "name": self.company_name,
                "industry": self.industry,
                "period_start": self.start_date.strftime("%Y-%m-%d"),
                "period_end": self.end_date.strftime("%Y-%m-%d")
            },
            "monthly_data": self.monthly_data,
            "quarterly_data": self.quarterly_data,
            "yearly_data": self.yearly_data
        }
    
    def _generate_monthly_data(self):
        """Generate monthly financial statements."""
        current_date = self.start_date
        last_month_data = None
        
        while current_date <= self.end_date:
            month_num = current_date.month - 1  # 0-indexed month for seasonality
            year_progress = (current_date - self.start_date).days / 365
            
            # Calculate base metrics with growth over time
            base_revenue = self.initial_assets * 0.15 * (1 + self.revenue_growth_rate) ** year_progress
            # Apply seasonality factor
            revenue = base_revenue * self.seasonality[month_num]
            
            # Calculate other income statement items
            cogs = revenue * (1 - self.gross_margin)
            gross_profit = revenue - cogs
            operating_expenses = revenue * self.opex_ratio
            ebitda = gross_profit - operating_expenses
            
            # Randomize depreciation and amortization (3-7% of revenue)
            depreciation = revenue * random.uniform(0.03, 0.07)
            
            # Calculate EBIT and other metrics
            ebit = ebitda - depreciation
            financial_expenses = self.initial_assets * 0.005 * (1 - year_progress * 0.1)  # Decreasing over time
            ebt = ebit - financial_expenses
            tax = max(0, ebt * self.tax_rate)
            net_income = ebt - tax
            
            # Calculate balance sheet items
            if last_month_data:
                prev_cash = last_month_data["balance_sheet"]["cash_and_equivalents"]
                prev_assets = last_month_data["balance_sheet"]["total_assets"]
                prev_equity = last_month_data["balance_sheet"]["total_equity"]
            else:
                prev_cash = self.initial_assets * 0.15
                prev_assets = self.initial_assets
                prev_equity = self.initial_assets * 0.4
            
            # Cash changes (simplified)
            cash_from_operations = net_income + depreciation - random.uniform(0, net_income * 0.3)
            cash_from_investing = -random.uniform(depreciation * 0.5, depreciation * 1.5)
            cash_from_financing = -random.uniform(0, net_income * 0.2)
            net_cash_change = cash_from_operations + cash_from_investing + cash_from_financing
            
            # Balance sheet construction
            cash = prev_cash + net_cash_change
            accounts_receivable = revenue * random.uniform(0.5, 0.7)
            inventory = cogs * random.uniform(0.3, 0.5)
            current_assets = cash + accounts_receivable + inventory
            
            ppe = prev_assets * 0.5 - depreciation + max(0, -cash_from_investing)
            intangible_assets = prev_assets * 0.1
            other_noncurrent_assets = prev_assets * 0.1
            noncurrent_assets = ppe + intangible_assets + other_noncurrent_assets
            
            total_assets = current_assets + noncurrent_assets
            
            # Liabilities
            accounts_payable = cogs * random.uniform(0.4, 0.6)
            short_term_debt = total_assets * random.uniform(0.05, 0.15)
            current_liabilities = accounts_payable + short_term_debt
            
            long_term_debt = total_assets * random.uniform(0.2, 0.3)
            other_noncurrent_liabilities = total_assets * random.uniform(0.05, 0.1)
            noncurrent_liabilities = long_term_debt + other_noncurrent_liabilities
            
            total_liabilities = current_liabilities + noncurrent_liabilities
            
            # Equity
            equity = total_assets - total_liabilities
            retained_earnings = prev_equity + net_income - random.uniform(0, net_income * 0.3)  # Some dividends
            capital = equity - retained_earnings
            
            month_data = {
                "date": current_date.strftime("%Y-%m-%d"),
                "year": current_date.year,
                "month": current_date.month,
                "income_statement": {
                    "revenue": round(revenue, 2),
                    "cost_of_goods_sold": round(cogs, 2),
                    "gross_profit": round(gross_profit, 2),
                    "operating_expenses": round(operating_expenses, 2),
                    "ebitda": round(ebitda, 2),
                    "depreciation_amortization": round(depreciation, 2),
                    "ebit": round(ebit, 2),
                    "financial_expenses": round(financial_expenses, 2),
                    "ebt": round(ebt, 2),
                    "taxes": round(tax, 2),
                    "net_income": round(net_income, 2)
                },
                "balance_sheet": {
                    "cash_and_equivalents": round(cash, 2),
                    "accounts_receivable": round(accounts_receivable, 2),
                    "inventory": round(inventory, 2),
                    "total_current_assets": round(current_assets, 2),
                    "property_plant_equipment": round(ppe, 2),
                    "intangible_assets": round(intangible_assets, 2),
                    "other_noncurrent_assets": round(other_noncurrent_assets, 2),
                    "total_noncurrent_assets": round(noncurrent_assets, 2),
                    "total_assets": round(total_assets, 2),
                    "accounts_payable": round(accounts_payable, 2),
                    "short_term_debt": round(short_term_debt, 2),
                    "total_current_liabilities": round(current_liabilities, 2),
                    "long_term_debt": round(long_term_debt, 2),
                    "other_noncurrent_liabilities": round(other_noncurrent_liabilities, 2),
                    "total_noncurrent_liabilities": round(noncurrent_liabilities, 2),
                    "total_liabilities": round(total_liabilities, 2),
                    "capital": round(capital, 2),
                    "retained_earnings": round(retained_earnings, 2),
                    "total_equity": round(equity, 2)
                },
                "cash_flow_statement": {
                    "cash_from_operations": round(cash_from_operations, 2),
                    "cash_from_investing": round(cash_from_investing, 2),
                    "cash_from_financing": round(cash_from_financing, 2),
                    "net_change_in_cash": round(net_cash_change, 2),
                    "beginning_cash_balance": round(prev_cash, 2),
                    "ending_cash_balance": round(cash, 2)
                },
                "financial_ratios": {
                    "current_ratio": round(current_assets / current_liabilities, 2) if current_liabilities > 0 else "N/A",
                    "quick_ratio": round((current_assets - inventory) / current_liabilities, 2) if current_liabilities > 0 else "N/A",
                    "debt_to_equity": round(total_liabilities / equity, 2) if equity > 0 else "N/A",
                    "return_on_assets": round(net_income / total_assets * 100, 2) if total_assets > 0 else "N/A",
                    "return_on_equity": round(net_income / equity * 100, 2) if equity > 0 else "N/A",
                    "profit_margin": round(net_income / revenue * 100, 2) if revenue > 0 else "N/A",
                    "inventory_turnover": round(cogs / inventory, 2) if inventory > 0 else "N/A"
                }
            }
            
            self.monthly_data.append(month_data)
            last_month_data = month_data
            current_date = current_date + relativedelta(months=1)
    
    def _generate_quarterly_data(self):
        """Aggregate monthly data into quarterly reports."""
        quarters = {}
        
        for month_data in self.monthly_data:
            year = month_data["year"]
            month = month_data["month"]
            quarter = (month - 1) // 3 + 1
            quarter_key = f"{year}Q{quarter}"
            
            if quarter_key not in quarters:
                quarters[quarter_key] = {
                    "date": f"{year}-{quarter*3-2:02d}-01",  # First day of first month in quarter
                    "year": year,
                    "quarter": quarter,
                    "income_statement": {k: 0 for k in month_data["income_statement"].keys()},
                    "cash_flow_statement": {k: 0 for k in month_data["cash_flow_statement"].keys() 
                                          if k not in ["beginning_cash_balance", "ending_cash_balance"]},
                    "months_included": []
                }
            
            # Aggregate income statement and cash flow
            for key in month_data["income_statement"]:
                quarters[quarter_key]["income_statement"][key] += month_data["income_statement"][key]
                
            for key in month_data["cash_flow_statement"]:
                if key not in ["beginning_cash_balance", "ending_cash_balance"]:
                    quarters[quarter_key]["cash_flow_statement"][key] += month_data["cash_flow_statement"][key]
            
            quarters[quarter_key]["months_included"].append(month)
            
            # Last month of the quarter - add balance sheet
            if month % 3 == 0 or month == 12:
                quarters[quarter_key]["balance_sheet"] = month_data["balance_sheet"]
                quarters[quarter_key]["financial_ratios"] = month_data["financial_ratios"]
        
        # Convert dictionary to list and sort by date
        self.quarterly_data = list(quarters.values())
        self.quarterly_data.sort(key=lambda x: (x["year"], x["quarter"]))
    
    def _generate_yearly_data(self):
        """Aggregate data into yearly financial statements."""
        years = {}
        
        for month_data in self.monthly_data:
            year = month_data["year"]
            
            if year not in years:
                years[year] = {
                    "year": year,
                    "income_statement": {k: 0 for k in month_data["income_statement"].keys()},
                    "cash_flow_statement": {k: 0 for k in month_data["cash_flow_statement"].keys() 
                                          if k not in ["beginning_cash_balance", "ending_cash_balance"]},
                }
            
            # Aggregate income statement and cash flow
            for key in month_data["income_statement"]:
                years[year]["income_statement"][key] += month_data["income_statement"][key]
                
            for key in month_data["cash_flow_statement"]:
                if key not in ["beginning_cash_balance", "ending_cash_balance"]:
                    years[year]["cash_flow_statement"][key] += month_data["cash_flow_statement"][key]
            
            # December data - use for balance sheet
            if month_data["month"] == 12:
                years[year]["balance_sheet"] = month_data["balance_sheet"]
                # Calculate annual ratios
                annual_net_income = years[year]["income_statement"]["net_income"]
                annual_revenue = years[year]["income_statement"]["revenue"]
                total_assets = month_data["balance_sheet"]["total_assets"]
                total_equity = month_data["balance_sheet"]["total_equity"]
                current_assets = month_data["balance_sheet"]["total_current_assets"]
                current_liabilities = month_data["balance_sheet"]["total_current_liabilities"]
                inventory = month_data["balance_sheet"]["inventory"]
                total_liabilities = month_data["balance_sheet"]["total_liabilities"]
                
                years[year]["financial_ratios"] = {
                    "current_ratio": round(current_assets / current_liabilities, 2) if current_liabilities > 0 else "N/A",
                    "quick_ratio": round((current_assets - inventory) / current_liabilities, 2) if current_liabilities > 0 else "N/A",
                    "debt_to_equity": round(total_liabilities / total_equity, 2) if total_equity > 0 else "N/A",
                    "return_on_assets": round(annual_net_income / total_assets * 100, 2) if total_assets > 0 else "N/A",
                    "return_on_equity": round(annual_net_income / total_equity * 100, 2) if total_equity > 0 else "N/A",
                    "profit_margin": round(annual_net_income / annual_revenue * 100, 2) if annual_revenue > 0 else "N/A"
                }
        
        # Convert dictionary to list and sort by year
        self.yearly_data = list(years.values())
        self.yearly_data.sort(key=lambda x: x["year"])

    def save_to_json(self, filename="chilean_sme_financial_data.json"):
        """Save the generated data to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.generate_all_data(), f, indent=2)
            
    def create_financing_data(self):
        """Generate financing history and options data."""
        # Current date for reference
        current_date = datetime.datetime.now()
        
        # Credit score (range 1-100, Chile uses a different scoring system than US)
        credit_score = random.randint(65, 95)
        
        # Contract limit based on company size and credit score (in millions)
        contract_limit = round(self.initial_assets * (credit_score / 100) * 0.5, 2)
        
        # Generate financing history
        financing_history = []
        for i in range(5):
            # Random date within the last year
            days_ago = random.randint(30, 365)
            request_date = (current_date - datetime.timedelta(days=days_ago)).strftime("%b %d, %Y")
            
            # Random amount based on contract limit
            amount = round(random.uniform(contract_limit * 0.1, contract_limit * 0.4), 2)
            
            # Random status weighted toward completed
            status_options = ["Waiting approval", "Denied", "Closed"]
            status_weights = [0.2, 0.1, 0.7]
            status = random.choices(status_options, status_weights)[0]
            
            # Generate contract number
            contract_number = f"NR-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            financing_history.append({
                "id": i + 1,
                "contract_number": contract_number,
                "request_date": request_date,
                "status": status,
                "due_date": (current_date - datetime.timedelta(days=random.randint(0, 30))).strftime("%m/%d/%Y") if status == "Closed" else "",
                "days_until_payment": random.randint(0, 30) if status != "Closed" else 0,
                "amount": amount
            })
        
        # Generate investment options
        investment_options = []
        for i in range(7):
            # Product ID
            product_id = 30 + i
            
            # Description
            descriptions = ["Pay an invoice", "Investments", "Urgent fees"]
            description = descriptions[random.randint(0, min(2, len(descriptions)-1))]
            
            # Request date - next month
            request_date = (current_date + datetime.timedelta(days=random.randint(1, 30))).strftime("%b %d, %Y")
            
            # Timeframe in weeks
            timeframe = random.choice([12, 24, 36, 48])
            
            # Risk score (0-100)
            customer_credit = random.randint(50, 99)
            
            # Yes/No field
            default_risk = random.choice(["YES", "NO"])
            
            # Amount
            amount = round(random.uniform(1000, 5000), 2)
            
            investment_options.append({
                "id": product_id,
                "description": description,
                "request_date": request_date,
                "timeframe": timeframe,
                "customer_credit": customer_credit,
                "default_risk": default_risk,
                "amount": amount
            })
        
        return {
            "credit_score": credit_score,
            "contract_limit": contract_limit,
            "financing_history": financing_history,
            "investment_options": investment_options
        }
    
    def generate_ai_recommendations(self):
        """Generate AI recommendations based on financial data."""
        # Get recent financial data
        if not self.monthly_data:
            self._generate_monthly_data()
            
        recent_data = self.monthly_data[-1]
        
        # Calculate some metrics
        cash_balance = recent_data["balance_sheet"]["cash_and_equivalents"]
        monthly_revenue = recent_data["income_statement"]["revenue"]
        monthly_expenses = recent_data["income_statement"]["operating_expenses"] + recent_data["income_statement"]["cost_of_goods_sold"]
        
        # Random upcoming payment
        upcoming_payment = round(random.uniform(500, 2000), 2)
        
        # Random potential revenue increase
        potential_revenue_increase = round(monthly_revenue * random.uniform(0.05, 0.15), 2)
        
        # Random invoices due
        invoices_due = []
        total_invoices = random.randint(2, 4)
        total_invoice_value = 0
        
        for i in range(total_invoices):
            invoice_value = round(random.uniform(300, 1000), 2)
            total_invoice_value += invoice_value
            invoices_due.append({
                "id": f"INV-{random.randint(1000, 9999)}",
                "value": invoice_value,
                "due_date": (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 7))).strftime("%b %d")
            })
        
        recommendations = {
            "financial_metrics": {
                "cash_balance": cash_balance,
                "projected_revenues": monthly_revenue * 12,
                "expected_net_cash": cash_balance + (monthly_revenue - monthly_expenses) * 3,
                "cash_balance_change": round(random.uniform(-2.0, 2.0), 1),
                "revenue_change": round(random.uniform(-5.0, 5.0), 1),
                "net_cash_change": round(random.uniform(-3.0, 3.0), 1)
            },
            "recommendations": [
                {
                    "type": "cash_flow",
                    "title": "Cash Flow Optimization",
                    "description": f"Upcoming payment of ${upcoming_payment} may impact your cash balance. Consider invoicing project ABC early.",
                    "potential": round(random.uniform(1000, 3000), 0),
                    "action": "Send Invoice"
                },
                {
                    "type": "revenue",
                    "title": "Revenue Opportunity",
                    "description": f"Upselling to Segment A customers typically increase orders by 10-15% in the next month. Consider reaching out.",
                    "potential": round(potential_revenue_increase, 0),
                    "action": "Send Email"
                },
                {
                    "type": "payment",
                    "title": "Payment Due Soon",
                    "description": f"{total_invoices} invoices worth ${total_invoice_value:.2f} are due in the next 7 days. Schedule payments now.",
                    "due_date": (datetime.datetime.now() + datetime.timedelta(days=random.randint(5, 20))).strftime("%b %d"),
                    "action": "Schedule Payment Now"
                }
            ],
            "common_questions": [
                "How can I optimize my business cashflow?",
                "What expenses are increasing the most this month?",
                "Predict my financial status in 30 days?"
            ]
        }
        
        return recommendations

# Example usage
if __name__ == "__main__":
    generator = ChileanSMEFinancialDataGenerator()
    financial_data = generator.generate_all_data()
    financing_data = generator.create_financing_data()
    ai_recommendations = generator.generate_ai_recommendations()
    
    # Save to files
    with open("chilean_sme_financial_data.json", "w") as f:
        json.dump(financial_data, f, indent=2)
    
    with open("financing_data.json", "w") as f:
        json.dump(financing_data, f, indent=2)
        
    with open("ai_recommendations.json", "w") as f:
        json.dump(ai_recommendations, f, indent=2)
    
    print("Financial data generated successfully!")
