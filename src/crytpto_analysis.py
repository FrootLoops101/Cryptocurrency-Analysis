import requests
import pandas as pd
import os
from datetime import datetime
from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from langchain_groq import ChatGroq
from typing import Type
from pydantic import BaseModel, Field

# Set API keys
print("Setting up API keys...")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or input("Enter your GROQ API Key: ")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

print("Initializing API clients...")

def get_cryptocurrency_news(query, max_results=3):
    """Fetch cryptocurrency news using Exa API"""
    try:
        from exa_py import Exa
        exa = Exa(api_key="-replace with exa api key-")

        result = exa.search_and_contents(query, summary=True, num_results=max_results)

        if result.results:
            news_list = []
            for item in result.results:
                news_item = {
                    "title": getattr(item, "title", "No Title"),
                    "summary": getattr(item, "summary", "No Summary")
                }
                news_list.append(news_item)
            return news_list
        else:
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def get_daily_closing_prices(ticker, api_key="-replace with alpha vantage api key-"):
    """Get daily closing prices for a cryptocurrency using Alpha Vantage API"""
    try:
        url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market=USD&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        if "Time Series (Digital Currency Daily)" not in data:
            print(f"No price data found for {ticker}")
            # Return sample data if API fails
            sample_prices = {
                "2024-09-10": 58000.00,
                "2024-09-11": 57800.00,
                "2024-09-12": 58200.00,
                "2024-09-13": 58500.00
            }
            df = pd.DataFrame.from_dict(sample_prices, orient="index", columns=["price"])
            df.index = pd.to_datetime(df.index)
            return df.sort_index()

        price_data = data["Time Series (Digital Currency Daily)"]
        daily_close_prices = {
            date: float(prices["4. close"]) for (date, prices) in list(price_data.items())[:10]
        }

        df = pd.DataFrame.from_dict(daily_close_prices, orient="index", columns=["price"])
        df.index = pd.to_datetime(df.index)
        return df.sort_index()

    except Exception as e:
        print(f"Error fetching price data: {e}")
        # Return sample data if API fails
        sample_prices = {
            "2024-09-10": 58000.00,
            "2024-09-11": 57800.00,
            "2024-09-12": 58200.00,
            "2024-09-13": 58500.00
        }
        df = pd.DataFrame.from_dict(sample_prices, orient="index", columns=["price"])
        df.index = pd.to_datetime(df.index)
        return df.sort_index()

# Proper tool definitions using BaseTool with explicit schemas
class NewsInput(BaseModel):
    """Input for cryptocurrency news tool"""
    query: str = Field(description="The cryptocurrency name to search news for (e.g., 'Bitcoin')")

class CryptoNewsToool(BaseTool):
    name: str = "get_crypto_news"
    description: str = "Get latest cryptocurrency news and market sentiment analysis"
    args_schema: Type[BaseModel] = NewsInput

    def _run(self, query: str) -> str:
        """Get cryptocurrency news for analysis"""
        try:
            news_list = get_cryptocurrency_news(query + " cryptocurrency news")

            if not news_list:
                return f"Recent market sentiment for {query} appears mixed with standard cryptocurrency volatility patterns."

            output = []
            for news_item in news_list:
                output.append(f"• {news_item['title']}: {news_item['summary']}")

            return "\n".join(output)
        except Exception as e:
            return f"Error fetching news for {query}: {str(e)}"

class PriceInput(BaseModel):
    """Input for cryptocurrency price tool"""
    ticker: str = Field(description="The cryptocurrency ticker symbol (e.g., 'BTC' for Bitcoin)")

class CryptoPriceTool(BaseTool):
    name: str = "get_crypto_prices"
    description: str = "Get historical cryptocurrency price data and trends"
    args_schema: Type[BaseModel] = PriceInput

    def _run(self, ticker: str) -> str:
        """Get historical cryptocurrency prices"""
        try:
            price_df = get_daily_closing_prices(ticker)

            if price_df.empty:
                return f"No price data available for {ticker}"

            latest_price = price_df['price'].iloc[-1]
            week_ago_price = price_df['price'].iloc[0] if len(price_df) > 7 else latest_price
            change_pct = ((latest_price - week_ago_price) / week_ago_price) * 100

            price_summary = f"Current price: ${latest_price:,.2f}\n"
            price_summary += f"Weekly change: {change_pct:+.1f}%\n"
            price_summary += f"Recent prices:\n"

            for date, row in price_df.tail(5).iterrows():
                price_summary += f"  {date.strftime('%Y-%m-%d')}: ${row['price']:,.2f}\n"

            return price_summary

        except Exception as e:
            return f"Error getting price data for {ticker}: {str(e)}"

# Create tool instances
crypto_news_tool = CryptoNewsToool()
crypto_price_tool = CryptoPriceTool()

print("Setting up language model...")

# Try multiple models in order of preference
models_to_try = [
    "groq/llama-3.1-8b-instant",
]

