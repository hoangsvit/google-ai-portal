# ePlus AI Portal

A browser-first desktop utility for discovering published Google AI offers and reviewing their eligibility requirements. No Android emulator, ADB, Frida, or Google Play installation is required.

## Features

- Search an offline catalog of official Google and education-partner offer pages.
- View eligibility, region notes, and source review dates.
- Open the official page in your own browser.
- Use the desktop interface or the command line.
- No collection of credentials, cookies, verification codes, or payment details.

## Quick start

Install Python 3.10 or newer with Tk support (included in standard Windows Python installations; on Debian/Ubuntu install `python3-tk` for the desktop UI).

```bash
git clone https://github.com/hoangsvit/google-ai-portal.git
cd google-ai-portal
python -m portal
```

For Windows, double-click `start.bat` after installing Python.

## CLI

```bash
python -m portal --list
python -m portal --list --search student
python -m portal --open google-students
python -m unittest discover -s tests -v
```

## Offer availability

The catalog is informational and is not a live account eligibility check. Offers can change by account, country, student status, enrollment, and date. Review actual terms and renewal pricing on the provider's website before participating. All login, verification, enrollment and checkout are handled manually on the official website using accurate information.

This is an independent utility, not an official Google or Internshala product.
