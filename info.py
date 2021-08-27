from argparse import Namespace, ArgumentParser
from datetime import date, datetime, timedelta
from tqdm import tqdm
from graph import get_datetimes_from, get_intervals

def get_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('-f', '--files', type=str, nargs='+',
		help='CSV file to load', required=True)

    args = parser.parse_args(None)

    return args

def main():
    args = get_args()
    datetimes = get_datetimes_from(args.files)
    
    intervals = get_intervals(datetimes)

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