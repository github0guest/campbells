from datetime import date
import unittest
from storage import ComicManager
from exceptions import NonexistentComicException


class TestCharacters(unittest.TestCase):
    def setUp(self):
        self.cm = ComicManager()

    def test_search_transcripts(self):
        self.assertEqual(self.cm.search_transcripts("skeeter falls"),
                         [date(1996, 8, 12), date(1996, 8, 15), date(1996, 8, 16), date(1996, 8, 24)])

    # def test_search_transcripts_special_characters(self):
    #     self.assertEquals(self.cm.search_transcripts("''"), '')
    #     self.assertEquals(self.cm.search_transcripts("{}"), '')

    def test_get_next_comic(self):
        self.assertEqual(self.cm.get_next_comic('1988-08-13'), date(1988, 8, 15))

    def test_get_next_comic_last_comic(self):
        with self.assertRaises(NonexistentComicException):
            self.cm.get_next_comic('3020-01-01')

    def test_get_previous_comic(self):
        self.assertEqual(self.cm.get_previous_comic('1988-08-15'), date(1988, 8, 13))

    def test_get_previous_comic_first_comic(self):
        with self.assertRaises(NonexistentComicException):
            self.cm.get_previous_comic('1988-04-11')


if __name__ == '__main__':
    unittest.main()
