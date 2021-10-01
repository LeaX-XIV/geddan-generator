from enum import Enum, auto
from os.path import exists
from typing import List

from utils import pad_right_with, remove_none


class SelectionType(Enum):
	SELECTION_CYCLE = auto()
	SELECTION_RANDOM = auto()
	# SELECTION_RANDOM_BETTER = auto()


class ThrustPause(Enum):
	PAUSE_NO = auto()
	PAUSE_PITA = auto()
	PAUSE_RECT = auto()


class FrameType(Enum):
	IDLE = auto()
	GETDOWN = auto()
	RANDOM = auto()
	HIPSHAKE = auto()
	HIPTHRUST = auto()
	CHIKAU = auto()


class Options:
	"""
		Class to collect the options chosen by the user
	"""

	def __init__(self):
		self.path_idle_pose: str = None
		"""
			Path to the image to be used as the idle pose.
		"""

		self.paths_get_down_pose: List[str] = []
		"""
			List containing 2 strings. The strings are the paths to 2 images.
		"""
		self.paths_random_pose: List[str] = []
		"""
			List containing the paths to the images of random poses. Must contain at least 2 elements.
		"""
		self.paths_hip_shake_pose: List[str] = []
		"""
			List containing either the path to the video of the hip shake, or paths of 3 images.
			The video must be at least 0.2s long; only the [0.000, 0.200] interval will be used if longer.
			The images should be sorted as hip right to left order.

			Empty values should be `None`.
		"""
		self.paths_hip_thrust_pose: List[str] = []
		"""
			List containing 2 paths to the 2 images of the hip thrust.
			First image should have the hips forward.
			Second picture should have the hips backwards.
		"""
		self.paths_chikau_pose: List[str] = []
		"""
			List containing either 1 or 3 paths to images.
			If 1, the image is mirrored horizontally at every syllabe of CHIKAU
			If 3, the images will be played in order.

			Empty values should be `None`.
		"""

		self.selection_type: SelectionType = SelectionType.SELECTION_CYCLE
		"""
			The type of algorythm used to select the next random pose.
			- SELECTION_CYCLE: The images are displayed in the provided order, and loop back (Default)
			- SELECTION_RANDOM: The images are displayed randomically, with care to not choose the same image back to back.
		"""
		self.thrust_pause: ThrustPause = ThrustPause.PAUSE_PITA
		"""
			The type of pause image to adopt between the hip thrust and CHIKAU.
			- PAUSE_NO: No pause. This causes the thrust to continue for another loop
			- PAUSE_PITA: The pause used by japanese memers. Displays ピタッ (Default)
			- PAUSE_RECT: The pause used by american memers. Displays 2 vertical, semi-opaque, white rectangles.
		"""
		self.ready: bool = False
		"""
			This value specifies if the set of input paths is complete and ready to be converted to video.
		"""

	def select_path_idle_pose(self, path: str) -> None:
		if(not exists(path)):
			raise RuntimeError()

		self.path_idle_pose = path
		self.__check_ready__()

	def select_paths_get_down_pose(self, paths: List[str]) -> None:
		paths = remove_none(paths)

		if(len(paths) != 2):
			raise RuntimeError()

		for p in paths:
			if(not exists(p)):
				raise RuntimeError()

		self.paths_get_down_pose = tuple(paths.copy())
		self.__check_ready__()

	def select_paths_random_pose(self, paths: List[str]) -> None:
		paths = remove_none(paths)

		if(len(paths) < 2):
			raise RuntimeError()

		for p in paths:
			if(not exists(p)):
				raise RuntimeError()

		self.paths_random_pose = paths.copy()
		self.__check_ready__()

	def select_paths_hip_shake_pose(self, paths: List[str]) -> None:
		paths = remove_none(paths)

		if(len(paths) != 1 and len(paths) != 3):
			raise RuntimeError()

		for p in paths:
			if(not exists(p)):
				raise RuntimeError()

		self.paths_hip_shake_pose = tuple(pad_right_with(paths, 3, None))
		self.__check_ready__()

	def select_paths_hip_thrust_pose(self, paths: List[str]) -> None:
		paths = remove_none(paths)

		if(len(paths) != 2):
			raise RuntimeError()

		for p in paths:
			if(not exists(p)):
				raise RuntimeError()

		self.paths_hip_thrust_pose = tuple(paths.copy())
		self.__check_ready__()

	def select_paths_chikau_pose(self, paths: List[str]) -> None:
		paths = remove_none(paths)

		if(len(paths) != 1 and len(paths) != 3):
			raise RuntimeError()

		for p in paths:
			if(not exists(p)):
				raise RuntimeError()

		self.paths_chikau_pose = tuple(pad_right_with(paths, 3, None))
		self.__check_ready__()

	def select_selection_type(self, sltype: SelectionType) -> None:
		self.selection_type = sltype
		self.__check_ready__()

	def select_thrust_pause(self, thpause: ThrustPause) -> None:
		self.thrust_pause = thpause
		self.__check_ready__()

	def __check_ready__(self) -> None:
		self.ready = self.path_idle_pose is not None and \
			len(remove_none(self.paths_get_down_pose)) == 2 and \
			len(remove_none(self.paths_random_pose)) >= 2 and \
			(len(remove_none(self.paths_hip_shake_pose)) == 1 or
                            len(remove_none(self.paths_hip_shake_pose)) == 3) and \
			len(remove_none(self.paths_hip_thrust_pose)) == 2 and \
			(len(remove_none(self.paths_chikau_pose)) == 1 or
                            len(remove_none(self.paths_chikau_pose)) == 3)
