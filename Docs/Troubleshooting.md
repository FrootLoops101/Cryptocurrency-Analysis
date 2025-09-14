#  Troubleshooting Guide

This guide covers common issues and their solutions for the Cryptocurrency Analysis Multi-Agent System.

##  Common Issues

### 1. Rate Limit Errors 

#### Symptoms
```
RateLimitError: GroqException - Rate limit reached for model
TPM: Limit 6000, Used 5526, Requested 535
```

#### Solutions
```python
# Option 1: Use efficient version
python efficient_crypto_analysis.py

# Option 2: Add delays between requests
import time
time.sleep(2)  # Wait 2 seconds between calls

# Option 3: Upgrade API tier
# Visit: https://console.groq.com/settings/billing
```

#### Prevention
- Use `efficient_crypto_analysis.py` for free tiers
- Monitor token usage with verbose logging
- Implement exponential backoff

### 2. Tool Validation Errors 

#### Symptoms
```
Arguments validation failed: 1 validation error for Get_Crypto_News
Input should be a valid string [type=string_type]
```

#### Root Cause
LLM passes dictionary instead of string to tools

#### Solution
```python
# Use BaseTool class with proper schema
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class NewsInput(BaseModel):
    query: str = Field(description="Cryptocurrency name")

class CryptoNewsTool(BaseTool):
    name: str = "get_crypto_news"
    args_schema: Type[BaseModel] = NewsInput
    
    def _run(self, query: str) -> str:
        # Tool implementation
        return "News data"
```

### 3. API Connection Failures 

#### Symptoms
```
ConnectionError: Failed to connect to api.groq.com
TimeoutError: Request timed out after 30 seconds
```

#### Diagnostic Steps
```python
# Run environment test
python test_environment.py

# Check specific APIs
import requests

# Test Groq
response = requests.get("https://api.groq.com", timeout=10)
print(f"Groq Status: {response.status_code}")

# Test Exa
response = requests.get("https://api.exa.ai", timeout=10)
print(f"Exa Status: {response.status_code}")
```

#### Solutions
1. **Check Internet Connection**
2. **Verify Firewall Settings**
3. **Try Different Network**
4. **Use VPN if Geo-blocked**

### 4. Empty LLM Responses 

#### Symptoms
```
ValueError: Invalid response from LLM call - None or empty
```

#### Diagnostic Checklist
- [ ] API key is valid and has credits
- [ ] Not hitting rate limits
- [ ] Model name is correct
- [ ] Prompt is not too long
- [ ] Network connection is stable

#### Solutions
```python
# Test LLM directly
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="groq/llama-3.1-8b-instant",
    api_key="your_key",
    timeout=60  # Increase timeout
)

test_response = llm.invoke("Hello")
print(f"Response: {test_response.content}")
```

### 5. Module Import Errors 

#### Symptoms
```
ModuleNotFoundError: No module named 'crewai'
ImportError: cannot import name 'tool' from 'crewai.tools'
```

#### Solutions
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check versions
pip list | grep -E "(crewai|langchain|groq)"

# Reinstall if needed
pip uninstall crewai langchain-groq
pip install crewai langchain-groq
```

##  Diagnostic Tools

### System Health Check
```python
def system_health_check():
    """Comprehensive system health check."""
    checks = {
        "Python Version": sys.version_info >= (3, 10),
        "Memory Available": psutil.virtual_memory().available > 1024**3,
        "Disk Space": psutil.disk_usage('.').free > 1024**3,
        "Network": test_network_connectivity(),
        "API Keys": test_api_keys()
    }
    
    for check, status in checks.items():
        print(f"{check}: {'✅' if status else '❌'}")
    
    return all(checks.values())
```

### API Response Time Testing
```python
import time
import requests

def benchmark_apis():
    """Benchmark API response times."""
    apis = {
        "Groq": "https://api.groq.com",
        "Exa": "https://api.exa.ai",
        "Alpha Vantage": "https://www.alphavantage.co"
    }
    
    results = {}
    for name, url in apis.items():
        start = time.time()
        try:
            response = requests.get(url, timeout=10)
            duration = time.time() - start
            results[name] = {
                "time": f"{duration:.2f}s",
                "status": response.status_code
            }
        except Exception as e:
            results[name] = {"error": str(e)}
    
    return results
```

##  Additional Resources

### Documentation Links
- [CrewAI Documentation](https://docs.crewai.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [Exa API Reference](https://docs.exa.ai/)
- [Alpha Vantage Docs](https://www.alphavantage.co/documentation/)

---
