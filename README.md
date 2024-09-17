# Object Tracker with Template Matching and OpenCV

This project implements an object tracker using OpenCV, combining the CSRT algorithm with template matching for enhanced accuracy. The `Tracker` class allows users to initialize a video stream, select an object to track, and continuously track the object throughout the video. If the tracker loses the object, it uses template matching to attempt to find and reinitialize the tracker.

## Features

- **CSRT Tracker**: Utilizes OpenCV's CSRT tracker for accurate and robust object tracking.
- **Template Matching**: Provides a backup method to find the object if the primary tracker loses it.
- **Image Enhancement**: Applies Gaussian blur and adaptive histogram equalization to improve the accuracy of template matching.
- **Dynamic Reinitialization**: Reinitializes the tracker if the object is found again using template matching.

## Requirements

- Python 3.6+
- OpenCV (`opencv-contrib-python`)

### Installation

Install OpenCV using pip if not already installed:

```bash
pip install opencv-python
```

Clone the repository and import the `Tracker` class into your project:

```bash
git clone https://github.com/Thomas-Kr/object-tracking.git
```

## Usage

1. **Initialize the Tracker**: Create an instance of the `Tracker` class by providing the video source. The source can be a video file path or a camera index.
2. **Run the Tracking Process**: Call the track method to start tracking the selected object in the video. You can optionally set a threshold for template matching.
3. **Select the Object to Track**: When you run the track method, the program will display the first frame of the video. Use the mouse to draw a bounding box around the object you want to track. Press 'Enter' or 'Space' to confirm the selection.
4. **Tracking**:
  - The tracker will attempt to follow the selected object throughout the video.
  - If the tracker loses the object, it uses template matching to try to find it again and reinitialize the tracker.
  - The tracked object is displayed with a bounding box, and its top-left coordinates (X and Y) are shown on the screen.
  - If the object is lost and cannot be found, the text "Lost" is displayed on the video feed.
5. **Exit the Tracking**: To stop the tracking process, press the 'q' key. This will exit the loop, release the video capture, and close all OpenCV windows.

```python
  tracker = Tracker("source.mp4")
  tracker.track(threshold=0.7)
```

   
