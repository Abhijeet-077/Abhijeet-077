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
    username = os.environ.get('GITHUB_ACTOR', 'Abhijeet-077')  # fallback to hardcoded username

    print(f"Username: {username}")
    print(f"Token available: {'Yes' if token else 'No'}")

    # Get user data from GitHub API
    url = f'https://api.github.com/users/{username}'
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    print(f"Making API request to: {url}")
    print(f"Headers: {headers}")

    try:
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully fetched user data for {username}")

            # Get recent repositories
            recent_repos = get_recent_repositories(headers, username, 5)

            # Create repository showcase
            repo_showcase = ""
            if recent_repos:
                repo_showcase = "\n### 🚀 Recent Projects\n"
                for repo in recent_repos[:3]:  # Show top 3 recent repos
                    repo_name = repo.get('name', 'Unknown')
                    description = repo.get('description') or 'No description available'
                    repo_desc = description[:100]
                    repo_url = repo.get('html_url', '#')
                    repo_lang = repo.get('language', 'Unknown')
                    updated = repo.get('updated_at', '')[:10]  # Get date only

                    repo_showcase += f"- **[{repo_name}]({repo_url})** ({repo_lang}) - {repo_desc}{'...' if len(description) > 100 else ''} *Updated: {updated}*\n"

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

            print(f"README content length: {len(content)}")
            print(f"Stats section length: {len(stats_section)}")
            print("Stats section content:")
            print(repr(stats_section[:200]))

            # Update README
            import re
            pattern = r'<!-- GITHUB-STATS:START -->.*?<!-- GITHUB-STATS:END -->'

            if re.search(pattern, content, re.DOTALL):
                print("✅ Found GitHub stats markers, updating content...")
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    print(f"Current content between markers: {repr(match.group()[:100])}")
                updated_content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
                print(f"Updated content length: {len(updated_content)}")
                print(f"Content changed: {len(updated_content) != len(content)}")
            else:
                print("⚠️ No GitHub stats markers found, appending content...")
                updated_content = content + "\n\n" + stats_section
            
            # Write updated README
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ README updated successfully!")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
