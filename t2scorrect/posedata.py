from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
#clone this https://github.com/sign-language-processing/pose/tree/master?tab=readme-ov-file
# Load the .pose file
data_buffer = open("C:\\Users\\kabil\\Downloads\\signvideo\\youth.pose", "rb").read()
pose = Pose.read(data_buffer)

# Create a visualizer object
visualizer = PoseVisualizer(pose)

# Save the visualized poses as a video
visualizer.save_video("C:\\Users\\kabil\\Downloads\\signvideo\\output_video.mp4", visualizer.draw())

# Optionally, save the overlay on the original video
visualizer.save_video("C:\\Users\\kabil\\Downloads\\signvideo\\output_overlay.mp4", visualizer.draw_on_video("C:\\Users\\kabil\\Downloads\\signvideo\\yummy.mp4"))

# Optional: Save as GIF if using a Jupyter notebook or Google Colab
# visualizer.save_gif("C:\\Users\\kabil\\Downloads\\signvideo\\output.gif", visualizer.draw())
