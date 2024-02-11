"""
This module contains various useful functions in order to process data or create repeated arrays
"""

# Recursively removes empty array from an input deep nested array
def remove_empty(l):
	return list(filter(lambda x: not isinstance(x, (str, list, list)) or x, (remove_empty(x) if isinstance(x, (list, list)) else x for x in l)))

# Fill list with 1s - create a check matrix
def create_check_matrix(l):
	for i, sl in enumerate(l):
		for j, ssl in enumerate(sl):
			for k, sssl in enumerate(ssl):
				for m in range(len(sssl)):
					l[i][j][k][m] = 1
	return l