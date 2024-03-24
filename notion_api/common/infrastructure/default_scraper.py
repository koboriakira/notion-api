import trafilatura
from bs4 import BeautifulSoup

from common.domain.scraped_result import OgpTags, OtherMetaTags, ScrapedResult


class ScrapeError(Exception):
    pass


class DefaultScraper:
    """シンプルなスクレイピング"""

    def execute(self, url: str) -> ScrapedResult:
        """指定したURLのページをスクレイピングする """
        data = trafilatura.fetch_url(url)

        # とりあえずテキストをいい感じに抜き出す
        formatted_text = trafilatura.extract(data, include_formatting=True)
        not_formatted_text = trafilatura.extract(data, include_formatting=False)
        if not formatted_text:
            msg = "No content found"
            raise ScrapeError(msg)

        # BeautifulSoupでメタタグを取得
        soup = BeautifulSoup(data, features="html.parser")
        ogp_tags = {}
        other_meta_tags = {}
        for property_tag in soup.find_all("meta", attrs={"property": True}):
            key:str = property_tag["property"]
            value:str = property_tag["content"]
            if key.startswith("og:"):
                ogp_tags[key[3:]] = value
            else:
                other_meta_tags[key] = value

        for name_tag in soup.find_all("meta", attrs={"name": True}):
            key:str = name_tag["name"]
            value:str = name_tag["content"]
            other_meta_tags[key] = value

        return ScrapedResult(
            not_formatted_text=not_formatted_text,
            formatted_text=formatted_text,
            ogp_tags=OgpTags(values=ogp_tags),
            other_meta_tags=OtherMetaTags(values=other_meta_tags),
        )



if __name__ == "__main__":
    # python -m notion_api.usecase.service.simple_scraper
    scraper = DefaultScraper()
    print(scraper.handle("https://tabelog.com/tokyo/A1317/A131703/13253095/"))
