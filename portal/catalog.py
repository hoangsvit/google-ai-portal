"""Curated public offer directory; no account access or scraping."""
from dataclasses import dataclass
from urllib.parse import urlsplit
import webbrowser

ALLOWED_HOSTS = frozenset({
    "one.google.com", "trainings.internshala.com",
})

@dataclass(frozen=True)
class Offer:
    id: str
    title: str
    provider: str
    description: str
    eligibility: str
    region: str
    url: str
    reviewed: str

OFFERS = (
    Offer(
        "google-plans", "Google AI plans", "Google",
        "Compare Google AI Plus, Pro and Ultra plans.",
        "Availability and pricing depend on account and region.",
        "Country-specific", "https://one.google.com/about/google-ai-plans/",
        "2026-11-26",
    ),
    Offer(
        "google-students", "Google AI student offers", "Google",
        "Published introductory student offers for eligible users.",
        "Actual student status and provider verification required. Review renewal terms.",
        "Selected countries", "https://one.google.com/intl/en_ie/about/articles/google-ai-for-students/",
        "2026-11-26",
    ),
    Offer(
        "internshala-training", "Google AI Plus with course enrollment", "Internshala",
        "The provider advertises a one-year AI Plus benefit with eligible course enrollment.",
        "Review course fees, enrollment conditions, country restrictions and redemption terms.",
        "Provider-dependent", "https://trainings.internshala.com/generative-ai-course/",
        "2026-11-26",
    ),
)

def find_offers(query: str = "") -> tuple[Offer, ...]:
    words = query.casefold().split()
    return tuple(
        offer for offer in OFFERS
        if all(word in " ".join((offer.id, offer.title, offer.provider,
                                  offer.description, offer.eligibility, offer.region)).casefold()
               for word in words)
    )

def get_offer(offer_id: str) -> Offer:
    for offer in OFFERS:
        if offer.id == offer_id:
            return offer
    raise ValueError(f"Unknown offer: {offer_id}")

def validate_url(url: str) -> None:
    parts = urlsplit(url)
    if (parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS
            or parts.username is not None or parts.password is not None
            or parts.port not in (None, 443)
            or any(char.isspace() or ord(char) < 32 for char in url)
            or "\\" in url):
        raise ValueError("Only approved HTTPS provider URLs are supported.")

def open_offer(offer: Offer) -> bool:
    validate_url(offer.url)
    return webbrowser.open(offer.url, new=2)
