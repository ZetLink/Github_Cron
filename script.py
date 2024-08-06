import requests
import datetime
import subprocess
import os

GITHUB_REPOS = [
    {'name': 'repository1', 'local_path': '/path1'},
    {'name': 'repository2', 'local_path': '/path2'}
]
TELEGRAM_TOKEN = {TELEGRAM_BOT_TOEKEN}
CHAT_ID = {CHAT_ID}

def get_commits_on_date(repo, date):
    url = f'https://api.github.com/repos/{repo}/commits'
    params = {
        'since': date.isoformat() + 'T00:00:00Z',
        'until': date.isoformat() + 'T23:59:59Z'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching commits for {repo}: {response.status_code}")
    return []

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.status_code}")

def fetch_and_cherrypick(local_path, commit_shas):
    try:
        os.chdir(local_path)
        
        subprocess.run(['git', 'fetch'], check=True)

        for sha in commit_shas:
            subprocess.run(['git', 'cherry-pick', sha], check=True)
        
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error en fetch o cherry-pick: {e}")
        return False

def main():
    today = datetime.datetime.now(datetime.timezone.utc).date()

    for repo_info in GITHUB_REPOS:
        repo = repo_info['name']
        local_path = repo_info['local_path']
        commit_messages = []
        commits = get_commits_on_date(repo, today)

        if commits:
            commit_messages.append(f"Se realizaron los siguientes commits hoy en *{repo}:*")
            commit_shas = []
            for commit in commits:
                author = commit['commit']['author']['name']
                message = commit['commit']['message']
                url = commit['html_url']
                sha = commit['sha']
                commit_shas.append(sha)
                commit_messages.append(f"- {author}: {message}\n{url}")
            
            if repo == 'repository1':
                if fetch_and_cherrypick(local_path, commit_shas):
                    commit_messages.append("Los commits han sido aplicados correctamente en DanceKernel.")
                else:
                    commit_messages.append("Error al aplicar los commits con cherry-pick en DanceKernel.")
        
        else:
            commit_messages.append(f"No se realizaron commits hoy en el repositorio *{repo}*")

        send_telegram_message("\n".join(commit_messages))

if __name__ == '__main__':
    main()
