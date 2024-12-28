from unittest import TestCase

from notion_api.video.video_injector import VideoInjector

from video.service.video_creator import VideoCreator


class TestVideoInjector(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_video関連のinjector(self):
        suite = VideoInjector.create_video_creator()
        self.assertIsInstance(suite, VideoCreator)
