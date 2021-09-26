# -*- coding: utf-8 -*-

import unittest

import better_profanity
from better_profanity import profanity, Profanity
import os


class ProfanityTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Pre-load CENSOR_WORDSET
        profanity.load_censor_words()

    def test_contains_profanity(self):
        profane = profanity.contains_profanity("he is a m0th3rf*cker")
        self.assertTrue(profane)

    def test_leaves_paragraphs_untouched(self):
        innocent_text = """If you tickle us do we not laugh?
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

    def test_init_with_list(self):
        custom_badwords = ["happy", "jolly", "merry"]
        Profanity(custom_badwords)
        Profanity(set(custom_badwords))
        Profanity(tuple(custom_badwords))

    def test_init_with_bad_type(self):
        with self.assertRaises(TypeError):
            Profanity(123)
        with self.assertRaises(TypeError):
            Profanity(False)

    def test_punctuation(self):
        bad_text = "Holy shit! Oh fuck, damn. What the hell? Shut up, asshole..."
        censored_text = "Holy ****! Oh ****, ****. What the ****? Shut up, ****..."
        self.assertEqual(profanity.censor(bad_text), censored_text)

    def test_all_default_words(self):
        """Tests that every word in the default word list is censored"""
        wordlist_path = os.path.join(
            better_profanity.__file__, "../profanity_wordlist.txt"
        )
        wordlist_path = os.path.abspath(wordlist_path)
        with open(wordlist_path) as f:
            for word in f.readlines():
                word = word.strip()
                if word:
                    self.assertEqual(profanity.censor(word)[:4], "****")
                    self.assertTrue(profanity.contains_profanity(word))


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
        bad_text = "I have boobs"
        censored_text = "I have ****"
        self.assertEqual(profanity.censor(bad_text), censored_text)

        # Whitelist the word `boobs`
        profanity.load_censor_words(whitelist_words=["boobs"])
        self.assertEqual(profanity.censor(bad_text), bad_text)


class ProfanityFileTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_read_wordlist_not_found(self):
        with self.assertRaises(FileNotFoundError):
            profanity.load_censor_words_from_file("not_found_file.txt")

    def test_init_wordlist_not_found(self):
        with self.assertRaises(FileNotFoundError):
            Profanity("not_found_file.txt")


class ProfanityLargeCorpusTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Pre-load CENSOR_WORDSET
        profanity.load_censor_words()

    def test_0per_paragraph(self):
        # Paragraph with no profanity.
        good_text = "Veniam sed do pariatur irure deserunt. Et fugiat sint reprehenderit eiusmod magna. Deserunt occaecat officia eu quis. Velit laborum enim nulla laborum tempor ad. Amet culpa veniam nisi reprehenderit officia, elit ullamco exercitation do, incididunt qui voluptate quis incididunt. Tempor culpa ea amet ipsum, dolore quis proident pariatur. Laboris reprehenderit ad eiusmod proident irure dolor, fugiat qui aute aute et dolor aliqua. Ullamco fugiat deserunt aliqua consequat sit proident consectetur, qui nulla excepteur sit. Occaecat dolor sed occaecat cupidatat labore quis incididunt. Sit ex aute fugiat cupidatat reprehenderit."
        self.assertEqual(profanity.censor(good_text), good_text)
        self.assertFalse(profanity.contains_profanity(good_text))

    def test_5per_paragraph(self):
        # Paragraph with about 5% profanity.
        bad_text = "G@*k do dolore sunt exercitation do cillum, adipiscing mollit sit qui sit. Nulla ea aliquip sed non, exercitation in officia exercitation sed. Velit aliquip eiusmod ut est ad, ullamco ex veniam aliqua exercitation eiusmod excepteur, minim sint aliquip adipiscing sit. Quis cupidatat nulla laboris sit ex, eiusmod aliquip labore $hagg3r labore duis. Amet ut excepteur fugiat tempor exercitation ipsum. Ipsum nulla commodo aliqua veniam sit consequat aliqua, nostrud exercitation deserunt ut dolore adipiscing duis et. Et officia elit occaecat pariatur sed. G*dd*mn*d labore deserunt ad. Nostrud non non ea irure, ex cupidatat fugiat do nostrud enim veniam. Sint consequat consectetur in exercitation, dolore occaecat aute sed."
        censored_text = "**** do dolore sunt exercitation do cillum, adipiscing mollit sit qui sit. Nulla ea aliquip sed non, exercitation in officia exercitation sed. Velit aliquip eiusmod ut est ad, ullamco ex veniam aliqua exercitation eiusmod excepteur, minim sint aliquip adipiscing sit. Quis cupidatat nulla laboris sit ex, eiusmod aliquip labore **** labore duis. Amet ut excepteur fugiat tempor exercitation ipsum. Ipsum nulla commodo aliqua veniam sit consequat aliqua, nostrud exercitation deserunt ut dolore adipiscing duis et. Et officia elit occaecat pariatur sed. **** labore deserunt ad. Nostrud non non ea irure, ex cupidatat fugiat do nostrud enim veniam. Sint consequat consectetur in exercitation, dolore occaecat aute sed."
        self.assertEqual(profanity.censor(bad_text), censored_text)
        self.assertTrue(profanity.contains_profanity(bad_text))

    def test_50per_paragraph(self):
        # Paragraph with about 50% profanity.
        bad_text = "Exercitation g@ngbangs quis mv7h@ h4ndjob aliqua. T**7 sit enim esse 7e3z ph*kk3d. Adipiscing f*cknvt quis nisi. Culpa 0p*@7* aliqua sunt laborum br**s7s, nisi dlckh3ad cillum lorem pariatur. Laborum ex k@ndvm5 mollit pariatur 571ffy g3y. Amet g3y ipsum $h*t7lng esse lu$ty laboris. Prick duis pariatur d4mn aute p*5sing minim. Incididunt dolore negro r31ch commodo feck3r 1vs7 p*cker. Tempor p*nk@ nisi elit, quis h*rdcor*$ex nobh*4d p*s$y$ thug d1nk phvck, et ipsum culpa f*dgep@ck3r fvckt@rd k@*ch3$ 1ab**."
        censored_text = "Exercitation **** quis **** **** aliqua. **** sit enim esse **** ****. Adipiscing **** quis nisi. Culpa **** aliqua sunt laborum ****, nisi **** cillum lorem pariatur. Laborum ex **** mollit pariatur **** ****. Amet **** ipsum **** esse **** laboris. **** duis pariatur **** aute **** minim. Incididunt dolore **** **** commodo **** **** ****. Tempor **** nisi elit, quis **** **** **** **** **** ****, et ipsum culpa **** **** **** ****."
        self.assertEqual(profanity.censor(bad_text), censored_text)
        self.assertTrue(profanity.contains_profanity(bad_text))

    def test_100per_paragraph(self):
        # Paragraph with only profanity.
        bad_text = "C@ck5 j1z p*$5e cr0tch u*y**r n@d 5tfu p*5$*ng, g@nj4 m*nstr**71on fvkwhit f1ngerfucked f*ckwi7 f*kker st1ffy h@mo*r@7*c. Fuck7@rd 2 gir1$ 1 cvp 5hit 7*bglr1 en1*rg3ment perv3r5i*n. Fuckh3ad g*ddam r*mp f*g$ fvcknugge7 d@gg**57y13. P*wn 1*zzy f*t4n*ry m*thaf*ck*r. Wanky 5tupid bltchin bvc37a, fuckup pot $h17f*ck*r f*s7f*ck3d f1st3d, mv7h*rfvcker stf* *jacu1*te thre*$0m* dlck. H@w70mvrd*p phuk5 w@nk*r clpa fuk*r 5h*7* c0cks, c*n7lick*r k14n *rr5e kumming."
        censored_text = "**** **** **** **** **** **** **** ****, **** **** **** **** **** **** **** ****. **** **** **** **** **** ****. **** **** **** **** **** ****. **** **** **** ****. **** **** **** ****, **** **** **** **** ****, **** **** **** **** ****. **** **** **** **** **** **** ****, **** **** **** ****."
        self.assertEqual(profanity.censor(bad_text), censored_text)
        self.assertTrue(profanity.contains_profanity(bad_text))


if __name__ == "__main__":
    unittest.main()
