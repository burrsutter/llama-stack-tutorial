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

BRAVE_SEARCH_API_KEY=os.getenv("BRAVE_SEARCH_API_KEY")

# Retrieve your API key from the environment
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
if not BRAVE_SEARCH_API_KEY:
    raise ValueError("Please set the BRAVE_SEARCH_API_KEY environment variable.")

# Define the API endpoint URL (update this as needed according to your API docs)
API_URL = "https://api.search.brave.com/res/v1/web/search"

# Define the search parameters
params = {
    "q": "hello world",  # The search query
    "count": 5
}

# Set up the headers including the API key 
headers = {
    "Accept": "application/json",
    "X-Subscription-Token": BRAVE_SEARCH_API_KEY
}

# Make the GET request
response = requests.get(API_URL, headers=headers, params=params)

# Check for a successful response and print the results
if response.status_code == 200:
    results = response.json()
    print(f"Search results for 'hello world': ")
    for i, result in enumerate(results.get("web", {}).get("results", []), 1):
        print(f"{i}. {result.get('title')}")
        print(f"   {result.get('url')}")
        print(f"   {result.get('description')}\n")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
