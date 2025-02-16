import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def load_json_data(date):
    """Load data from JSON file for a specific date."""
    try:
        file_path = Path(f"activity_logs/activity_log_{date.strftime('%Y%m%d')}.json")
        if not file_path.exists():
            return pd.DataFrame()
        with open(file_path, 'r') as f:
            data = pd.DataFrame(json.load(f))
            if not data.empty:
                data['date'] = pd.to_datetime(date).strftime('%Y-%m-%d')
            return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def load_week_data(start_date):
    """Load data for a specific week."""
    week_data = []
    for i in range(7):
        date = start_date + timedelta(days=i)
        daily_data = load_json_data(date)
        if not daily_data.empty:
            week_data.append(daily_data)
    
    if not week_data:
        return pd.DataFrame()
    
    return pd.concat(week_data, ignore_index=True)

def process_data(df):
    """Process the dataframe to extract relevant metrics."""
    if df.empty:
        return None, None, None

    for col in ['duration', 'keystrokes', 'mouse_clicks']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    def get_window_title(row):
        try:
            winfo = row.get('window_info', {})
            title = winfo.get('window_title', '').strip()
            return title if title else winfo.get('app_name', 'Unknown')
        except Exception:
            return 'Unknown'

    def get_website_domain(row):
        try:
            if row.get('window_info', {}).get('app_name') in ['Google Chrome', 'Safari']:
                if isinstance(row.get('browser_info'), dict):
                    domain = row['browser_info'].get('domain', 'Unknown')
                    return domain if domain.strip() else 'Unknown'
            return None
        except Exception:
            return None

    df['window_title'] = df.apply(get_window_title, axis=1)
    df['website'] = df.apply(get_website_domain, axis=1)

    time_spent = df.groupby('window_title')['duration'].sum().reset_index().sort_values('duration', ascending=False).head(10)
    window_inputs = df.groupby('window_title').agg({
        'keystrokes': 'sum',
        'mouse_clicks': 'sum'
    }).reset_index().sort_values('keystrokes', ascending=False).head(10)
    website_time = df[df['website'].notna()].groupby('website')['duration'].sum().reset_index().sort_values('duration', ascending=False)

    return time_spent, window_inputs, website_time

def format_duration(seconds):
    """Return time in the format HH:MM:SS."""
    seconds = int(seconds)
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"
