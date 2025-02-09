import json
from datetime import datetime
from pathlib import Path
from activity_tracker.tracker import ActivityTracker

def activity_callback(data):
    # Create data directory if it doesn't exist
    data_dir = Path("activity_logs")
    data_dir.mkdir(exist_ok=True)
    
    # Create a filename based on current date
    filename = data_dir / f"activity_log_{datetime.now().strftime('%Y%m%d')}.json"
    
    # Load existing data if file exists
    if filename.exists():
        with open(filename, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    
    # Append new data
    existing_data.append(data)
    
    # Write updated data back to file
    with open(filename, 'w') as f:
        json.dump(existing_data, default=str, indent=2, fp=f)
    
    # Also print to console for debugging
    print(json.dumps(data, default=str, indent=2))

if __name__ == "__main__":
    tracker = ActivityTracker()
    print("Starting activity tracking... Data will be saved in ./data/ directory")
    tracker.start(callback=activity_callback)
    
    try:
        input("Press Enter to stop tracking...\n")
    except KeyboardInterrupt:
        pass
    finally:
        tracker.stop()
        print("Tracking stopped. Check the data directory for activity logs.")