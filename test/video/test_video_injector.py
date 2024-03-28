from unittest import TestCase

from notion_api.video.video_injector import VideoInjector


class TestVideoInjector(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_video関連のinjector(self):
        self.assertIsNotNone(VideoInjector.create_video_creator())
