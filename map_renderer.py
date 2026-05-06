import folium
from folium.plugins import HeatMap
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

def render_smooth_heatmap(heat_data: List[List[float]], center_location: Tuple[float, float], output_filename: str):
    if not heat_data:
        logger.warning("No data to render.")
        return

    m = folium.Map(location=center_location, zoom_start=12, tiles="CartoDB dark_matter")

    HeatMap(
        heat_data,
        radius=25,
        blur=15,
        min_opacity=0.4,
        gradient={0.0: 'blue', 0.25: 'cyan', 0.5: 'lime', 0.75: 'yellow', 1.0: 'red'}
    ).add_to(m)

    m.save(output_filename)