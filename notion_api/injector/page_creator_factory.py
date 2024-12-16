from logging import Logger

from common.service.page_creator import PageCreator
from common.value.site_kind import SiteKind
from music.infrastructure.song_repository_impl import SongRepositoryImpl
from music.service.music_creator import MusicCreator
from lotion import Lotion
from restaurant.infrastructure.restaurant_repository_impl import RestaurantRepositoryImpl
from restaurant.service.restaurant_creator import RestaurantCreator
from video.video_injector import VideoInjector
from webclip.injector import WebclipInjector


class PageCreatorFactory:
    def __init__(self, generator_dict: dict[SiteKind, PageCreator]) -> None:
        self.generator_dict = generator_dict

    @classmethod
    def generate_rule(cls: "PageCreatorFactory", logger: Logger) -> "PageCreatorFactory":
        client = Lotion.get_instance()
        webclip_creator = WebclipInjector.create_webclip_creator()
        video_creator = VideoInjector.create_video_creator()
        restaurant_repository = RestaurantRepositoryImpl(client=client)
        restaurant_creator = RestaurantCreator(restaurant_repository=restaurant_repository, logger=logger)
        song_repository = SongRepositoryImpl(client=client)
        music_creator = MusicCreator(song_repository=song_repository, logger=logger)

        generator_dict = {}
        for site_kind in SiteKind:
            match site_kind:
                case SiteKind.TABELOG:
                    generator_dict[site_kind] = restaurant_creator
                case SiteKind.YOUTUBE:
                    generator_dict[site_kind] = video_creator
                case SiteKind.SPOTIFY:
                    generator_dict[site_kind] = music_creator
                case _:
                    generator_dict[site_kind] = webclip_creator
        return PageCreatorFactory(generator_dict=generator_dict)

    def get_creator(self, site_kind: SiteKind) -> PageCreator:
        """任意のPageCreatorを取得する"""
        return self.generator_dict[site_kind]
