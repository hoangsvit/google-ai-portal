import unittest
from unittest.mock import patch
from portal.catalog import OFFERS, find_offers, get_offer, open_offer, validate_url
from portal.__main__ import main

class CatalogTests(unittest.TestCase):
    def test_unique_ids_and_valid_urls(self):
        self.assertEqual(len(OFFERS), len({offer.id for offer in OFFERS}))
        for offer in OFFERS:
            validate_url(offer.url)

    def test_search(self):
        self.assertEqual(find_offers("INTERNshala")[0].id, "internshala-training")
        self.assertEqual(find_offers("missing-offer"), ())
        self.assertEqual(len(find_offers()), len(OFFERS))

    def test_unknown_id(self):
        with self.assertRaises(ValueError):
            get_offer("invalid")

    def test_reject_unsafe_urls(self):
        for url in (
            "http://one.google.com",
            "https://one.google.com.evil.example",
            "https://one.google.com@evil.example",
            "https://user@one.google.com",
            "https://one.google.com:8443",
            "file:///tmp/test",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)

    @patch("portal.catalog.webbrowser.open", return_value=True)
    def test_browser(self, browser):
        offer = get_offer("google-plans")
        self.assertTrue(open_offer(offer))
        browser.assert_called_once_with(offer.url, new=2)

    @patch("portal.__main__.open_offer", return_value=False)
    def test_browser_failure(self, browser):
        self.assertEqual(main(["--open", "google-plans"]), 1)

if __name__ == "__main__":
    unittest.main()
