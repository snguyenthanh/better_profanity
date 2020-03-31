# -*- coding: utf-8 -*-

import unittest

from better_profanity import profanity


class ProfanityTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Pre-load CENSOR_WORDSET
        profanity.load_censor_words()

    def test_contains_profanity(self):
        profane = profanity.contains_profanity("he is a m0th3rf*cker")
        self.assertTrue(profane)

    def test_leaves_paragraphs_untouched(self):
        innocent_text = """If you prick us do we not bleed?
                        If you tickle us do we not laugh?
                        If you poison us do we not die?
                        And if you wrong us shall we not revenge?"""
        censored_text = profanity.censor(innocent_text)
        self.assertEqual(innocent_text, censored_text)

    def test_empty_string(self):
        censored_text = profanity.censor("")
        self.assertEqual(censored_text, "")

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

    def test_censorship_3(self):
        bad_text = "Those 2 girls 1 cup. You gotta check. "
        censored_text = "Those ****. You gotta check. "
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_censorship_4(self):
        bad_text = "2 girls 1 cup"
        censored_text = "****"
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_censorship_5(self):
        bad_text = "fuck 2 girls 1 cup"
        censored_text = "**** ****"
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
        custom_badwords = ["happy", "jolly", "merry"]
        profanity.load_censor_words(custom_badwords)
        # make sure it doesn't find real profanity anymore
        self.assertFalse(profanity.contains_profanity("Fuck you!"))
        # make sure it finds profanity in a sentence containing custom_badwords
        self.assertTrue(profanity.contains_profanity("Have a merry day! :)"))

    def test_censorship_without_spaces(self):
        bad_text = "...pen1s...hello_cat_vagina,,,,qew"
        censored_text = "...****...hello_cat_****,,,,qew"
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_custom_words(self):
        bad_text = "supremacia ariana"
        censored_text = "****"
        profanity.add_censor_words([bad_text])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_custom_words_doesnt_remove_initial_words(self):
        bad_text = "fuck and heck"
        censored_text = "**** and heck"
        profanity.add_censor_words(["supremacia ariana"])
        self.assertEqual(profanity.censor(bad_text), censored_text)


class ProfanityUnicodeTestRussian(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Pre-load CENSOR_WORDSET
        profanity.load_censor_words()

    def test_unicode_censorship(self):
        bad_text = "соседский мальчик сказал хайль и я опешил."
        censored_text = "соседский мальчик сказал **** и я опешил."
        profanity.load_censor_words(["хайль"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_unicode_censorship_2(self):
        bad_text = "Эффекти́вного противоя́дия от я́да фу́гу не существу́ет до сих пор"
        censored_text = "Эффекти́вного **** от я́да фу́гу не существу́ет до сих пор"
        profanity.load_censor_words(["противоя́дия"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_unicode_censorship_3(self):
        bad_text = "Эффекти́вного противоя́дия от я́да фу́гу не существу́ет до сих пор. Но э́то не остана́вливает люде́й от употребле́ния блюд из ры́бы фу́гу."
        censored_text = "Эффекти́вного **** от я́да фу́гу не существу́ет до сих пор. Но э́то не остана́вливает люде́й от **** блюд из ры́бы фу́гу."
        profanity.load_censor_words(["противоя́дия", "употребле́ния"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_unicode_censorship_4(self):
        bad_text = "...противоя́дия...hello_cat_употребле́ния,,,,qew"
        censored_text = "...****...hello_cat_****,,,,qew"
        profanity.load_censor_words(["противоя́дия", "употребле́ния"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_unicode_censorship_5(self):
        bad_text = "Маргаре́та (э́то бы́ло её настоя́щее и́мя) родила́сь в 1876 (ты́сяча восемьсо́т се́мьдесят шесто́м) году́ в Нидерла́ндах. В 18 (восемна́дцать) лет Маргаре́та вы́шла за́муж и перее́хала в Индоне́зию. Там она́ изуча́ла ме́стную культу́ру и та́нцы."
        censored_text = "Маргаре́та (э́то бы́ло её настоя́щее и́мя) родила́сь в 1876 (ты́сяча восемьсо́т се́мьдесят ****) году́ в ****. В 18 (восемна́дцать) лет Маргаре́та вы́шла за́муж и **** в Индоне́зию. Там она́ изуча́ла ме́стную культу́ру и ****."
        profanity.load_censor_words(["шесто́м", "Нидерла́ндах", "перее́хала", "та́нцы"])

        self.assertEqual(profanity.censor(bad_text), censored_text)


class ProfanityUnicodeTestVietnamese(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Pre-load CENSOR_WORDSET
        profanity.load_censor_words()

    def test_unicode_vietnamese_1(self):
        bad_text = "Đây là 1 câu nói bậy."
        censored_text = "Đây là 1 **** nói ****."
        profanity.load_censor_words(["câu", "bậy"])
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_unicode_vietnamese_2(self):
        bad_text = "Con chó sủa gâu gâu!"
        censored_text = "Con chó sủa **** ****!"
        profanity.load_censor_words(["gâu"])
        self.assertEqual(profanity.censor(bad_text), censored_text)


class ProfanityWhitelistTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Pre-load CENSOR_WORDSET
        profanity.load_censor_words()

    def test_whitelist_words(self):
        bad_text = "I am gay"
        censored_text = "I am ****"
        self.assertEqual(profanity.censor(bad_text), censored_text)

        # Whitelist the word `gay`
        profanity.load_censor_words(whitelist_words=["gay"])
        self.assertEqual(profanity.censor(bad_text), bad_text)


class ProfanityFileTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_read_wordlist_not_found(self):
        with self.assertRaises(FileNotFoundError):
            profanity.load_censor_words_from_file("not_found_file.txt")


if __name__ == "__main__":
    unittest.main()
