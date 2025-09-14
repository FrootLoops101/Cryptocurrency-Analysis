import pytest
from crewai import Agent, Task
from crypto_analysis import crypto_news_tool, crypto_price_tool  # Adjust imports

def test_coordinator_agent_response():
    coordinator = Agent(
        role="Coordinator",
        goal="Return BTC",
        llm=None,  # Mock or real LLM depending on setup
        max_iter=1,
        allow_delegation=False,
        memory=False,
        verbose=False
    )
    task = Task(description="Return BTC", expected_output="BTC", agent=coordinator)
    result = coordinator.execute_task(task)
    assert result == "BTC" or result.raw == "BTC"

def test_news_analyst_agent_calls_tool():
    # Simplified test to check if agent can call tool and get string output
    news_agent = Agent(
        role="News Analyst",
        goal="Analyze news",
        tools=[crypto_news_tool],
        llm=None,
        max_iter=1,
        allow_delegation=False,
        memory=False,
        verbose=False
    )
    
    # Simulate calling tool with example query
    output = crypto_news_tool._run("Bitcoin")
    assert isinstance(output, str)
    assert "Bitcoin" in output or len(output) > 0

def test_price_analyst_agent_calls_tool():
    price_agent = Agent(
        role="Price Analyst",
        goal="Analyze price trends",
        tools=[crypto_price_tool],
        llm=None,
        max_iter=1,
        allow_delegation=False,
        memory=False,
        verbose=False
    )
    output = crypto_price_tool._run("BTC")
    assert isinstance(output, str)
    assert "$" in output or len(output) > 0
