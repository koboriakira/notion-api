from datetime import datetime, timedelta

from github import Auth, Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from lotion.lotion import os

from util.datetime import jst_now


class GitHubService:
    def __init__(self, github_access_token: str | None = None) -> None:
        access_token = os.environ["GITHUB_ACCESS_TOKEN"] if github_access_token is None else github_access_token
        auth = Auth.Token(access_token)
        self._pygithub = Github(auth=auth)

    def get_latest_merged_prs(self, target_datetime: datetime) -> dict[str, list[dict[str, str]]]:
        repos = self._get_repos()
        result = {}
        for repo in repos:
            updated_at = repo.updated_at
            if updated_at < target_datetime:
                continue
            latest_merged_prs = self._get_latest_merged_prs_as_repo(repo, target_datetime)
            if len(list(latest_merged_prs)) == 0:
                continue
            result[repo.name] = latest_merged_prs
        return result

    def _get_latest_merged_prs_as_repo(self, repo: Repository, target_datetime: datetime) -> list[dict[str, str]]:
        pull_requests = repo.get_pulls(state="merged")
        result = []
        for pull_request in pull_requests:
            merged_at = pull_request.merged_at
            if merged_at is not None and merged_at < target_datetime:
                continue
            result.append(
                {"title": pull_request.title, "url": pull_request.html_url},
            )
        return result

    def _get_repos(self) -> PaginatedList[Repository]:
        return self._pygithub.get_user().get_repos()


if __name__ == "__main__":
    # python -m notion_api.common.service.github.github_service
    service = GitHubService()
    print(service.get_latest_merged_prs(jst_now() - timedelta(days=1)))
