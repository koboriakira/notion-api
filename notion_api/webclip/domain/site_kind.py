from enum import Enum


class SiteKind(Enum):
    TWITTER = "twitter.com"
    DEFAULT = "_"

    @staticmethod
    def find_site_kind(url: str) -> "SiteKind":
        for site_kind in SiteKind:
            if site_kind == SiteKind.DEFAULT:
                continue
            if site_kind.value in url:
                return site_kind
        return SiteKind.DEFAULT
