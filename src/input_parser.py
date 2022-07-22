import argparse


def stdin():
    # required args
    parser = argparse.ArgumentParser(description="Parser tutorial")
    parser.add_argument("source", nargs='?', type=str,
                        help="This is the source place")
    parser.add_argument("destination", nargs='?', type=str,
                        help="This is the destination place")
    parser.add_argument("date", nargs='?', type=str,
                        help="This is the date option")

    args, _ = parser.parse_known_args()

    source = args.source
    destination = args.destination
    date = args.date

    return source, destination, date
