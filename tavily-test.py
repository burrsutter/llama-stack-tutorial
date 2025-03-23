from dotenv import load_dotenv
import logging
import os
import requests

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

TAVILY_SEARCH_API_KEY=os.getenv("TAVILY_SEARCH_API_KEY")

# Retrieve your API key from the environment
TAVILY_SEARCH_API_KEY = os.getenv("TAVILY_SEARCH_API_KEY")
if not TAVILY_SEARCH_API_KEY:
    raise ValueError("Please set the TAVILY_SEARCH_API_KEY environment variable.")

# Define the API endpoint URL (update this as needed according to your API docs)
API_URL = "https://api.tavily.com/search"

# Define the search parameters
params = {
    "query": "hello world",  # The search query
    "max_results": 3           # Number of results to return
}

# Set up the headers including the API key (assuming Bearer token auth)
headers = {
    "Authorization": f"Bearer {TAVILY_SEARCH_API_KEY}",
    "Content-Type": "application/json"
}

# Make the GET request
response = requests.post(API_URL, headers=headers, json=params)

# Check for a successful response and print the results
if response.status_code == 200:
    results = response.json()
    print("Search results for 'hello world':")
    for result in results.get("results", []):
        print(f"Title: {result.get('title')}")
        print(f"URL: {result.get('url')}")
        print("-----")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
