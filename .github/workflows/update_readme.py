#!/usr/bin/env python3
"""
Enhanced README Profile Stats Updater
Automatically updates README.md with GitHub profile statistics
"""

import os
import re
import requests
from datetime import datetime
from typing import Dict, List, Optional

class GitHubStatsUpdater:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.username = os.environ.get('GITHUB_ACTOR')
        self.repo = os.environ.get('GITHUB_REPOSITORY', '').split('/')[-1]
        
        if not all([self.token, self.username]):
            raise ValueError("Missing required environment variables")
            
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def fetch_github_stats(self) -> Dict:
        """Fetch comprehensive GitHub statistics"""
        print(f"🔍 Fetching stats for {self.username}...")
        
        # User profile data
        user_url = f'https://api.github.com/users/{self.username}'
        user_response = requests.get(user_url, headers=self.headers)
        user_data = user_response.json()
        
        # Repository data
        repos_url = f'https://api.github.com/users/{self.username}/repos?per_page=100'
        repos_response = requests.get(repos_url, headers=self.headers)
        repos_data = repos_response.json()
        
        # Calculate statistics
        stats = {
            'total_repos': len(repos_data),
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'total_stars': sum(repo.get('stargazers_count', 0) for repo in repos_data),
            'total_forks': sum(repo.get('forks_count', 0) for repo in repos_data),
            'languages': self.get_top_languages(repos_data),
            'most_starred_repo': max(repos_data, key=lambda x: x.get('stargazers_count', 0), default={}),
            'recent_activity': self.get_recent_activity(),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        
        return stats
    
    def get_top_languages(self, repos_data: List[Dict]) -> List[str]:
        """Get top programming languages from repositories"""
        languages = {}
        
        for repo in repos_data:
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
                
        # Sort by frequency and return top 5
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        return [lang[0] for lang in sorted_langs[:5]]
    
    def get_recent_activity(self) -> int:
        """Get recent commit activity (last 30 days)"""
        try:
            events_url = f'https://api.github.com/users/{self.username}/events?per_page=100'
            events_response = requests.get(events_url, headers=self.headers)
            events_data = events_response.json()
            
            # Count push events in the last 30 days
            from datetime import datetime, timedelta
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            recent_commits = 0
            for event in events_data:
                if event.get('type') == 'PushEvent':
                    event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    if event_date > thirty_days_ago:
                        recent_commits += len(event.get('payload', {}).get('commits', []))
                        
            return recent_commits
        except:
            return 0
    
    def generate_stats_section(self, stats: Dict) -> str:
        """Generate the stats section for README"""
        languages_str = " • ".join(stats['languages'][:3]) if stats['languages'] else "Various"
        
        most_starred = stats['most_starred_repo']
        starred_repo_info = f"[{most_starred.get('name', 'N/A')}]({most_starred.get('html_url', '#')}) ⭐ {most_starred.get('stargazers_count', 0)}" if most_starred else "None"
        
        stats_section = f"""<!-- GITHUB-STATS:START -->
## 📊 GitHub Statistics

<div align="center">
  
![Profile Views](https://komarev.com/ghpvc/?username={self.username}&color=blue&style=flat-square)
![GitHub followers](https://img.shields.io/github/followers/{self.username}?style=flat-square&color=blue)
![GitHub stars](https://img.shields.io/github/stars/{self.username}?affiliations=OWNER&style=flat-square&color=yellow)

</div>

### 🔥 Quick Stats
- 📝 **{stats['public_repos']}** Public Repositories
- ⭐ **{stats['total_stars']}** Total Stars Earned  
- 🍴 **{stats['total_forks']}** Total Forks
- 👥 **{stats['followers']}** Followers | **{stats['following']}** Following
- 💻 **{stats['recent_activity']}** Commits (Last 30 days)

### 🚀 Top Languages
**{languages_str}**

### 🏆 Most Starred Repository
{starred_repo_info}

---
<div align="center">
  
[![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user={self.Abhijeet-077}&theme=dark)](https://git.io/streak-stats)

</div>

*Last updated: {stats['last_updated']}*
<!-- GITHUB-STATS:END -->"""
        
        return stats_section
    
    def update_readme(self):
        """Update README.md file with latest stats"""
        readme_path = 'README.md'
        
        # Read current README
        try:
            with open(readme_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("📄 README.md not found, creating new one...")
            content = f"# {self.username}'s GitHub Profile\n\nWelcome to my GitHub profile!\n\n"
        
        # Fetch latest stats
        stats = self.fetch_github_stats()
        new_stats_section = self.generate_stats_section(stats)
        
        # Replace stats section
        pattern = r'<!-- GITHUB-STATS:START -->.*?<!-- GITHUB-STATS:END -->'
        
        if re.search(pattern, content, re.DOTALL):
            # Replace existing stats section
            updated_content = re.sub(pattern, new_stats_section, content, flags=re.DOTALL)
            print("🔄 Updated existing stats section")
        else:
            # Append stats section
            updated_content = content + "\n\n" + new_stats_section
            print("➕ Added new stats section")
        
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print("✅ README.md updated successfully!")
        print(f"📊 Stats: {stats['total_stars']} stars, {stats['public_repos']} repos, {stats['followers']} followers")

def main():
    try:
        updater = GitHubStatsUpdater()
        updater.update_readme()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()