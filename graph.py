import matplotlib.pyplot as plt
from argparse import Namespace, ArgumentParser
from datetime import datetime, timedelta
from collections import defaultdict
import sys

def get_args() -> Namespace:
	parser = ArgumentParser()

	parser.add_argument('-f', '--file', help='CSV file to load', required=True)

	args = parser.parse_args()

	return args

def get_datetimes_from(path: str) -> list[datetime]:
	with open(path, 'r') as csv_file:
		datetimes = list(
			map(
				lambda line: datetime.fromisoformat(line),
				map(
					lambda x: x.strip(),
					csv_file.readlines()
				)
			)
		)
	return datetimes

def get_intervals(datetimes: list[datetime]) -> list[timedelta]:
	return list(
		map(
			lambda x: x[1] - x[0],
			zip(datetimes[:], datetimes[1:])
		)
	)

def get_hours(td: timedelta) -> int:
	return td.days*24 + td.seconds // 3600

def main():
	args = get_args()

	datetimes = get_datetimes_from(args.file)
		
	intervals = get_intervals(datetimes)

	if len(intervals) == 0:
		print('No available interval detected.', file=sys.stderr)
		exit(-1)

	d: dict[int, int] = defaultdict(lambda: 0)
	for td in intervals:
		d[get_hours(td)] += 1
	
	d_l = list( d.items() )

	print(d)

	median = list( map(get_hours, intervals) )
	median.sort()
	median = median[len(median)//2] if len(median) % 2 != 0 else (median[len(median)//2] + median[len(median)//2 + 1]) / 2

	avg = sum(map(lambda x: x[0]*x[1], d_l)) / len(intervals)

	plt.bar( list(map(lambda x: x[0], d_l)), list(map(lambda x: x[1], d_l)), align='center')
	plt.axvline(x=avg, color='r')
	plt.axvline(x=median, color='g')

	plt.xlabel('Hours')
	plt.ylabel('Amount')
	plt.title( args.file )
	plt.legend(['Average', 'Median', 'Amount'])
	plt.show()

if __name__ == '__main__':
	main()