import sys
import pstats

a = len(sys.argv)

if(a > 2):
	p = pstats.Stats(sys.argv[1])
	deArghed = sys.argv[2:]
	p.strip_dirs().sort_stats(*deArghed).print_stats()
elif(a == 2):
	p = pstats.Stats(sys.argv[1])
	deArghed = sys.argv[2:]
	p.strip_dirs().sort_stats('file', 'name', 'line').print_stats()
else:
	print ('\n\nHow to use:' + '\npython fancystats.py filetobeanalyzed sorts to be '
	+ 'performed\n\nPossible Sorts: calls, cumulative, file, module, pcalls,'
	+ ' line, name, stdname, time, nfl\n')
	print ('Generate the file to be analyzed with:\n'
	+ 'python -m cProfile -o outputFile pythonfiletobeanalyzed\n\n')