import os
import sys
from argparse import ArgumentParser
from urllib.request import urlopen

from .kml import parse_kml, write_kml
from .scraper import get_all_history, login


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--username",
        help="FlightAware username or email address [$FLIGHTAWARE_USERNAME]",
        default=os.environ.get("FLIGHTAWARE_USERNAME"),
    )
    parser.add_argument(
        "--password",
        help="FlightAware password [$FLIGHTAWARE_PASSWORD]",
        default=os.environ.get("FLIGHTAWARE_PASSWORD"),
    )
    parser.add_argument("--out", "-o", help="Output file name", metavar="OUTFILE")
    parser.add_argument(
        "target",
        help="Aircraft registration or flight number",
    )
    args = parser.parse_args()
    if not (args.username and args.password):
        print("--username or $FLIGHTAWARE_USERNAME and --password or $FLIGHTAWARE_PASSWORD are required")
        parser.exit()

    if args.out:
        outfile = args.out
    else:
        outfile = f"{args.target}.kml"

    browser = login(args.username, args.password)
    urls = get_all_history(browser, args.target)
    print(f"{len(urls)} flights found")
    if not urls:
        return

    tracks = []
    airports = {}
    errors = []
    reqs = 0
    print("Fetching flight track logs... ", end="")
    sys.stdout.flush()
    for url in urls:
        with urlopen(f"{url}/google_earth") as response:
            if response.getcode() != 200:
                errors.append(url)
                continue
            r_tracks, r_airports = parse_kml(response)
        tracks += r_tracks
        for name, el in r_airports.items():
            if name != " Airport" and name not in airports:
                airports[name] = el
        reqs += 1
        if reqs % 5 == 0:
            print(reqs, end=" ")
            sys.stdout.flush()
    if reqs >= 5:
        print()
    write_kml(
        outfile, tracks + list(airports.values()), f"Flight track log for {args.target}"
    )
    print(f"{reqs} flight track logs written to {outfile}")


if __name__ == "__main__":
    main()
