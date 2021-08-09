import matplotlib.pyplot as plt
from argparse import Namespace, ArgumentParser
from datetime import datetime, timedelta
from collections import defaultdict
import sys

def get_args() -> Namespace:
	parser = ArgumentParser()

	parser.add_argument('-f', '--file', type=str,
		help='CSV file to load', required=True)
	parser.add_argument('-c', '--include_current',
		type=bool, default=False, const=True, nargs='?',
		help='Include interval from the latest entry until now')

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

def get_hours_distribution(intervals: list[timedelta]) -> dict[int, int]:
	d: dict[int, int] = defaultdict(lambda: 0)
	for td in intervals:
		d[get_hours(td)] += 1
	return d

def get_median(intervals: list[timedelta]) -> float:
	median = list( map(get_hours, intervals) )
	median.sort()
	if len(median) == 0:
		return (median[len(median)//2] + median[len(median)//2 + 1]) / 2
	else:
		return median[len(median)//2]
	
def get_avg(td_distribution: list[int, int]) -> float:
	s = sum(map(lambda x: x[0]*x[1], td_distribution))
	amount = sum(
		map(
			lambda x: x[1],
			td_distribution
		)
	)
	return s / amount

def main():
	args = get_args()

	datetimes = get_datetimes_from(args.file)
		
	intervals = get_intervals(datetimes)

	if len(intervals) == 0:
		print('No available interval detected.', file=sys.stderr)
		exit(-1)

	d = get_hours_distribution(intervals)

	# store distribution with saved order
	d_l = list( d.items() )

	median = get_median(intervals)
	avg = get_avg(d_l)
	print(f'Average: {avg:.2f}')
	print(f'Median: {median:.2f}')

	plt.bar( list(map(lambda x: x[0], d_l)), list(map(lambda x: x[1], d_l)), align='center')
	plt.axvline(x=avg, color='r')
	plt.axvline(x=median, color='g')
	plt.xlabel('Hours')
	plt.ylabel('Amount')
	plt.title( args.file )
	plt.legend(['Average', 'Median', 'Amount'])
	# plt.show()
	# plt.clf()

	if args.include_current:
		# add current timedelta
		intervals.append( datetime.now() - datetimes[-1])

		d = get_hours_distribution(intervals)
		d_l = list( d.items() )

		curr_median = get_median(intervals)
		curr_avg = get_avg(d_l)
		print(f'Average (+ current): {curr_avg:.2f}')
		print(f'Median (+ current):  {curr_median:.2f}')

		plt.bar( d_l[-1][0], d_l[-1][1], align='center', color='orange')
		plt.axvline(x=curr_avg, color='y')
		plt.axvline(x=curr_median, color='m')
		plt.title( f'{args.file} + current' )
		plt.legend(['Average', 'Median', 'Average + current', 'Median + current', 'Amount', 'Current interval'])
	plt.show()

if __name__ == '__main__':
	main()