# TimeSentinel - Productivity Time Tracker
test

TimeSentinel is a powerful macOS application that helps you monitor and improve your productivity by tracking your application usage, maintaining focus streaks, and providing detailed activity insights.

## Features

### Activity Tracking
- **Window Tracking**: Monitors active applications and window titles
- **Input Monitoring**: Tracks keystrokes and mouse clicks
- **Browser Integration**: Tracks website usage in Chrome and Safari
- **Automatic Logging**: Saves activity data in daily JSON files

### Focus System
- **Focus Streaks**: Maintains a streak system for uninterrupted productive work
- **Distractions Blocking**: Built-in blocklist for common distracting apps and websites
- **Custom Blocks**: Add your own applications and domains to block
- **Streak Protection**: Automatically breaks streak when accessing blocked content

### Analytics Dashboard
- **Daily View**: Detailed breakdown of daily activities
- **Weekly Analysis**: Week-by-week comparison and trends
- **Visual Stats**: Interactive charts showing time distribution
- **Website Insights**: Treemap visualization of web browsing patterns

## Installation

### Prerequisites
- macOS (10.15 or later)
- Python 3.8+
- pip (Python package installer)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TimeSentinel.git
cd TimeSentinel
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the dashboard:
```bash
streamlit run src/dashboard/app.py
```

2. Use the dashboard interface to:
   - Start/Stop tracking (sidebar controls)
   - View daily and weekly statistics
   - Manage blocked applications and websites
   - Monitor your focus streak

## Directory Structure
```
TimeSentinel/
├── src/
│   ├── activity_tracker/    # Core tracking functionality
│   ├── dashboard/          # Streamlit dashboard
│   └── rewards/           # Streak and rewards system
├── config/               # Configuration files
└── activity_logs/      # Daily activity data
```

## Configuration

### Default Blocked Items
Edit `config/default_blocks.json` to modify the default list of blocked applications and domains.

### Custom Blocks
Use the dashboard interface to add or remove custom blocked items, which are stored in `config/blocked_items.json`.

## Data Storage

Activity data is stored locally in JSON files:
- Location: `activity_logs/`
- Format: `activity_log_YYYYMMDD.json`
- Contains: Window usage, input statistics, and streak data

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
