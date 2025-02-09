# README for Time Tracker

## Overview
The Time Tracker is a local macOS application designed to help users monitor and analyze their time usage during working hours. The application tracks active window titles, mouse clicks, and keystrokes, providing insights into productivity and focus.

## Key Features
- **Activity Tracking**: Logs the active window title and duration, mouse clicks, and keystrokes.
- **Custom Note Annotations**: Allows users to manually enter annotations tied to timestamps.
- **Streak-Based Reward System**: Encourages focus through a streak system that rewards uninterrupted work sessions.
- **Data Visualization Dashboard**: Displays daily and weekly statistics of tracked data using charts and graphs.

## Tech Stack
- **Language**: Python
- **Libraries**:
  - `pyobjc` for macOS window tracking
  - `pynput` for mouse and keyboard tracking
  - `sqlite3` or `pandas` for data storage
  - `Streamlit` or `Dash/Plotly` for the dashboard

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd time-tracker
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python -m src.dashboard.app
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.