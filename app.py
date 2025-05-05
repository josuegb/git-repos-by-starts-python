from flask import Flask, render_template, request
from repos.api import repos_with_most_stars
from repos.exceptions import GitHubApiError

LANGUAGES = ["Python", "JavaScript", "C++"]

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        selected_languages = LANGUAGES
    elif request.method == "POST":
        selected_languages = request.form.getlist("languages")

    results = repos_with_most_stars(selected_languages)

    return render_template(
        "index.html",
        available_languages=LANGUAGES,
        selected_languages=selected_languages,
        results=results,
    )


@app.errorhandler(GitHubApiError)
def handle_api_error(error):
    return render_template("error.html", message=error)
