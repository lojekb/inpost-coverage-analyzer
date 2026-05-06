import numpy as np
import logging
from pyproj import Transformer
from scipy.spatial import cKDTree
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

transformer_to_meters = Transformer.from_crs("EPSG:4326", "EPSG:2180", always_xy=True)

def build_global_tree(points: List[Dict]) -> cKDTree:
    logger.info("Budowanie globalnego Drzewa KD w pamięci...")
    lockers_coords_meters = []
    for p in points:
        lat, lon = p["location"]["latitude"], p["location"]["longitude"]
        x, y = transformer_to_meters.transform(lon, lat)
        lockers_coords_meters.append((x, y))
    
    return cKDTree(lockers_coords_meters)

def calculate_viewport_heatmap(
    tree: cKDTree, 
    bbox: Tuple[float, float, float, float], 
    grid_size: int = 70, 
    min_distance: float = 300,  
    max_distance: float = 1200 
) -> List[List[float]]:
    
    min_lat, min_lon, max_lat, max_lon = bbox
    grid_lats = np.linspace(min_lat, max_lat, num=grid_size)
    grid_lons = np.linspace(min_lon, max_lon, num=grid_size)
    
    heat_data = []
    
    for lat in grid_lats:
        for lon in grid_lons:
            x, y = transformer_to_meters.transform(lon, lat)
            distance, _ = tree.query((x, y), k=1)
            
            
            if min_distance <= distance <= max_distance:
                
                if max_distance == min_distance:
                    weight = 1.0
                else:
                    weight = (distance - min_distance) / (max_distance - min_distance)
                heat_data.append([float(lat), float(lon), float(weight)])

    return heat_data