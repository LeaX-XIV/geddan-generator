import random
from typing import List

from options import SelectionType


def idle_generator(path: str):
	while(True):
		yield path


def getdown_generator(list: List[str]):
	last_index: int = 0
	while(True):
		yield list[last_index % 2]
		last_index += 1


def random_generator(list: List[str], seltype: SelectionType):
	last_index: int = -1
	while(True):
		if(seltype == SelectionType.SELECTION_CYCLE):
			last_index += 1
			yield list[last_index % len(list)]
		elif(seltype == SelectionType.SELECTION_RANDOM):
			# paths = list.copy()
			# if(last_index != -1):
			# 	paths.pop(last_index)
			last_index = random.randrange(len(list))
			yield list[last_index]


def hipshake_generator(list: List[str]):
	last_index: int = 0
	while(True):
		yield list[last_index % 3]
		if(len(list) == 3):
			last_index += 1


def hipthrust_generator(list: List[str]):
	last_index: int = 0
	while(True):
		yield list[last_index % 2]
		last_index += 1


def chikau_generator(list: List[str]):
	last_index: int = 0
	while(True):
		yield list[last_index % 3]
		last_index += 1
