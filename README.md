# 🛰️ InPost Gap Scanner (Coverage Analyzer)

An interactive Location Intelligence tool designed to identify "service deserts" and gaps in the InPost parcel locker network across Poland.

## 🎯 Project Overview
**What did you build?**
I developed a specialized analytical web application that visualizes areas where InPost services are missing. Unlike standard maps that display existing points, this tool uses a **band-pass distance filter** to isolate and highlight regions where the nearest parcel locker is located within a specific user-defined distance range (e.g., 500m to 1500m).

## 🧩 Problem Statement
**What problem are you solving?**
With over 90,000 points in the network, standard distribution maps become cluttered, making it difficult to spot underserved areas in high-density cities. For expansion and logistics teams, the priority is identifying "white spots." My tool solves this by filtering out well-served zones (points below the minimum distance) and irrelevant far-off areas (points above the maximum distance), leaving only the critical gaps visible.

## 🛠️ Technical Decisions & Architecture
**Why this stack?**
*   **FastAPI (Python)**: Selected for its high performance and native support for asynchronous tasks, which is crucial for handling large-scale API data fetching.
*   **Spatial Analysis (cKDTree)**: To ensure millisecond-level responsiveness, I implemented a **K-Dimensional Tree** (`scipy.spatial`). This allows the system to find the nearest neighbor in $O(\log n)$ time, avoiding expensive $O(n)$ brute-force calculations.
*   **Coordinate Transformation (EPSG:2180)**: I used `pyproj` to transform WGS84 coordinates into the Polish 1992 metric system. This ensures that the distance sliders (in meters) provide geographically accurate results on the map.
*   **Viewport-Based Processing**: To optimize performance, the engine only calculates the heatmap for the user's current map bounds (bbox), preventing unnecessary server-side load.

## 🚀 How to Build and Run
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/lojekb/inpost-coverage-analyzer
    cd inpost-coverage-analyzer
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Launch the application**:
    
```bash
    python main.py
```
4.  **View the tool**:
    Navigate to `http://127.0.0.1:8000` in your browser.

## 📊 Key Features
*   **Interactive Distance Sliders**: Real-time adjustment of the "Gap Range" (Min vs Max distance).
*   **Automated Data Pipeline**: Fetches live data from the InPost Global Points API.
*   **Smart Visualization**: A heatmap that ignores "noise" and only renders the specific band of service exclusion defined by the user.

## 🔮 Future Roadmap
*   **Isochrone Integration**: Moving from "as the crow flies" distance to actual walking time using road network data.
*   **Demographic Heatmaps**: Layering population density data to identify gaps in the most populated areas.
*   **Locker Availability**: Incorporating real-time locker status from the API to show where capacity is a recurring issue.

---
*Developed as a Technical Assignment for InPost.*