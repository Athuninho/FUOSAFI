"""
FUOSAFI - Interactive Folium Map Builder
Creates responsive, interactive maps with status markers, popups, category filters, and automatic hotspot warning circles.
"""

from typing import List, Dict, Any, Optional
import folium
from folium.plugins import MarkerCluster
import config
from utils.ai_engine import detect_hotspots_and_warnings

# Coastal Kenya Default Center (Mombasa coastline)
DEFAULT_CENTER = [-4.0435, 39.6682]
DEFAULT_ZOOM = 11

def create_reports_map(
    reports: List[Dict[str, Any]],
    center_coords: Optional[List[float]] = None,
    zoom_start: int = DEFAULT_ZOOM,
    show_hotspot_warnings: bool = True
) -> folium.Map:
    """
    Builds a Folium map loaded with pollution report markers.
    Marker colors represent report status.
    If multiple incidents cluster together, automated warning alert circles are rendered.
    """
    if center_coords is None:
        if reports and len(reports) > 0:
            avg_lat = sum(r["latitude"] for r in reports) / len(reports)
            avg_lon = sum(r["longitude"] for r in reports) / len(reports)
            center = [avg_lat, avg_lon]
        else:
            center = DEFAULT_CENTER
    else:
        center = center_coords

    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="CartoDB positron"
    )

    # 1. Automatic Hotspot Alert Warning Circles (if 2+ incidents in proximity)
    if show_hotspot_warnings and reports:
        hotspots = detect_hotspots_and_warnings(reports)
        for spot in hotspots:
            color = "#E05638" if spot["severity"] == "CRITICAL" else "#E67E22"
            warning_html = f"""
            <div style="font-family: Arial, sans-serif; font-size: 12px; width: 220px; color: #193642;">
                <b style="color: {color}; font-size: 13px;">⚠️ HOTSPOT WARNING ZONE</b><br>
                <b>Area:</b> {spot['location_name']}<br>
                <b>Clustered Incidents:</b> {spot['cluster_count']} observations<br>
                <b>Severity:</b> <span style="color: {color}; font-weight: bold;">{spot['severity']}</span><br>
                <small style="color: #666;">Multiple pollution reports pinpointed in this zone.</small>
            </div>
            """
            folium.Circle(
                location=[spot["avg_latitude"], spot["avg_longitude"]],
                radius=1800, # 1.8km radius
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.22,
                weight=2,
                dash_array="5, 5",
                popup=folium.Popup(warning_html, max_width=250),
                tooltip=f"⚠️ Contamination Warning Zone ({spot['cluster_count']} reports)"
            ).add_to(m)

    # 2. Marker Cluster for Individual Incident Pinpoints
    marker_cluster = MarkerCluster().add_to(m)

    for r in reports:
        status = r.get("status", config.STATUS_SUBMITTED)
        color = config.STATUS_COLORS.get(status, "#087F8C")
        
        category = r.get("category", "")
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 13px; width: 220px; color: #193642;">
            <b style="color: #063B56; font-size: 14px;">{r.get('reference_number', 'N/A')}</b><br>
            <span style="display:inline-block; margin-top:3px; margin-bottom:5px; background:{color}; color:#fff; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">
                {status}
            </span><br>
            <b>Category:</b> {r.get('category')}<br>
            <b>Location:</b> {r.get('location_name', 'N/A')}<br>
            <b>Date:</b> {r.get('date_observed')}<br>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #e0e0e0;">
            <p style="margin: 0; font-size: 12px; color: #555;">{r.get('title')}</p>
        </div>
        """

        folium.CircleMarker(
            location=[r["latitude"], r["longitude"]],
            radius=8,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{r.get('reference_number')} - {r.get('title')}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2
        ).add_to(marker_cluster)

    return m


def create_location_picker_map(default_lat: float = -4.0435, default_lon: float = 39.7123) -> folium.Map:
    """
    Creates an interactive map allowing the user to view and click/pinpoint coordinates.
    """
    m = folium.Map(
        location=[default_lat, default_lon],
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    folium.Marker(
        [default_lat, default_lon],
        tooltip="Selected Observation Point",
        icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
    ).add_to(m)

    m.add_child(folium.LatLngPopup())
    return m
