
![trans_poster](https://github.com/akmgeek/GestureVerse/assets/106646158/67bd1e95-1bb9-48f2-8022-d55e9432a99f)


GestureVerse is a hand gesture recognition project that enables control of various applications and functionalities using gestures captured via a webcam. The project utilizes MediaPipe for hand landmark detection, OpenCV for image processing, and PyAutoGUI for simulating mouse and keyboard inputs.

## Features

1. **Media Control**: Control media playback (play, pause, next, previous) using hand gestures.
2. **PowerPoint Control**: Navigate through slides in PowerPoint presentations with gestures.
3. **Virtual Mouse**: Move the cursor and perform click actions on the screen using hand movements.
4. **Painter Mode**: Draw, erase, and create shapes (lines, rectangles, circles) using gestures.

## Installation

### Prerequisites

- Python 3.6+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

### Step-by-Step Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/akmgeek/GestureVerse.git
    cd GestureVerse
    ```

2. **Install Dependencies**:

    ```bash
    pip install opencv-python-headless mediapipe pyautogui numpy
    ```

3. **Add Tool Image**:

    Place a `tools.png` image in the project directory. This image is used for tool selection in painter mode.

## Usage

Run the main script:

```bash
python main.py
```

### Modes

GestureVerse operates in four modes:
1. **Media Control Mode**: Control media playback.
2. **PowerPoint Control Mode**: Navigate through PowerPoint slides.
3. **Virtual Mouse Mode**: Control the cursor and perform clicks.
4. **Painter Mode**: Draw and create shapes on the screen.

### Switching Modes

Switch between modes using gestures with your non-dominant hand:
- 1 Finger: Media Control Mode
- 2 Fingers: PowerPoint Control Mode
- 3 Fingers: Virtual Mouse Mode
- 4 Fingers: Painter Mode

### Hand Gestures

- **Media Control**:
    - 1 Finger: Next
    - 2 Fingers: Previous
    - 3 Fingers: Volume Up
    - 4 Fingers: Volume Down
    - 5 Fingers: Play/Pause
- **PowerPoint Control**:
    - 1 Finger: Next Slide
    - 2 Fingers: Previous Slide
- **Virtual Mouse**:
    - Index and middle fingers up: Move cursor
    - Index finger half closed: Right click
    - Middle finger half closed: Left click
- **Painter Mode**:
    - Line Tool: Select from the toolbar
    - Rectangle Tool: Select from the toolbar
    - Draw Tool: Select from the toolbar
    - Circle Tool: Select from the toolbar
    - Erase Tool: Select from the toolbar

## Project Structure

- `gesture_verse.py`: Main script containing the `HandGestureRecognition` class and the main execution loop.
- `HandGestureRecognition`: Class handling all gesture recognition and control functionalities.
- `control_media`: Method for media control gestures.
- `control_ppt`: Method for PowerPoint control gestures.
- `control_virtual_mouse`: Method for virtual mouse control gestures.
- `control_painter`: Method for painter mode gestures.
- `count_fingers`: Utility method to count the number of fingers detected.
- `fingers_status`: Utility method to determine the status of each finger (up or down).
- `switch_mode`: Method to switch between different operational modes.
- `getTool`: Utility method to determine the selected tool in painter mode.
- `index_raised`: Utility method to check if the index finger is raised.

## Contribution

Contributions via pull requests are welcome! Feel free to fork this repository and enhance the project.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [MediaPipe](https://mediapipe.dev/) by Google for hand landmark detection.
- [OpenCV](https://opencv.org/) for computer vision functionalities.
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for simulating mouse and keyboard inputs.


