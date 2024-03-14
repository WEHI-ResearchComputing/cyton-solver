"""
Last Edit: 11-Feb-2024

This module contains various useful functions in order to process data or create repeated arrays
"""
from typing import Iterable, Any

def flatten(l: Iterable[Any]) -> Iterable[Any]:
	for item in l:
		if isinstance(item, list):
			yield from flatten(item)
		else:
			yield item

# Recursively removes empty array from an input deep nested array
def remove_empty[T](l: Iterable[T]) -> list[T]:
	return [
		# Recursively call this on lists
		remove_empty(x) if isinstance(x, list) else x
		for x in l
		# Keep anything that is truthy, or anything that isn't a list or string.
		# In other words, remove [] and ""
		if x or not isinstance(x, (str, list))
	]
