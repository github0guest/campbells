import unittest
from characters import characters_from_date


class TestCharacters(unittest.TestCase):

    def test_characters_from_date(self):
        self.assertEqual(characters_from_date("1988-08-03"), ['Jason', 'punishment', 'Roger'])


if __name__ == '__main__':
    unittest.main()