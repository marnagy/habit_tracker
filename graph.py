import matplotlib.pyplot as plt
from argparse import Namespace, ArgumentParser
from datetime import datetime, timedelta

def get_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('-f', '--file', help='CSV file to load', required=True)

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    datetimes: list[datetime] = None
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
            lambda x: x[1] - x[0],
            zip(datetimes[:], datetimes[1:])
        )
    )

    max_hours = max(
        map(
            get_hours,
            intervals
        )
    )

    d: dict[int, int] = dict()
    for i in range(max_hours + 1):
        d[i] = sum(
            map(
                lambda td: get_hours(td) == i,
                intervals
            )
        )
    
    d = { k:v for k,v in d.items() if v > 0 }
    d_l = list( k_v_pair for k_v_pair in d.items() )

    print(d)

    plt.bar( list(map(lambda x: x[0], d_l)), list(map(lambda x: x[1], d_l)))
    plt.xlabel('Hours')
    plt.ylabel('Amount')
    plt.title( '.'.join(args.file.split('.')[:-1]) )
    plt.show()

def get_hours(td: timedelta) -> int:
    return td.days*24 + td.seconds // 3600

if __name__ == '__main__':
    main()