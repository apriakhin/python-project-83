import validators


def validate_url(url):
	if not url:
		return "URL не должен быть пустым"

	if len(url) > 255:
		return "URL не должен превышать 255 символов"

	if not validators.url(url):
		return "Некорректный URL"

	return None
