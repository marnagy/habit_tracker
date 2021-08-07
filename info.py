from argparse import Namespace, ArgumentParser
from datetime import datetime, timedelta
from tqdm import tqdm

def get_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('-f', '--file', help='CSV file to plot', required=True)

    args = parser.parse_args(None)

    return args

def main():
    args = get_args()

    with open(args.file, 'r') as csv_file:
        datetimes = list(
            map(
                lambda line: datetime.fromisoformat(line),
                map(
                    lambda x: x.strip(),
                    csv_file.readlines()
                )
            )
        )
    
    intervals = list(
        map(
            lambda dt_pair: dt_pair[1] - dt_pair[0],
            zip(datetimes, datetimes[1:])
        )
    )

    if len(intervals) > 0:
        min_interval = min(intervals) if len(intervals) > 0 else 'NaN'
        avg_interval = sum(intervals, timedelta()) / len(intervals) if len(intervals) > 0 else 'NaN'
        max_interval = max(intervals) if len(intervals) > 0 else 'NaN'
        last_interval = intervals[-1] if len(intervals) > 0 else 'NaN'

        print(f'Minimum interval:\t{ min_interval  }')
        print(f'Average interval:\t{ avg_interval  }')
        print(f'Maximum interval:\t{ max_interval  }')
        print(f'Last interval:   \t{ last_interval }')
    
    print(f'Time since last: \t{ datetime.now() - datetimes[-1] }')

if __name__ == '__main__':
    main()