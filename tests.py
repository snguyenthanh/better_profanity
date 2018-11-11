import unittest
from better_profanity import profanity


class ProfanityTest(unittest.TestCase):
    def test_contains_profanity(self):
        profane = profanity.contains_profanity('he is a m0th3rf*cker')
        self.assertTrue(profane)

    def test_leaves_paragraphs_untouched(self):
        innocent_text = """If you prick us do we not bleed?
                        If you tickle us do we not laugh?
                        If you poison us do we not die?
                        And if you wrong us shall we not revenge?"""
        censored_text = profanity.censor(innocent_text)
        self.assertTrue(innocent_text == censored_text)

    def test_censorship(self):
        bad_text = "Dude, I hate shit. Fuck bullshit."
        censored_text = profanity.censor(bad_text)
        # make sure it finds both instances
        self.assertFalse("shit" in censored_text)
        # make sure it's case sensitive
        self.assertFalse("fuck" in censored_text)
        # make sure some of the original text is still there
        self.assertTrue("Dude" in censored_text)

    def test_censorship_for_2_words(self):
        bad_text = "That wh0re gave m3 a very good H4nd j0b"
        censored_text = profanity.censor(bad_text)

        self.assertFalse("H4nd j0b" in censored_text)
        self.assertTrue("m3" in censored_text)
        
    def test_custom_wordlist(self):
        custom_badwords = ['happy', 'jolly', 'merry']
        profanity.load_censor_words(custom_badwords)
        # make sure it doesn't find real profanity anymore
        self.assertFalse(profanity.contains_profanity("Fuck you!"))
        # make sure it finds profanity in a sentence containing custom_badwords
        self.assertTrue(profanity.contains_profanity("Have a merry day! :)"))


if __name__ == "__main__":
    unittest.main()
