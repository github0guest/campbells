import unittest
import config
from storage import ComicManager, NonexistentComicException


class TestCharacters(unittest.TestCase):
    def setUp(self):
        self.cm = ComicManager(config.database, echo=False)

    def test_search_transcripts(self):
        self.assertEqual(self.cm.search_transcripts("skeeter falls"),
                         ['1996-08-12', '1996-08-15', '1996-08-16', '1996-08-24'])

    # def test_search_transcripts_special_characters(self):
    #     self.assertEquals(self.cm.search_transcripts("''"), '')
    #     self.assertEquals(self.cm.search_transcripts("{}"), '')

    def test_get_next_comic(self):
        self.assertEqual(self.cm.get_next_comic('1988-08-13'), '1988-08-15')

    def test_get_next_comic_last_comic(self):
        with self.assertRaises(NonexistentComicException):
            self.cm.get_next_comic('3020-01-01')

    def test_get_previous_comic(self):
        self.assertEqual(self.cm.get_previous_comic('1988-08-15'), '1988-08-13')

    def test_get_previous_comic_first_comic(self):
        with self.assertRaises(NonexistentComicException):
            self.cm.get_previous_comic('1988-04-11')


if __name__ == '__main__':
    unittest.main()
