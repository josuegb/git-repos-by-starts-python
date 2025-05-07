import unittest
from unittest.mock import patch, Mock

from repos.exceptions import GitHubApiError
from repos.api import create_query, repos_with_most_stars
from repos.models import GitHubRepo


class TestGitHubApiError(unittest.TestCase):
    def test_rate_limit_error(self):
        error = GitHubApiError(403)
        self.assertEqual(str(error), "Rate limit reached.")

    def test_other_error(self):
        error = GitHubApiError(404)
        self.assertEqual(str(error), "Status code was: 404")


class TestCreateQuery(unittest.TestCase):
    def test_create_query(self):
        query = create_query(["python", "javascript"], 50000)
        self.assertEqual(query, "stars:>50000 language:python language:javascript ")


class TestReposWithMostStars(unittest.TestCase):
    @patch("repos.api.requests.get")
    def test_repos_with_most_stars_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "language": "Python",
                    "name": "awesome-python",
                    "stargazers_count": 100000,
                },
                {
                    "language": "JavaScript",
                    "name": "freeCodeCamp",
                    "stargazers_count": 350000,
                },
            ]
        }
        mock_get.return_value = mock_response

        result = repos_with_most_stars(["Python", "JavaScript"], min_stars=50000)
        expected = [
            GitHubRepo("Python", "awesome-python", 100000),
            GitHubRepo("JavaScript", "freeCodeCamp", 350000),
        ]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].language, expected[0].language)
        self.assertEqual(result[0].name, expected[0].name)
        self.assertEqual(result[0].num_stars, expected[0].num_stars)
        self.assertEqual(result[1].language, expected[1].language)
        self.assertEqual(result[1].name, expected[1].name)
        self.assertEqual(result[1].num_stars, expected[1].num_stars)

    @patch("repos.api.requests.get")
    def test_repos_with_most_stars_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        with self.assertRaises(GitHubApiError) as context:
            repos_with_most_stars(["Python"], min_stars=50000)
        self.assertEqual(str(context.exception), "Rate limit reached.")


if __name__ == "__main__":
    unittest.main()
