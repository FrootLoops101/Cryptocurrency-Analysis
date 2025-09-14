Cryptocurrency Analysis Multi-Agent System
A Python-based multi-agent system that fetches real-time news and historical cryptocurrency prices, analyzes market sentiment and trends, and generates actionable investment reports—optimized for cost, speed, and accuracy.

Features
Multi-Agent Architecture: Coordinator, News Analyst, Price Analyst, and Report Writer.

Real-Time News Sentiment: Automated semantic search and analysis.

Technical Price Analysis: Historical data and trend evaluation.

Robust Error Handling: Graceful API failure recovery.

Token-Efficient: Optimized for rate limits and low-cost operation.

Production-Ready: Includes Docker, CI/CD, and full documentation.

Quick Start
bash
git clone https://github.com/your-username/crypto-analysis.git
cd crypto-analysis
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_api_key"
python efficient_crypto_analysis.py
Project Structure
text
crypto-analysis/
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── crypto_analysis.py
├── efficient_crypto_analysis.py
├── test_environment.py
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci-cd.yml
Configuration
Required: GROQ_API_KEY (Groq LLM)

Optional: EXA_API_KEY (news), ALPHA_VANTAGE_KEY (prices)

Example Output
Sentiment: Moderately Bullish

Price: $58,500, Weekly Change: +1.2%

Summary: Bullish momentum, institutional interest, risk warning.
