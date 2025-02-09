from streamlit import st
import pandas as pd
from database.db_manager import DatabaseManager

def load_data():
    db_manager = DatabaseManager()
    data = db_manager.get_activity_logs()  # Assuming this method retrieves activity logs
    return pd.DataFrame(data)

def display_dashboard():
    st.title("Time Tracking Dashboard")
    
    data = load_data()
    
    if not data.empty:
        st.subheader("Activity Logs")
        st.write(data)
        
        # Example visualization: Time spent per application
        time_spent = data.groupby('application')['duration'].sum().reset_index()
        st.bar_chart(time_spent.set_index('application'))
    else:
        st.write("No activity data available.")

if __name__ == "__main__":
    display_dashboard()