import requests
from bs4 import BeautifulSoup


def analyze_page(url_data):
	try:
		response = requests.get(url_data["name"], timeout=10)
		response.raise_for_status()
		status_code = response.status_code
		soup = BeautifulSoup(response.text, "html.parser")

	except requests.RequestException:
		raise ValueError("Произошла ошибка при проверке")

	h1_tag = soup.find("h1")
	if h1_tag:
		h1 = _truncate(h1_tag.get_text(strip=True))

	else:
		h1 = None

	title_tag = soup.find("title")
	if title_tag:
		title = _truncate(title_tag.get_text(strip=True))

	else:
		title = None

	description_tag = soup.find("meta", attrs={"name": "description"})
	if description_tag:
		description = _truncate(description_tag.get("content", "").strip())

	else:
		description = None

	return {
		"url_id": url_data["id"],
		"status_code": status_code,
		"h1": h1,
		"title": title,
		"description": description,
	}


def _truncate(text, max_length=200):
	if len(text) <= max_length:
		return text

	return text[:max_length] + "..."
