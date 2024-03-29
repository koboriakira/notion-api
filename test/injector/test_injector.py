from unittest import TestCase

from notion_api.injector.injector import Injector


class TestInjector(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_CreateTagToZettlekastenUseCase(self):
        actual = Injector.get_create_tag_to_zettlekasten_use_case()
        self.assertIsNotNone(actual)
