import cv2
import os


def extract_frames(video_path, output_folder, interval_ms=300):
    os.makedirs(output_folder, exist_ok=True)

    # open video
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Failed to open video:", video_path)
        return

    # get frames per second
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * (interval_ms / 1000))

    print(f"Video fps:{fps}, extracting 1 frame every {frame_interval} frames")

    count = 0
    frame_id = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        if count % frame_interval == 0:
            frame_filename = f"{output_folder}/frame_{frame_id}.jpg"
            cv2.imwrite(frame_filename, frame)
            print("Saved:", frame_filename)
            frame_id += 1

        count += 1

    video.release()
    print("Frame extraction complete.")
