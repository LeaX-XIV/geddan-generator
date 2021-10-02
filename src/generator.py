import logging
import subprocess
from typing import Iterable

from constants import DEBUG
from constants import FFMPEG_COMMAND
from constants import FFMPEG_LOG_FILE
from constants import FRAMERATE
from constants import PATH_AUDIO_ORIGINAL
from constants import PATH_LISTFILE
from constants import PATH_OUTPUT
from constants import TIMINGS
import generators
from options import Options, FrameType
from utils import to_ffmpeg_duration_string


class VideoGenerator():

	def __init__(self, opt: Options):
		self.user_options = opt
		"""
			The Options object the user will interact with.
			It contains all the paths of the image and/or video files to generate a GEDDAN video.
		"""
		self.iterators: dict(FrameType, Iterable[str]) = {}

	def start_generation(self) -> int:
		if(not self.user_options.ready):
			raise RuntimeError()

		self.iterators = {
			FrameType.IDLE: generators.idle_generator((self.user_options.path_idle_pose + '.')[:-1]),
			FrameType.GETDOWN: generators.getdown_generator(self.user_options.paths_get_down_pose),
			FrameType.RANDOM: generators.random_generator(self.user_options.paths_random_pose, self.user_options.selection_type),
			FrameType.HIPSHAKE: generators.hipshake_generator(self.user_options.paths_hip_shake_pose),
			FrameType.HIPTHRUST: generators.hipthrust_generator(self.user_options.paths_hip_thrust_pose),
			FrameType.CHIKAU: generators.chikau_generator(self.user_options.paths_chikau_pose),
		}

		logging.info(" Generating frames list file")
		frame_duration: float = 1 / FRAMERATE
		with open(PATH_LISTFILE, "w") as f:
			f.write("ffconcat version 1.0\n")
			for i in range(len(TIMINGS)):
				type, nframe = TIMINGS[i].values()
				filename: str = next(self.iterators[type])
				duration_str: str = to_ffmpeg_duration_string(nframe * frame_duration)

				if(DEBUG):
					f.write(f"# frame {type}\n")
				f.write(f"    file '{filename}'\n")
				f.write(f"    duration {duration_str}\n")

				if(type == FrameType.CHIKAU and TIMINGS[i - 1]['type'] == FrameType.HIPTHRUST):
					self.iterators[FrameType.HIPTHRUST] = generators.hipthrust_generator(
                                            self.user_options.paths_hip_thrust_pose
                                        )
		full_cmd: str = FFMPEG_COMMAND.format(
                    path_listfile=PATH_LISTFILE,
                    path_audio=PATH_AUDIO_ORIGINAL,
                    framerate=FRAMERATE,
                    path_output=PATH_OUTPUT
                )

		logging.info(" Generating video file")
		logging.debug(" Running command:")
		logging.debug(f" {full_cmd}")
		with open(FFMPEG_LOG_FILE, "w") as log:
			return_code: int = subprocess.call(
				full_cmd.split(' '), stdout=log, stderr=log
			)

		if(return_code == 0):
			# os.remove(FFMPEG_LOG_FILE)
			logging.info(" Success")
		else:
			logging.error(
				f" Could not generate video file. See log in {FFMPEG_LOG_FILE}")

	def get_next_filepath_of(self, frtype: FrameType) -> str:
		return next(self.iterators[frtype])
