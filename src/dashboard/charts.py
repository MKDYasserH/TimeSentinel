import streamlit as st
import plotly.express as px
from data import format_duration

# Define a custom color palette
colors = ["#FF6347", "#FFD700", "#90EE90", "#87CEFA", "#DA70D6", "#FFA500", "#40E0D0", "#ADFF2F", "#FF69B4", "#CD5C5C"]

def display_metrics(time_spent, window_inputs, website_time, prefix=""):
    """Display metrics using Plotly charts."""
    st.subheader("Time Spent by Window")
    total_duration = time_spent['duration'].sum()
    formatted_total = format_duration(total_duration)  # Format total duration intuitively
    fig_time = px.pie(
        time_spent,
        values='duration',
        names='window_title',
        title=f'Time Spent by Window (Top 10) | Total: {formatted_total}',
        hole=0.3,
        color_discrete_sequence=colors
    )
    fig_time.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_time, use_container_width=True, key=f"{prefix}pie_chart")

    st.subheader("Input Activity by Window")
    col1, col2 = st.columns(2)
    with col1:
        fig_keys = px.histogram(
            window_inputs,
            x='window_title',
            y='keystrokes',
            title='Keystrokes per Window',
            labels={'window_title': 'Window Title', 'keystrokes': 'Keystrokes'},
            color_discrete_sequence=colors
        )
        fig_keys.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_keys, use_container_width=True, key=f"{prefix}keystrokes_chart")
    with col2:
        fig_clicks = px.histogram(
            window_inputs,
            x='window_title',
            y='mouse_clicks',
            title='Mouse Clicks per Window',
            labels={'window_title': 'Window Title', 'mouse_clicks': 'Mouse Clicks'},
            color_discrete_sequence=colors
        )
        fig_clicks.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_clicks, use_container_width=True, key=f"{prefix}mouse_clicks_chart")

    st.subheader("Website Time Breakdown")
    if not website_time.empty:
        website_time["root"] = "All Websites"
        fig_websites = px.treemap(
            website_time,
            path=['root', 'website'],
            values='duration',
            title='Time Spent on Websites',
            color_discrete_sequence=colors
        )
        fig_websites.update_traces(textinfo="label+value")
        st.plotly_chart(fig_websites, use_container_width=True, key=f"{prefix}website_treemap")
