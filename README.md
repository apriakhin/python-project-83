### Hexlet tests and linter status:

[![Actions Status](https://github.com/apriakhin/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/apriakhin/python-project-83/actions)
[![CI Status](https://github.com/apriakhin/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/apriakhin/python-project-83/actions)

# Page Analyzer

Page Analyzer is a Flask web application that checks web pages for basic SEO
elements. It stores submitted URLs in PostgreSQL and records the response code,
page title, heading, and description for every check.

The deployed application is available at
[python-project-83-02yt.onrender.com](https://python-project-83-02yt.onrender.com).

## Install

Python 3.13, [uv](https://docs.astral.sh/uv/), and PostgreSQL are required.

Copy and run the commands below in the terminal:

```sh
git clone https://github.com/apriakhin/python-project-83.git
cd python-project-83
make install
```

Set the required environment variables:

```sh
export SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://user:password@localhost:5432/page_analyzer
```

Create the database tables and start the development server:

```sh
psql -d "$DATABASE_URL" -f database.sql
make dev
```

## Usage

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser and submit a
web page URL. Open the saved URL and click **Запустить проверку** to retrieve
its HTTP status code and SEO metadata.
