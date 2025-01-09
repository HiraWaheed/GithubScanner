import os
import requests
import time
import csv
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

def create_github_query(language: str, date_range: tuple) -> str:
    """Create a GitHub search query for Java repos within a date range"""
    return f'language:{language} vulnerable created:{date_range[0]}..{date_range[1]} is:public'

def get_auth_headers(token: str) -> Dict:
    """Return headers with authentication"""
    return {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

def search_repositories(query: str, headers: Dict) -> List[Dict]:
    """Search GitHub repositories with pagination and rate limit handling"""
    base_url = 'https://api.github.com/search/repositories'
    repos = []
    page = 1
    
    while len(repos) < 100:
        params = {
            'q': query,
            'sort': 'updated',
            'order': 'desc',
            'per_page': 100,
            'page': page
        }
        
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            
            if response.status_code == 200:
                data = response.json()
                if not data['items']:
                    break
                    
                repos.extend(data['items'])
                
                # Handle rate limiting
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                if remaining == 0:
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    sleep_time = reset_time - time.time()
                    if sleep_time > 0:
                        print(f"Rate limit reached. Waiting {sleep_time:.2f} seconds...")
                        time.sleep(sleep_time + 1)
                
            page += 1
            time.sleep(2)  # Basic rate limiting
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            break
    
    return repos[:100]


def export_results(repos: List[Dict], filename: str):
    """Export results to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for repo in repos:
            writer.writerow([
                repo['html_url']
            ])

def main():

    github_token = os.getenv("GITHUB_TOKEN")
    
    # Search for repositories from 2015-2024
    date_range = ('2015-01-01', '2024-12-31')
    language = 'javascript'
    
    headers = get_auth_headers(github_token)

    print(f"Searching for potentially vulnerable {language} repositories...")
    repos = search_repositories(create_github_query(language, date_range), headers)
    
    # Export results
    export_results(repos, f'vulnerable_{language}_repos.csv')
    print(f"Results exported to vulnerable_{language}_repos.csv")
    
if __name__ == "__main__":
    main()