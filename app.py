import os
import time
import jwt
import requests
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# Ortam değişkenlerinden bilgileri al
APP_ID = os.getenv("APP_ID")
INSTALLATION_ID = os.getenv("INSTALLATION_ID")
REPO = os.getenv("REPO")

# Özel anahtarı dosyadan oku
with open("private-key.pem", "r") as key_file:
    PRIVATE_KEY = key_file.read()

def generate_jwt():
    """JWT oluştur."""
    payload = {
        "iat": int(time.time()),  # Şimdiki zaman
        "exp": int(time.time()) + (10 * 60),  # 10 dakika geçerli
        "iss": APP_ID,  # App ID
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def get_installation_access_token(installation_id):
    """GitHub API'den erişim token al."""
    jwt_token = generate_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()["token"]

# GitHub'da issue oluşturma
def create_github_issue():
    access_token = get_installation_access_token(INSTALLATION_ID)
    headers = {"Authorization": f"token {access_token}"}
    issue_data = {"title": "Demo Issue", "body": "This is a demo issue created by the GitHub App."}
    response = requests.post(
        f"https://api.github.com/repos/{REPO}/issues",
        json=issue_data,
        headers=headers,
    )
    print(response.json())

if __name__ == "__main__":
    create_github_issue()
