🔑 API Setup Guide
Complete guide for setting up all required APIs for the Cryptocurrency Analysis Multi-Agent System.

📊 API Overview
API Service	Purpose	Free Tier	Paid Plans	Setup Difficulty
Groq	LLM Processing	6,000 TPM	$0.27/1M tokens	⭐⭐ Easy
Exa	News Search	1,000 searches	$10/10K searches	⭐⭐ Easy
Alpha Vantage	Price Data	25 calls/day	$50/mo unlimited	⭐ Very Easy
Total Setup Time: ~15 minutes
Monthly Free Usage: ~100 analyses
Paid Monthly Cost: ~$20-50 for heavy usage

🚀 Groq API Setup
Why Groq?
Speed: 10x faster inference than traditional APIs

Cost: Competitive pricing with generous free tier

Quality: Access to Llama 3.1 models

Reliability: 99.9% uptime SLA

Setup Steps
Create Account

Visit console.groq.com

Sign up with email or GitHub

Verify your email address

Generate API Key

bash
# Navigate to API Keys section
# Click "Create API Key"
# Name: "crypto-analysis-system"
# Copy the key (starts with gsk_...)
Set Environment Variable

bash
# Linux/Mac
export GROQ_API_KEY="gsk_your_key_here"
echo 'export GROQ_API_KEY="gsk_your_key_here"' >> ~/.bashrc

# Windows
set GROQ_API_KEY=gsk_your_key_here
Test Connection

python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="groq/llama-3.1-8b-instant",
    api_key="your_key"
)

response = llm.invoke("Hello")
print(f"Success: {response.content}")
Rate Limits & Pricing
Tier	TPM Limit	RPM Limit	Price per 1M Tokens
Free	6,000	30	$0.00
Dev	60,000	300	$0.27
Pro	600,000	3,000	$0.27
Available Models
python
# Recommended models
models = {
    "groq/llama-3.1-8b-instant": {
        "speed": "Very Fast",
        "quality": "Good",
        "context": "8K tokens",
        "recommended": True
    },
    "groq/llama-3.1-70b-versatile": {
        "speed": "Fast", 
        "quality": "Excellent",
        "context": "32K tokens",
        "recommended": False  # Higher cost
    },
    "groq/mixtral-8x7b-32768": {
        "speed": "Fast",
        "quality": "Very Good",
        "context": "32K tokens",
        "recommended": True
    }
}
🔍 Exa API Setup
Why Exa?
Semantic Search: Better than keyword-based search

Real-time: Latest news and content

Summaries: Built-in content summarization

Quality: Filters out spam and low-quality content

Setup Steps
Create Account

Visit exa.ai

Sign up with email

Complete onboarding

Get API Key

bash
# Visit Dashboard -> API Keys
# Click "Generate New Key"
# Copy the key
Test API

python
from exa_py import Exa

exa = Exa(api_key="your_key")
result = exa.search("Bitcoin news", num_results=3)

print(f"Found {len(result.results)} results")
for item in result.results:
    print(f"- {item.title}")
Usage Limits & Pricing
Plan	Searches/Month	Price	Features
Free	1,000	$0	Basic search
Starter	10,000	$10	Summaries included
Pro	100,000	$50	Advanced filters
Optimization Tips
python
# Optimize search queries for better results
optimized_queries = {
    "bitcoin_news": "Bitcoin cryptocurrency news",
    "price_analysis": "Bitcoin price technical analysis",
    "market_sentiment": "Bitcoin market sentiment analysis"
}

# Use filters for better quality
result = exa.search(
    "Bitcoin news",
    num_results=3,
    include_domains=["coindesk.com", "cointelegraph.com"],
    start_published_date="2024-09-01"
)
📈 Alpha Vantage API Setup
Why Alpha Vantage?
Comprehensive: Stock, crypto, forex data

Reliable: 99.5% uptime

Free Tier: Generous free usage

Easy Integration: Simple REST API

Setup Steps
Get Free API Key

