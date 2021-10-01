import os
from typing import Iterable

from constants import DEBUG, FFMPEG_COMMAND, FRAMERATE, PATH_AUDIO_ORIGINAL, PATH_LISTFILE, PATH_OUTPUT, TIMINGS
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

	def start_generation(self):
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

		os.system(FFMPEG_COMMAND.format(path_listfile=PATH_LISTFILE,
		          path_audio=PATH_AUDIO_ORIGINAL, framerate=FRAMERATE, path_output=PATH_OUTPUT))

	def get_next_filepath_of(self, frtype: FrameType) -> str:
		return next(self.iterators[frtype])
