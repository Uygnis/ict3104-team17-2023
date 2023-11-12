# Video inferencing and analysis work flow with Follow Your Pose

This project extends the capabilities of the Follow Your Pose project by enabling users to upload their video files locally for both training and MMPose. Users can compare the outputs of the training to determine the best fit for their needs. The workflow consists of running MMPose code, followed by training and inferencing. Users can then analyze the results using Superimpose and calculate the Fréchet Inception Distance (FID) for quantitative analysis.

## Getting Started

To use this project, follow the steps below in order. Note that the first code block is crucial for installing all dependencies. Pay attention to input parameters to select input files or adjust fields to affect the output.

### Section 1: MMPose Skeleton Video Generation

This section utilizes MMPose to generate a skeleton video. Follow the steps in code blocks 1.2 and 1.3 to upload files needed for training, MMPose, and inference. Use code block 1.3 to generate a skeleton video using MMPose.

### Section 2: Model Training

This section is responsible for training a new model for inference. It begins by downloading a pre-trained model. Set various parameters for training, including input files and output adjustment fields. After training, test the new model by generating GIFs.

If you prefer to use your own files, upload functions are available in section 1.2.

### Section 3: Inferencing with Follow Your Pose

Perform inferencing using Follow Your Pose. Select the skeleton video file and a prompt. Generate the code with the inputs and run the inference. Add a caption to the generated video and view the input and output side by side for comparison. Manually enter the paths of the videos to be compared under sections 3.5 and 3.6.

### Section 4: Visual Analysis

Analyze inferencing output by superimposing input skeleton videos on the initial input video (used for skeleton generation) and the inferencing output.

### Section 5: Quantitative Analysis - FID Calculation

Perform quantitative analysis by calculating the Fréchet Inception Distance (FID) between the input video (for MMPose) and the output (from inferencing). Resize the original video to fit the generated video, cut it into frames, and use them to calculate the FID.

## Important Note

Ensure that all sections are executed in order, starting with the installation of dependencies. Be attentive to input parameters for selecting files and adjusting output fields.

Access the Colab notebook [here](https://colab.research.google.com/drive/1XdgEihd99v_wrNxGctVIwOyXiJsa4x6i?usp=sharing) to get started.
