from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer

# Load the pose data
data_buffer = open("C:\\Users\\kabil\\Downloads\\signvideo\\smelly.pose", "rb").read()
pose = Pose.read(data_buffer)

# Create a visualizer object
visualizer = PoseVisualizer(pose)

# Save the visualized poses as a video
visualizer.save_video("C:\\Users\\kabil\\Downloads\\signvideo\\smellyoutput_video.mp4", visualizer.draw())


visualizer.save_video("C:\\Users\\kabil\\Downloads\\signvideo\\smellyoutput_overlay.mp4", 
                      visualizer.draw_on_video("C:\\Users\\kabil\\Downloads\\signvideo\\smelly.mp4"))

