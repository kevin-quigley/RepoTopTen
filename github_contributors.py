import requests
import configparser
import re

def get_top_contributors(repo_urls, access_token):
    for repo_url in repo_urls:
        # Extract owner and repo name from the repository URL
        match = re.match(r"https://github\.com/([^/]+)/([^/]+)", repo_url)
        if match:
            owner, repo = match.groups()
            repo_name = f"{owner}/{repo}"
        else:
            # Handle case where pattern does not match
            print(f"Invalid repository URL format: {repo_url}")
            continue  # Skip processing this repository

        # Fetch contributors for the repository using GitHub API
        url = f"https://api.github.com/repos/{repo_name}/contributors"
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            contributors_data = response.json()

            # Print the top 10 contributors for the current repository
            print(f"\nTop 10 Contributors for {repo_name}:")
            for i, contributor in enumerate(contributors_data[:10], start=1):
                print(f"{i}. {contributor['login']}: {contributor['contributions']} contributions")
        else:
            print(f"Failed to fetch contributors for {repo_name}. Status code: {response.status_code}")

if __name__ == "__main__":
    # Read configuration from config.ini file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Get GitHub access token from config.ini file
    access_token = config.get("github", "access_token")

    # Input GitHub repository URLs (comma-separated)
    repo_urls_input = input("Enter GitHub repository URLs (comma-separated): ")
    repo_urls = [url.strip() for url in repo_urls_input.split(",")]

    # Call the function to get top contributors for each repository
    get_top_contributors(repo_urls, access_token)
