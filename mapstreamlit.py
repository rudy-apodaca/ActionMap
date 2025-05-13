import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Load data
df = pd.read_csv("data/events.csv")

# Sidebar filter
status_filter = st.sidebar.selectbox("Show events:", ["All", "Past", "Future"])
if status_filter != "All":
    df = df[df["status"].str.lower() == status_filter.lower()]

# Page layout
st.title("🗺️ The Impact Map – IL-9 Community Tracker")
st.markdown("""
This interactive map shows community-centered events driven by Kat Abughazaleh's campaign. 
Hover over a pin to see outcomes from past events or click future events for how to get involved.
""")

# Create map centered on Chicago
m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

# Add pins
for _, row in df.iterrows():
    popup_html = f"""
    <strong>{row['event_name']}</strong><br>
    <em>{row['date']}</em><br>
    {row['description']}<br>
    """
    if isinstance(row['status'], str) and row['status'].lower() == 'past':
        popup_html += f"<ul><li>People Helped: {row.get('people_helped', 'N/A')}</li><li>Volunteer Hours: {row.get('volunteer_hours', 'N/A')}</li></ul>"
        color = "purple"
    else:
        if pd.notna(row.get("link")):
            popup_html += f'<a href="{row["link"]}" target="_blank">RSVP or Learn More</a>'
        color = "blue"

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=color)
    ).add_to(m)

# Render map
st_data = st_folium(m, width=700, height=500)

# Footer
st.markdown("""
---
Made with ❤️ by a believer in win-win-win-win solutions. Powered by data, mutual aid, and imagination.
""")