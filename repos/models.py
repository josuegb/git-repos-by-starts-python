class GitHubRepo:
    def __init__(self, language, name, num_stars):
        self.language = language
        self.name = name
        self.num_stars = num_stars

    def __str__(self):
        return f"Language: {self.language}, Name: {self.name}, Stars: {self.num_stars}."

    def __repr__(self):
        return f"GitHubRepo(language={self.language}, name={self.name}, num_stars={self.num_stars})"