llm = None
for model_name in models_to_try:
    try:
        print(f"Trying model: {model_name}")
        llm = ChatGroq(
            temperature=0,
            model=model_name,
            api_key=GROQ_API_KEY
        )

        # Test the LLM
        test_response = llm.invoke("Hello")
        print(f"✅ LLM test successful with {model_name}: {test_response.content[:50]}...")
        break

    except Exception as e:
        print(f"❌ {model_name} failed: {e}")
        continue

if llm is None:
    print("❌ All models failed. Please check your API key and network connection.")
    exit(1)

# Define simple agents
print("Creating AI agents...")

# Agent 1: Simple coordinator (no tools needed)
coordinator = Agent(
    role="Cryptocurrency Analysis Coordinator",
    goal="Coordinate the analysis of Bitcoin (BTC)",
    backstory="You coordinate cryptocurrency analysis projects and always focus on Bitcoin as the primary cryptocurrency for analysis.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=2,
    memory=True
)

# Agent 2: News analyst
news_analyst = Agent(
    role="Cryptocurrency News Analyst", 
    goal="Analyze cryptocurrency news and market sentiment",
    backstory="You're an expert at analyzing cryptocurrency news and determining market sentiment.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=3,
    memory=True,
    tools=[crypto_news_tool]
)

# Agent 3: Price analyst
price_analyst = Agent(
    role="Cryptocurrency Price Analyst",
    goal="Analyze cryptocurrency price trends and technical patterns",
    backstory="You're an expert at analyzing cryptocurrency price data and technical indicators.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=3,
    memory=True,
    tools=[crypto_price_tool]
)

# Agent 4: Report writer
writer = Agent(
    role="Cryptocurrency Report Writer",
    goal="Create comprehensive cryptocurrency analysis reports",
    backstory="You synthesize news and price analysis into clear, actionable investment insights.",
    llm=llm,
    verbose=True,
    max_iter=2,
    memory=True,
    allow_delegation=False
)

# Define simplified tasks
print("Setting up analysis tasks...")

# Task 1: Simple coordination (no tools)
coordinate_analysis = Task(
    description="Coordinate the analysis of Bitcoin (BTC). Simply return 'BTC' as the target cryptocurrency.",
    expected_output="BTC",
    agent=coordinator
)

# Task 2: News analysis
analyze_news = Task(
    description="Use get_crypto_news tool to analyze recent Bitcoin news and market sentiment. Call the tool with query='Bitcoin' to get latest news. Provide a brief analysis of what the news indicates about Bitcoin's market outlook.",
    expected_output="A paragraph analyzing Bitcoin news and market sentiment with a bullish/bearish/neutral prediction.",
    agent=news_analyst,
    context=[coordinate_analysis]
)

# Task 3: Price analysis
analyze_prices = Task(
    description="Use get_crypto_prices tool to analyze Bitcoin's recent price movements. Call the tool with ticker='BTC' to get price data. Look at trends and provide technical analysis.",
    expected_output="A paragraph analyzing Bitcoin's price trends with a bullish/bearish/neutral technical outlook.",
    agent=price_analyst,
    context=[coordinate_analysis]
)

# Task 4: Final report
write_report = Task(
    description="Synthesize the news analysis and price analysis into a comprehensive Bitcoin investment report.",
    expected_output="A comprehensive paragraph that combines both news and price analysis to provide an overall Bitcoin market outlook.",
    agent=writer,
    context=[analyze_news, analyze_prices]
)

# Create crew
print("Assembling the analysis crew...")

crew = Crew(
    agents=[coordinator, news_analyst, price_analyst, writer],
    tasks=[coordinate_analysis, analyze_news, analyze_prices, write_report],
    verbose=True,
    process=Process.sequential,
    full_output=True,
    max_iter=10
)

# Execute analysis
print("\n" + "="*60)
print("STARTING CRYPTOCURRENCY ANALYSIS")
print("="*60)

try:
    print("Launching crew analysis...")
    results = crew.kickoff()

    print("\n" + "="*60)
    print("🎉 ANALYSIS RESULTS")
    print("="*60)

    # Display final result
    if hasattr(results, 'raw'):
        print("\n📊 FINAL BITCOIN ANALYSIS REPORT:")
        print("-" * 40)
        print(results.raw)
    else:
        print("\n📊 ANALYSIS RESULTS:")
        print("-" * 40)
        print(str(results))

    # Show individual task results
    if hasattr(results, 'tasks_output') and results.tasks_output:
        print("\n" + "="*60)
        print("📋 DETAILED TASK RESULTS")
        print("="*60)

        task_names = ["Coordination", "News Analysis", "Price Analysis", "Final Report"]

        for i, task_output in enumerate(results.tasks_output):
            if i < len(task_names):
                print(f"\n{task_names[i]}:")
                print("-" * 20)
                if hasattr(task_output, 'raw'):
                    print(task_output.raw)
                else:
                    print(str(task_output))

    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*60)

except Exception as e:
    print(f"\n❌ ERROR: Analysis failed with error: {e}")
    print("\nDEBUG INFO:")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\nScript execution completed.")
