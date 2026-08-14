import os
from urllib.parse import urlparse

import psycopg
from dotenv import load_dotenv
from flask import (
	Flask,
	abort,
	flash,
	g,
	redirect,
	render_template,
	request,
	url_for,
)

from .analyzer import analyze_page
from .url_repository import UrlRepository
from .validator import validate_url

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")


def get_repo():
	if "db" not in g:
		g.db = psycopg.connect(
			app.config["DATABASE_URL"],
			autocommit=True,
		)

	return UrlRepository(g.db)


@app.teardown_appcontext
def close_db(_error):
	connection = g.pop("db", None)

	if connection is not None:
		connection.close()


@app.route("/")
def index():
	return render_template("index.html")


@app.get("/urls")
def urls_index():
	repo = get_repo()
	urls = repo.get_urls()
	return render_template("urls/index.html", urls=urls)


@app.post("/urls")
def urls_post():
	url = request.form.get("url", "").strip()
	error = validate_url(url)

	if error:
		flash(error, "danger")
		return render_template("index.html", url=url), 422

	normalized_url = _normalize_url(url)
	repo = get_repo()
	existing_url = repo.find_url_by_name(normalized_url)
	if existing_url:
		flash("Страница уже существует", "info")
		return redirect(url_for("urls_show", id=existing_url["id"]))

	try:
		id = repo.create_url({"name": normalized_url})

	except psycopg.errors.UniqueViolation:
		existing_url = repo.find_url_by_name(normalized_url)

		if existing_url:
			flash("Страница уже существует", "info")
			return redirect(url_for("urls_show", id=existing_url["id"]))

		raise

	except psycopg.Error:
		app.logger.exception("Failed to create URL")
		flash("Не удалось добавить страницу", "danger")
		return render_template("index.html", url=url), 500

	flash("Страница успешно добавлена", "success")
	return redirect(url_for("urls_show", id=id))


@app.get("/urls/<int:id>")
def urls_show(id):
	repo = get_repo()
	url = repo.find_url(id)

	if not url:
		abort(404)

	checks = repo.find_checks(id)

	return render_template("urls/show.html", url=url, checks=checks)


@app.post("/urls/<int:id>/checks")
def urls_checks_post(id):
	repo = get_repo()
	url_data = repo.find_url(id)

	if not url_data:
		abort(404)

	try:
		check_data = analyze_page(url_data)
		repo.create_check(check_data)
		flash("Страница успешно проверена", "success")
		return redirect(url_for("urls_show", id=id))

	except ValueError as error:
		flash(str(error), "danger")
		return redirect(url_for("urls_show", id=id))

	except psycopg.Error:
		app.logger.exception("Failed to create URL check")
		flash("Не удалось сохранить результат проверки", "danger")
		return redirect(url_for("urls_show", id=id))


def _normalize_url(url):
	parsed = urlparse(url)

	return f"{parsed.scheme}://{parsed.netloc}"
