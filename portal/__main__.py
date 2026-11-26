"""Desktop and command-line entry point."""
import argparse
import sys
from .catalog import find_offers, get_offer, open_offer

def main(argv=None):
    parser = argparse.ArgumentParser(prog="eplus-ai-portal")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--list", action="store_true", help="List published offers")
    actions.add_argument("--open", metavar="ID", help="Open the provider's official page")
    parser.add_argument("--search", default="", help="Filter the list")
    args = parser.parse_args(argv)
    if args.search and not args.list:
        parser.error("--search requires --list")
    if args.list:
        for offer in find_offers(args.search):
            print(f"{offer.id}: {offer.title}\n  {offer.eligibility}\n  {offer.url}\n")
        return 0
    if args.open:
        try:
            if open_offer(get_offer(args.open)):
                return 0
            print("Unable to open your browser.", file=sys.stderr)
        except (ValueError, OSError) as exc:
            print(str(exc), file=sys.stderr)
        return 1
    try:
        from .ui import run
        run()
    except ImportError:
        print("Tk is unavailable. Install Tk or use --list.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unable to start desktop UI: {exc}. Try --list.", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
