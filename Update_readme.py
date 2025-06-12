#!/usr/bin/env python3
import os
import requests
from datetime import datetime

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
            
            # Create stats section
            stats_section = f"""<!-- GITHUB-STATS:START -->
## 📊 GitHub Statistics

### Quick Stats
- 📝 **{data.get('public_repos', 0)}** Public Repositories
- ⭐ **{data.get('public_repos', 0)}** Total Repositories  
- 👥 **{data.get('followers', 0)}** Followers
- 👤 **{data.get('following', 0)}** Following

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
