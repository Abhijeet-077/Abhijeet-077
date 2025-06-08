#!/usr/bin/env python3
"""
Simple Debug Version - Test Basic Functionality
"""

import os
import requests
from datetime import datetime

def main():
    print("🔍 Starting debug script...")
    
    # Check environment variables
    token = os.environ.get('GITHUB_TOKEN')
    username = os.environ.get('GITHUB_ACTOR')
    
    print(f"📝 Username: {username}")
    print(f"🔑 Token exists: {'Yes' if token else 'No'}")
    
    if not token or not username:
        print("❌ Missing environment variables!")
        return
    
    # Test API access
    try:
        headers = {'Authorization': f'token {token}'}
        url = f'https://api.github.com/users/{username}'
        
        print(f"🌐 Testing API call to: {url}")
        response = requests.get(url, headers=headers)
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Success! Public repos: {data.get('public_repos', 'N/A')}")
            
            # Simple README update
            stats_text = f"""<!-- GITHUB-STATS:START -->
## 📊 GitHub Stats (Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

- 📝 Public Repositories: {data.get('public_repos', 0)}
- 👥 Followers: {data.get('followers', 0)}
- 👤 Following: {data.get('following', 0)}

<!-- GITHUB-STATS:END -->"""
            
            # Read existing README or create new one
            try:
                with open('README.md', 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                content = f"# {username}'s Profile\n\n"
            
            # Simple replacement
            import re
            pattern = r'<!-- GITHUB-STATS:START -->.*?<!-- GITHUB-STATS:END -->'
            
            if re.search(pattern, content, re.DOTALL):
                updated_content = re.sub(pattern, stats_text, content, flags=re.DOTALL)
            else:
                updated_content = content + "\n\n" + stats_text
            
            # Write updated README
            with open('README.md', 'w') as f:
                f.write(updated_content)
            
            print("✅ README updated successfully!")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()