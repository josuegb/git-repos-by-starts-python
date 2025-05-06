import requests
from repos.exceptions import GitHubApiError
from repos.models import GitHubRepo

GITHUB_API_URL = "https://api.github.com/search/repositories"


def create_query(languages, min_stars):
    query = f"stars:>{min_stars} "

    for language in languages:
        query += f"language:{language} "

    # a sample query looks like: "stars:>50 language:python language:javascript"
    return query


def repos_with_most_stars(languages, min_stars=50000, sort="stars", order="desc"):
    query = create_query(languages, min_stars)
    params = {"q": query, "sort": sort, "order": order}

    response = requests.get(GITHUB_API_URL, params=params)
    status_code = response.status_code

    if status_code != 200:
        raise GitHubApiError(status_code)

    response_json = response.json()
    items = response_json["items"]
    git_repos = [
        GitHubRepo(item["language"], item["name"], item["stargazers_count"])
        for item in items
    ]
    return git_repos
