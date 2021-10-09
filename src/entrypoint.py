import logging
import sys
from typing import List

from constants import DEBUG
from generator import VideoGenerator
from options import Options


def print_usage(prg_name: str):
	print("")
	print(f"Usage: {prg_name} [OPTIONS]")
	print("  OPTIONS:")
	print("    -d --debug          Enable debug mode")
	print("    -h --help           Print this help message")
	print("")


def parse_args(argv: List[str]):
	logging.basicConfig(encoding='utf-8', level=logging.INFO)

	assert len(argv) >= 1
	program_name, *argv = argv

	while(len(argv) > 0):
		arg = argv[0]

		if(arg == "-d" or arg == "--debug"):
			global DEBUG
			DEBUG = True
		elif(arg == "-h" or arg == "--help"):
			print_usage(program_name)
			exit(0)
		else:
			logging.warning(f" Ignoring unrecognized command line option '{arg}'")

		argv = argv[1:]

	if(DEBUG):
		logging.basicConfig(encoding='utf-8', level=logging.DEBUG, force=True)
		logging.debug(" Enabling debug mode")


def main(argv: List[str]):
	parse_args(argv)

	o = Options()
	o.select_path_idle_pose("base_frames/idle01.png")
	o.select_paths_get_down_pose([
		"base_frames/getdown01.png",
		"base_frames/getdown02.png"
	])
	o.select_paths_random_pose([
		"base_frames/random01.png",
		"base_frames/random02.png",
		"base_frames/random03.png",
		"base_frames/random04.png",
		"base_frames/random05.png",
		"base_frames/random06.png",
		"base_frames/random07.png",
		"base_frames/random08.png",
		"base_frames/random09.png",
		"base_frames/random10.png",
		"base_frames/random11.png",
		"base_frames/random12.png",
		"base_frames/random13.png",
		"base_frames/random14.png",
		"base_frames/random15.png",
	])
	o.select_paths_hip_shake_pose([
		"base_frames/hipshake01.png",
		"base_frames/hipshake02.png",
		"base_frames/hipshake03.png",
	])
	o.select_paths_hip_thrust_pose([
		"base_frames/hipthrust01.png",
		"base_frames/hipthrust02.png",
	])
	o.select_paths_chikau_pose([
		"base_frames/chikau01.png",
		"base_frames/chikau02.png",
		"base_frames/chikau01.png",
	])

	v = VideoGenerator(o)
	v.start_generation()


if __name__ == '__main__':
	main(sys.argv)
