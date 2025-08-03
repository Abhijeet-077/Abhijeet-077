#!/usr/bin/env python3
import os
import requests
from datetime import datetime

def get_recent_repositories(headers, username, limit=5):
    """Get recent repositories with details"""
    repos_url = f'https://api.github.com/users/{username}/repos'
    params = {'sort': 'updated', 'per_page': limit, 'type': 'owner'}

    try:
        response = requests.get(repos_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching repositories: {e}")
    return []

def main():
    # Get environment variables
    token = os.environ.get('GITHUB_TOKEN')
    username = os.environ.get('GITHUB_ACTOR')

    print(f"Username: {username}")

    if not token or not username:
        print("Error: Missing environment variables")
        return

    # Get user data from GitHub API
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/users/{username}'

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Get recent repositories
            recent_repos = get_recent_repositories(headers, username, 5)

            # Create repository showcase
            repo_showcase = ""
            if recent_repos:
                repo_showcase = "\n### 🚀 Recent Projects\n"
                for repo in recent_repos[:3]:  # Show top 3 recent repos
                    repo_name = repo.get('name', 'Unknown')
                    repo_desc = repo.get('description', 'No description available')[:100]
                    repo_url = repo.get('html_url', '#')
                    repo_lang = repo.get('language', 'Unknown')
                    updated = repo.get('updated_at', '')[:10]  # Get date only

                    repo_showcase += f"- **[{repo_name}]({repo_url})** ({repo_lang}) - {repo_desc}{'...' if len(repo.get('description', '')) > 100 else ''} *Updated: {updated}*\n"

            # Create stats section
            stats_section = f"""<!-- GITHUB-STATS:START -->
## 📊 GitHub Statistics

### Quick Stats
- 📝 **{data.get('public_repos', 0)}** Public Repositories
- ⭐ **{data.get('public_repos', 0)}** Total Repositories
- 👥 **{data.get('followers', 0)}** Followers
- 👤 **{data.get('following', 0)}** Following
{repo_showcase}
### 🐍 Contribution Snake
<div align="center">
  <img src="github-contribution-grid-snake.svg" alt="Snake animation" />
</div>

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*
<!-- GITHUB-STATS:END -->"""
            
            # Read README
            try:
                with open('README.md', 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                content = f"# {username}'s GitHub Profile\n\nWelcome to my profile!\n\n"
            
            # Update README
            import re
            pattern = r'<!-- GITHUB-STATS:START -->.*?<!-- GITHUB-STATS:END -->'
            
            if re.search(pattern, content, re.DOTALL):
                updated_content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
            else:
                updated_content = content + "\n\n" + stats_section
            
            # Write updated README
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ README updated successfully!")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
