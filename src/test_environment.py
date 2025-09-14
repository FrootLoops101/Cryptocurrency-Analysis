import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")

    required_packages = {
        'requests': 'requests',
        'pandas': 'pandas', 
        'crewai': 'crewai',
        'crewai.tools': 'crewai-tools',
        'langchain_groq': 'langchain-groq',
        'exa_py': 'exa-py',
        'os': 'built-in',
        'datetime': 'built-in'
    }

    missing_packages = []

    for package, install_name in required_packages.items():
        try:
            importlib.import_module(package)
            print(f" {package} - OK")
        except ImportError:
            print(f" {package} - MISSING (install with: pip install {install_name})")
            missing_packages.append(install_name)

    if missing_packages:
        print(f"\nMissing packages detected. Install with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    print("\n All required packages are available!")
    return True

def test_api_keys():
    """Test API key availability"""
    print("\nTesting API keys...")

    import os

    # Check GROQ API key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print(" GROQ_API_KEY - Found in environment")
    else:
        print("  GROQ_API_KEY - Not found in environment (will prompt during execution)")

    # Note: Exa API key is hardcoded in the original script
    print(" Exa API key - Hardcoded in script")
    print(" Alpha Vantage API key - Hardcoded in script")

    return True

def test_network_connectivity():
    """Test network connectivity to APIs"""
    print("\nTesting network connectivity...")

    import requests

    test_urls = {
        "Groq API": "https://api.groq.com",
        "Alpha Vantage": "https://www.alphavantage.co",
        "Exa API": "https://api.exa.ai"
    }

    all_good = True

    for name, url in test_urls.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:  # Any response except server errors
                print(f" {name} - Accessible (Status: {response.status_code})")
            else:
                print(f"  {name} - Server error (Status: {response.status_code})")
                all_good = False
        except requests.exceptions.RequestException as e:
            print(f" {name} - Connection failed ({str(e)[:50]}...)")
            all_good = False

    return all_good

def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")

    try:
        # Test pandas
        import pandas as pd
        df = pd.DataFrame({"test": [1, 2, 3]})
        print(" Pandas - DataFrame creation works")

        # Test requests
        import requests
        response = requests.get("https://httpbin.org/json", timeout=5)
        if response.status_code == 200:
            print(" Requests - HTTP requests work")
        else:
            print("  Requests - HTTP request returned unexpected status")

        # Test datetime
        from datetime import datetime
        now = datetime.now()
        print(f" Datetime - Current time: {now.strftime('%Y-%m-%d %H:%M')}")

        return True

    except Exception as e:
        print(f" Basic functionality test failed: {e}")
        return False

def test_crewai_basic():
    """Test basic CrewAI functionality"""
    print("\nTesting CrewAI basic setup...")

    try:
        from crewai import Agent, Task, Crew
        from crewai.tools import tool
        print(" CrewAI imports successful")

        # Test tool creation
        @tool("test_tool")
        def test_tool_func(input_text: str) -> str:
            """A simple test tool"""
            return f"Tool received: {input_text}"

        print(" CrewAI tool creation works")

        return True

    except Exception as e:
        print(f" CrewAI basic test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("CRYPTOCURRENCY ANALYSIS - ENVIRONMENT TEST")
    print("="*60)

    tests = [
        ("Package Imports", test_imports),
        ("API Keys", test_api_keys), 
        ("Network Connectivity", test_network_connectivity),
        ("Basic Functionality", test_basic_functionality),
        ("CrewAI Setup", test_crewai_basic)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'-'*40}")
        print(f"Running: {test_name}")
        print(f"{'-'*40}")

        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f" Test failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = " PASS" if result else " FAIL"
        print(f"{test_name:<25} {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n All tests passed! Your environment is ready for cryptocurrency analysis.")
        print("\nNext steps:")
        print("1. Run the fixed cryptocurrency analysis script")  
        print("2. Make sure to set GROQ_API_KEY environment variable or be ready to enter it")
        print("3. Check the output for the analysis results")
    else:
        print(f"\n  {total - passed} test(s) failed. Please address the issues above before running the main script.")
        print("\nCommon fixes:")
        print("- Install missing packages with pip")
        print("- Check your internet connection") 
        print("- Set up API keys properly")

if __name__ == "__main__":
    main()
