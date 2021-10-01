from generator import VideoGenerator
from options import Options

if __name__ == '__main__':
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
