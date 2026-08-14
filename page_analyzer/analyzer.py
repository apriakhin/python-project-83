import requests


def anaylyze_page(url_data):
    try:
        response = requests.get(url_data["name"], timeout=10)
        response.raise_for_status()
        status_code = response.status_code

    except requests.RequestException:
        raise ValueError('Произошла ошибка при проверке')

    return {
        "url_id": url_data["id"], 
        "status_code": status_code, 
        "h1": None, 
        "title": None, 
        "description": None
    }
