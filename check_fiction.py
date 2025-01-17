import requests

def is_fiction(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(url).json()
    for item in response.get('items', []):
        categories = item.get('volumeInfo', {}).get('categories', [])
        if any("Novel" in category for category in categories):
            return True
        if any("Poetry" in category or "Poems" in category for category in categories):
            return True
    return False

title = "무소유"
print(is_fiction(title))  # True면 소설, False면 비소설