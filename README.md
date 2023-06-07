## Video Data Quality Monitoring

This script analyzes videos in a specified folder and checks their health based on predefined criteria. It moves videos with bad health to a separate folder for further inspection.

## Input Parameters

The script reads the input parameters from the `parameters.json` file. The following parameters can be specified:

- `main_folder`: The path to the folder containing the videos to be analyzed.
- `bad_health_folder`: The path to the folder where videos with bad health will be moved.
- `min_video_length`: The minimum allowed duration of a video in seconds.
- `max_video_length`: The maximum allowed duration of a video in seconds.
- `min_video_size`: The minimum allowed size of a video in megabytes.

## Working Process

1. The script reads the input parameters from the `parameters.json` file.
2. It creates the `bad_health_folder` if it doesn't already exist.
3. The script scans the `main_folder` for video files with the `.mp4` extension.
4. For each video file, it retrieves information such as the video name, size, and length.
5. It checks if the video health is good by comparing the duration and size against the specified criteria.
6. If the video health is good, it is added to the list of videos with good health. Otherwise, it is moved to the `bad_health_folder`.
7. After analyzing all the videos, the script provides a summary of the data quality monitoring, including the total number of videos, the count of videos with bad and good health, and the percentage of videos with bad health.

## Output

The script generates console output to display the analysis results. Additionally, videos with bad health are moved to the `bad_health_folder` for further investigation.

### Please note that the script only supports videos in the `.mp4` format.
