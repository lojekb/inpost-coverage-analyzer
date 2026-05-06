from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging

from api_client import fetch_all_pages_async
from spatial_engine import build_global_tree, calculate_viewport_heatmap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

global_kd_tree = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global global_kd_tree
    logger.info("Uruchamianie serwera. Pobieranie danych InPost...")
    raw_points = await fetch_all_pages_async(country_code="PL", max_pages=None)
    global_kd_tree = build_global_tree(raw_points)
    logger.info("Dane załadowane. Serwer gotowy do pracy!")
    yield
    global_kd_tree = None

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_frontend():
    return FileResponse("index.html")

@app.get("/api/heatmap")
async def get_heatmap(
    min_lat: float, 
    min_lon: float, 
    max_lat: float, 
    max_lon: float,
    min_distance: float = Query(300.0), 
    max_distance: float = Query(1200.0)
):
    if not global_kd_tree:
        return {"error": "System loading"}

    bbox = (min_lat, min_lon, max_lat, max_lon)
    
    data = calculate_viewport_heatmap(
        tree=global_kd_tree,
        bbox=bbox,
        grid_size=70,
        min_distance=min_distance, 
        max_distance=max_distance
    )
    
    return {"data": data}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)