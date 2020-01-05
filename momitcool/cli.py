import logging
import argparse

from momitcool import MomitCool


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description='Control your Momit Cool.')

    parser.add_argument(
        '--host', type=str, required=True,
        help='ip address of your momit cool.')

    parser.add_argument(
        '--cool', action='store_true',
        help='turns on the ac in cooling mode')

    parser.add_argument(
        '--off', action='store_true',
        help='turns off the ac')

    parser.add_argument(
        '--mode', action='store_true',
        help='get current mode'
    )

    parser.add_argument(
        '--temperature', action='store_true',
        help='get current temperature'
    )

    args = parser.parse_args()

    cool = MomitCool(args.host)

    if args.mode:
        print(cool.mode())

    if args.temperature:
        print(cool.temperature())

    if args.cool:
        cool.cool()

    if args.off:
        cool.off()


if __name__ == '__main__':
    main()

