import os
import cv2

def get_video_info(video_path):
    if not os.path.isfile(video_path):
        print("Video file does not exist.")
        return None

    video_extension = os.path.splitext(video_path)[1].lower()
    if video_extension != '.mp4':
        print("Invalid video type. Only .mp4 files are supported.")
        return None

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error opening video file.")
        return None

    video_size = os.path.getsize(video_path)
    video_size_mb = round(video_size / (1024 * 1024), 2)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    duration = round(total_frames / frame_rate, 2)
    file_size = int(video.get(cv2.CAP_PROP_POS_AVI_RATIO) * video.get(cv2.CAP_PROP_FOURCC))
    bitrate = round((file_size * 8) / (duration * 1000), 2)
    video_name = os.path.basename(video_path)

    video.release()

    return video_name, video_size_mb, frame_rate, bitrate, total_frames, duration


def main():
    path = '/home/mlops/Documents/Sohail/Projects/videos'
    video_paths = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.mp4')]
    video_paths.sort()
    
    # Count and store the names of videos with bad health
    bad_health_videos = []
    
    for video in video_paths:
        video_info = get_video_info(video)
        
        if video_info is None:
            continue  # Skip to the next video if there is an error
        
        name, size, framerate, bitrate, totalframe, length = video_info
        print("Video Name:", name)
        print("Video Size:", size, "MB")        
        print("Frame Rate of video:", framerate)
        print("Video Bitrate:", bitrate)
        print("Total Frame of video:", totalframe)
        print("Total length of video in sec:", length)
        
        # Check if the duration is appropriate and frame rate is good
        if 40.0 <= length <= 120 or 15 <= framerate <= 30:
            print("Video health is good.")
        else:
            print("Video health is not good.")
            name = os.path.basename(os.path.splitext(name)[0])
            bad_health_videos.append(name)
        
        print()
    
    print("----------------------------------")
    print("Summary of Data quality monitoring")
    num_videos = len(video_paths)
    print("Total number of videos:", num_videos)
    
    # Count and display the bad health videos
    num_bad_health_videos = len(bad_health_videos)
    print("Total videos with bad health:", num_bad_health_videos)
    percentage_bad_health_videos = round((num_bad_health_videos / num_videos) * 100, 2)
    print("Percentage of videos with bad health:", percentage_bad_health_videos, "%")
    print("Bad health videos:")
    for video_name in bad_health_videos:
        print(video_name,end=",")
    print()


# Call the main function
main()