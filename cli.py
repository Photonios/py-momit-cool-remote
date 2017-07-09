import logging
import argparse

from momitcool import MomitCool


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Control your Momit Cool.')

    parser.add_argument(
        '--host', type=str, help='ip address of your momit cool.')

    parser.add_argument(
        '--action', type=str, choices=['on', 'off'],
        help='the action to perform'
    )

    args = parser.parse_args()

    cool = MomitCool(args.host)
    if args.action == 'on':
        cool.on()
    else:
        cool.off()


if __name__ == '__main__':
    main()

