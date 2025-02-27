import requests

options = {
    'url': 'http://localhost:8080/health',
    'method': 'GET',
    'timeout': 2000
}

def check():
    try:
        r = requests.request(
            "GET",
            "http://localhost:8080/health",
            timeout=2
        )
        if r.status_code == 200:
            if r.text == "0":
                return True
            return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    exit(0 if check() else 1)