import pytest
from crypto_analysis import crypto_news_tool, crypto_price_tool  # Adjust imports

def test_crypto_news_tool_valid_query():
    result = crypto_news_tool._run("Bitcoin")
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 10

def test_crypto_news_tool_invalid_query():
    result = crypto_news_tool._run("")
    assert result is not None
    assert isinstance(result, str)

def test_crypto_price_tool_valid_ticker():
    result = crypto_price_tool._run("BTC")
    assert result is not None
    assert isinstance(result, str)
    assert "$" in result

def test_crypto_price_tool_invalid_ticker():
    result = crypto_price_tool._run("")
    assert result is not None
    assert isinstance(result, str)
