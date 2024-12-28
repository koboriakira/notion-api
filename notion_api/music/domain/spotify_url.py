from lotion import notion_prop
from lotion.properties import Url


@notion_prop("Spotify")
class SpotifyUrl(Url):
    def get_spotify_url(self) -> str:
        return self.url.split("?")[0]

    def get_spotify_track_id(self) -> str:
        # https://open.spotify.com/intl-ja/track/0VfOZBCILsIrkJPzw3WdvA?si=731d95eb095543ac からクエリを除いた部分
        return self.get_spotify_url().split("/")[-1].split("?")[0]

    def get_embed_html(self) -> str:
        spotify_track_id = self.get_spotify_track_id()
        text = f"""<iframe style="border-radius:12px"
 src="https://open.spotify.com/embed/track/{spotify_track_id}?utm_source=generator"
 width="100%" height="152"
 frameBorder="0"
 allowfullscreen=""
 allow="autoplay;
 clipboard-write;
 encrypted-media;
 fullscreen;
 picture-in-picture"
 loading="lazy">
</iframe>
"""
        return text.replace("\n", "")
