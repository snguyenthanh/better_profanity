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
        self.assertEqual(innocent_text, censored_text)

    def test_censorship_1(self):
        bad_text = "Dude, I hate shit. Fuck bullshit."
        censored_text = profanity.censor(bad_text)
        # make sure it finds both instances
        self.assertFalse("shit" in censored_text)
        # make sure it's case sensitive
        self.assertFalse("fuck" in censored_text)
        # make sure some of the original text is still there
        self.assertTrue("Dude" in censored_text)

    def test_censorship_2(self):
        bad_text = "That wh0re gave m3 a very good H4nd j0b, dude. You gotta check."
        censored_text = "That **** gave m3 a very good ****, dude. You gotta check."

        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_censorship_with_starting_swear_word(self):
        bad_text = "  wh0re gave m3 a very good H@nD j0b."
        censored_text = "  **** gave m3 a very good ****."

        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_censorship_with_ending_swear_word(self):
        bad_text = "That wh0re gave m3 a very good H@nD j0b."
        censored_text = "That **** gave m3 a very good ****."

        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_censorship_empty_text(self):
        empty_text = ""
        self.assertEqual(profanity.censor(empty_text), empty_text)

    def test_censorship_for_2_words(self):
        bad_text = "That wh0re gave m3 a very good H4nd j0b"
        censored_text = profanity.censor(bad_text)

        self.assertFalse("H4nd j0b" in censored_text)
        self.assertTrue("m3" in censored_text)

    def test_censorship_for_clean_text(self):
        clean_text = "Hi there"
        self.assertEqual(profanity.censor(clean_text), clean_text)

    def test_custom_wordlist(self):
        custom_badwords = ['happy', 'jolly', 'merry']
        profanity.load_censor_words(custom_badwords)
        # make sure it doesn't find real profanity anymore
        self.assertFalse(profanity.contains_profanity("Fuck you!"))
        # make sure it finds profanity in a sentence containing custom_badwords
        self.assertTrue(profanity.contains_profanity("Have a merry day! :)"))
        
    def test_censorship_without_spaces(self):
        bad_text = "...penis...hello_cat_vagina,,,,qew"
        censored_text = "...****...hello_cat_****,,,,qew"
        self.assertEqual(profanity.censor(bad_text), censored_text)
        
    def test_unicode_censorship(self):
        bad_text = "соседский мальчик сказал хайль и я опешил."
        censored_text = "соседский мальчик сказал **** и я опешил."
        profanity.load_unicode_symbols()
        profanity.load_censor_words(["хайль"])
        self.assertEqual(profanity.censor(bad_text), censored_text)
        
    def test_unicode_censorship_2(self):
        bad_text = "Эффекти́вного противоя́дия от я́да фу́гу не существу́ет до сих пор"
        censored_text = "Эффекти́вного **** от я́да фу́гу не существу́ет до сих пор"
        profanity.load_unicode_symbols()
        profanity.load_censor_words(["противоя́дия"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_unicode_censorship_3(self):
        bad_text = "Эффекти́вного противоя́дия от я́да фу́гу не существу́ет до сих пор. Но э́то не остана́вливает люде́й от употребле́ния блюд из ры́бы фу́гу."
        censored_text = "Эффекти́вного **** от я́да фу́гу не существу́ет до сих пор. Но э́то не остана́вливает люде́й от **** блюд из ры́бы фу́гу."
        profanity.load_unicode_symbols()
        profanity.load_censor_words(["противоя́дия", "употребле́ния"])
        self.assertEqual(profanity.censor(bad_text), censored_text)
       
    def test_unicode_censorship_4(self):
        bad_text = "...противоя́ди...hello_cat_употребле́ния,,,,qew"
        censored_text = "...****...hello_cat_****,,,,qew"
        profanity.load_unicode_symbols()
        profanity.load_censor_words(["противоя́дия", "употребле́ния"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

        
if __name__ == "__main__":
    unittest.main()
