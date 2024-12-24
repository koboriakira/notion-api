from github import Auth, Github
from lotion.lotion import os


class GitHubService:
    def __init__(self, github_access_token: str | None = None) -> None:
        access_token = os.environ["GITHUB_ACCESS_TOKEN"] if github_access_token is None else github_access_token
        auth = Auth.Token(access_token)
        self._pygithub = Github(auth=auth)

    def get_repos(self):
        # Then play with your Github objects:
        for repo in self._pygithub.get_user().get_repos():
            print(repo.name)


if __name__ == "__main__":
    service = GitHubService()
    service.get_repos()