Visit alphavantage.co/support/#api-key

Enter email address

Key sent to email instantly

Test Connection

python
import requests

api_key = "your_alpha_vantage_key"
url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey={api_key}"

response = requests.get(url)
data = response.json()

if "Time Series (Digital Currency Daily)" in data:
    print("✅ Alpha Vantage connected successfully")
Usage Limits
Tier	Calls/Day	Calls/Minute	Price
Free	25	5	$0
Basic	500	25	$50/mo
Pro	Unlimited	200	$150/mo
API Functions Used
python
# Functions we use in the project
functions = {
    "DIGITAL_CURRENCY_DAILY": {
        "purpose": "Daily cryptocurrency prices",
        "data_points": "Open, High, Low, Close, Volume",
        "history": "Full history available"
    }
}

# Example response structure
example_response = {
    "Time Series (Digital Currency Daily)": {
        "2024-09-13": {
            "1. open": "58000.00000000",
            "2. high": "59500.00000000", 
            "3. low": "57800.00000000",
            "4. close": "58500.00000000",
            "5. volume": "1234567.89012345"
        }
    }
}
🔒 Security Best Practices
API Key Management
bash
# 1. Use environment variables (recommended)
export GROQ_API_KEY="gsk_..."
export EXA_API_KEY="..."
export ALPHA_VANTAGE_KEY="..."

# 2. Use .env file (for development)
echo "GROQ_API_KEY=gsk_..." >> .env
echo "EXA_API_KEY=..." >> .env
echo "ALPHA_VANTAGE_KEY=..." >> .env

# 3. Add .env to .gitignore
echo ".env" >> .gitignore
Key Rotation Schedule
Groq: Rotate every 90 days

Exa: Rotate every 90 days

Alpha Vantage: Rotate annually

Monitoring Usage
python
def monitor_api_usage():
    """Monitor API usage across all services."""
    usage_stats = {
        "groq_tokens": get_groq_token_usage(),
        "exa_searches": get_exa_search_count(),
        "alphavantage_calls": get_av_call_count()
    }

    # Alert if approaching limits
    for service, usage in usage_stats.items():
        if usage["percentage"] > 80:
            print(f"⚠️ {service} usage at {usage['percentage']}%")

    return usage_stats
🚨 Troubleshooting
Common API Issues
Invalid API Key

text
Error: 401 Unauthorized
Solution: Verify key is correct and active
Rate Limit Exceeded

text
Error: 429 Too Many Requests
Solution: Wait or upgrade plan
Quota Exceeded

text
Error: 403 Forbidden  
Solution: Wait for reset or upgrade
Debug Mode
python
import logging

# Enable debug logging for all APIs
logging.basicConfig(level=logging.DEBUG)

# Test each API individually
def test_apis():
    tests = {
        "groq": test_groq_api(),
        "exa": test_exa_api(),
        "alphavantage": test_av_api()
    }

    for api, status in tests.items():
        print(f"{api.upper()}: {'✅' if status else '❌'}")
💡 Cost Optimization Tips
Token Usage Optimization
python
# Groq token optimization strategies
optimization_tips = {
    "shorter_prompts": "Use concise, focused prompts",
    "efficient_models": "Use llama-3.1-8b-instant for basic tasks",
    "batch_processing": "Analyze multiple cryptos in one request",
    "caching": "Cache LLM responses for repeated queries",
    "early_termination": "Stop analysis on clear signals"
}

# Estimated costs per analysis
cost_breakdown = {
    "groq_tokens": "$0.003",
    "exa_searches": "$0.01", 
    "alphavantage_calls": "$0.00",  # Free tier
    "total_per_analysis": "$0.013"
}
Free Tier Maximization
python
# Maximize free tier usage
def optimize_free_usage():
    strategies = [
        "Use efficient_crypto_analysis.py",
        "Batch multiple cryptocurrencies",
        "Cache results for 1 hour",
        "Use minimal verbose output",
        "Implement smart retry logic"
    ]
    return strategies
