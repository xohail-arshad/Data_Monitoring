import os
import cv2
import json

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
    # print(video_size_mb)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    duration = round(total_frames / frame_rate, 2)
    # file_size = int(video.get(cv2.CAP_PROP_POS_AVI_RATIO) * video.get(cv2.CAP_PROP_FOURCC))
    # print(file_size)
    # bitrate = round((file_size * 8) / (duration * 1000), 2)
    video_name = os.path.basename(video_path)

    video.release()

    return video_name, video_size_mb, duration


def main():
    # Read parameters from JSON file
    with open('parameters.json') as file:
        parameters = json.load(file)
    
    main_folder = parameters['main_folder']
    bad_health_folder = parameters['bad_health_folder']
    min_video_length = parameters['min_video_length']
    max_video_length = parameters['max_video_length']
    min_video_size = parameters['min_video_size']
    
    # Create the bad health folder if it doesn't exist
    if not os.path.exists(bad_health_folder):
        os.makedirs(bad_health_folder)
    
    video_paths = [os.path.join(main_folder, file) for file in os.listdir(main_folder) if file.endswith('.mp4')]
    video_paths.sort()
    
    # Count and store the names of videos with bad health
    bad_health_videos = []
    good_health_videos = []
    
    for video in video_paths:
        video_info = get_video_info(video)
        
        if video_info is None:
            continue  # Skip to the next video if there is an error
        
        name, size, length = video_info
        print("Video Name:", name)
        print("Video Size:", size, "MB")        
        print("Total length of video in sec:", length)
        
        # Check if the duration is appropriate and frame rate is good
        if min_video_length <= length <= max_video_length and size >= min_video_size:
            print("Video health is good.")
            good_health_videos.append(name)
        else:
            print("Video health is not good.")
            name = os.path.basename(os.path.splitext(name)[0])
            bad_health_videos.append(name)
            
            # Move the bad health video to the bad health folder
            video_filename = os.path.basename(video)
            new_path = os.path.join(bad_health_folder, video_filename)
            os.rename(video, new_path)
            print("Video moved to bad health folder.")
        
        print()
    
    print("----------------------------------")
    print("Summary of Data quality monitoring")
    num_videos = len(video_paths)
    print("Total number of videos:", num_videos)
    
    # Count and display the bad health videos
    num_bad_health_videos = len(bad_health_videos)
    num_good_health_videos = len(good_health_videos)
    print("Total videos with bad health:", num_bad_health_videos)
    print("Total videos with good health:", num_good_health_videos)
    percentage_bad_health_videos = round((num_bad_health_videos / num_videos) * 100, 2)
    print("Percentage of videos with bad health:", percentage_bad_health_videos, "%")
    

if __name__ == "__main__":
    main()