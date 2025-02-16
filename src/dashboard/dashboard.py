import streamlit as st
from datetime import datetime, timedelta
from data import load_json_data, load_week_data, process_data, format_duration
from charts import display_metrics

def get_monday_of_week(date):
    """Get the Monday of the week containing the given date."""
    return date - timedelta(days=date.weekday())

def display_daily_view():
    """Display the daily view with activity data."""
    selected_date = st.date_input("Select Date", datetime.now())
    data = load_json_data(selected_date)
    
    if data.empty:
        st.info(f"No activity logs available for {selected_date.strftime('%B %d, %Y')}")
        return
    
    time_spent, window_inputs, website_time = process_data(data)
    display_metrics(time_spent, window_inputs, website_time, prefix="daily_")

def display_weekly_view():
    """Display the weekly view with navigation and summary."""
    # Initialize or get the selected week's Monday
    if 'week_start' not in st.session_state:
        st.session_state.week_start = get_monday_of_week(datetime.now().date())

    # Navigation controls
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("← Previous Week"):
            st.session_state.week_start -= timedelta(days=7)
            st.rerun()
    
    with col2:
        week_end = st.session_state.week_start + timedelta(days=6)
        st.markdown(f"### Week: {st.session_state.week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}")
        if st.button("Today's Week"):
            st.session_state.week_start = get_monday_of_week(datetime.now().date())
            st.rerun()
    
    with col3:
        if st.button("Next Week →"):
            st.session_state.week_start += timedelta(days=7)
            st.rerun()

    # Load and display the week's data
    week_data = load_week_data(st.session_state.week_start)
    
    if week_data.empty:
        st.info("No activity logs available for this week")
        return

    # Display daily summary
    st.subheader("Daily Breakdown")
    cols = st.columns(7)
    
    daily_data = week_data.groupby('date').agg({
        'duration': 'sum',
        'keystrokes': 'sum',
        'mouse_clicks': 'sum'
    }).reset_index()

    for i, col in enumerate(cols):
        date = st.session_state.week_start + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        
        with col:
            st.markdown(f"**{date.strftime('%a')}**")
            st.markdown(f"*{date.strftime('%d')}*")
            
            day_data = daily_data[daily_data['date'] == date_str]
            if not day_data.empty:
                duration = format_duration(day_data.iloc[0]['duration'])
                st.markdown(f"Time: {duration}")
            else:
                st.markdown("No data")

    # Display weekly aggregated data
    st.subheader("Weekly Summary")
    time_spent, window_inputs, website_time = process_data(week_data)
    display_metrics(time_spent, window_inputs, website_time, prefix="weekly_")

def display_streak_and_blocked_items():
    """Display streak information and blocked items management."""
    if 'tracker' in st.session_state:
        streak_manager = st.session_state.tracker.streak_manager
        
        # Streak display in a prominent card
        streak_info = streak_manager.format_streak()
        st.markdown("""
        <div style='padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 1rem;'>
            <h2 style='margin:0;'>🏆 Focus Streak</h2>
            <h3 style='color: #0066cc; margin:0;'>{}</h3>
            <p style='margin:0; color: #666;'>{}</p>
        </div>
        """.format(streak_info['main'], streak_info['detail']), unsafe_allow_html=True)

        # Blocked items management in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📱 Blocked Applications")
            new_app = st.text_input("Add custom application to block", key="new_app")
            if st.button("Add App", key="add_app"):
                if new_app:
                    streak_manager.add_blocked_app(new_app)
                    st.success(f"Added {new_app}")
            
            # Display blocked apps with default vs custom indication
            if streak_manager.blocked_apps:
                st.markdown("##### Default Blocked Apps")
                for app in sorted(streak_manager.blocked_apps):
                    if streak_manager.is_default_blocked(app, 'apps'):
                        st.text(f"• {app}")
                
                st.markdown("##### Custom Blocked Apps")
                for app in sorted(streak_manager.blocked_apps):
                    if not streak_manager.is_default_blocked(app, 'apps'):
                        cols = st.columns([3, 1])
                        cols[0].text(app)
                        if cols[1].button("🗑️", key=f"del_app_{app}"):
                            streak_manager.remove_blocked_app(app)
                            st.rerun()
        
        with col2:
            st.subheader("🌐 Blocked Websites")
            new_domain = st.text_input("Add custom domain to block", key="new_domain")
            if st.button("Add Domain", key="add_domain"):
                if new_domain:
                    streak_manager.add_blocked_domain(new_domain)
                    st.success(f"Added {new_domain}")
            
            # Display blocked domains with default vs custom indication
            if streak_manager.blocked_domains:
                st.markdown("##### Default Blocked Domains")
                for domain in sorted(streak_manager.blocked_domains):
                    if streak_manager.is_default_blocked(domain, 'domains'):
                        st.text(f"• {domain}")
                
                st.markdown("##### Custom Blocked Domains")
                for domain in sorted(streak_manager.blocked_domains):
                    if not streak_manager.is_default_blocked(domain, 'domains'):
                        cols = st.columns([3, 1])
                        cols[0].text(domain)
                        if cols[1].button("🗑️", key=f"del_domain_{domain}"):
                            streak_manager.remove_blocked_domain(domain)
                            st.rerun()

def display_dashboard():
    """Main dashboard display function."""
    st.title("Time Tracking Dashboard")
    
    # Display streak and blocked items at the top
    display_streak_and_blocked_items()
    
    # Add some spacing
    st.markdown("---")
    
    # Continue with existing tabs
    tab1, tab2 = st.tabs(["Daily View", "Weekly View"])
    with tab1:
        display_daily_view()
    with tab2:
        display_weekly_view()
