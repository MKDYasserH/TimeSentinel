import sys
from pathlib import Path
import streamlit as st
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from activity_tracker.tracker import ActivityTracker
from dashboard import display_dashboard
from main import update_activity_log

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'tracker' not in st.session_state:
        st.session_state.tracker = ActivityTracker()
    if 'tracking' not in st.session_state:
        st.session_state.tracking = False

if __name__ == "__main__":
    st.set_page_config(
        page_title="Time Tracker",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Main content: Display the new dashboard
    display_dashboard()
    
    # Sidebar: Activity tracking controls
    with st.sidebar:
        st.header("Activity Tracking")
        
        if not st.session_state.tracking:
            if st.button('Start Tracking', key='start_button'):
                st.session_state.tracker.start(callback=update_activity_log)
                st.session_state.tracking = True
                st.rerun()
        else:
            if st.button('Stop Tracking', key='stop_button'):
                st.session_state.tracker.stop()
                st.session_state.tracking = False
                st.rerun()
        
        # Show tracking status
        if st.session_state.tracking:
            st.success("● Currently Tracking")
        else:
            st.error("○ Not Tracking")