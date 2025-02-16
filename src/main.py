import json
from datetime import datetime
from pathlib import Path
from activity_tracker.tracker import ActivityTracker

def update_activity_log(activity_data):
    # Determine file path based on today's date
    log_dir = Path("activity_logs")
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    file_path = log_dir / f"activity_log_{today}.json"
    
    # Load current log if exists
    if file_path.exists():
        with open(file_path, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    
    # Append the new activity data; convert datetime to str if needed
    # (Assuming activity_data uses ISO format strings for timestamps.)
    logs.append(activity_data)
    
    with open(file_path, "w") as f:
        json.dump(logs, f, default=str, indent=2)

def activity_callback(data):
    update_activity_log(data)
    
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
        