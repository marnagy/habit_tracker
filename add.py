from argparse import ArgumentParser, Namespace
from datetime import datetime

FILE_NAME = 'habit.csv'

def get_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('-n', '--habit_name', type=str, help='Name of a habit', required=True)

    return parser.parse_args()

def main():
    args = get_args()

    with open(f'{args.habit_name}.csv', 'a') as csv_file:
        print(datetime.now().isoformat(), file=csv_file)

if __name__ == '__main__':
    main()