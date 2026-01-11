"""
Flood Vulnerability API Server
Provides a REST interface for assessment and automatic OpenAPI documentation.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os

from flood_tool.data_loader import fetch_osm_data
from flood_tool.analysis import perform_analysis

app = FastAPI(
    title="Flood Vulnerability Assessment API",
    description="A scientific API for building-level flood risk analysis using vector data.",
    version="0.1.0"
)

# --- Models ---

class BBox(BaseModel):
    min_lat: float = Field(..., description="Minimum latitude")
    min_lon: float = Field(..., description="Minimum longitude")
    max_lat: float = Field(..., description="Maximum latitude")
    max_lon: float = Field(..., description="Maximum longitude")

class AnalysisRequest(BaseModel):
    city_name: str = Field(..., description="Name of the city/region")
    bbox: BBox
    water_threshold: int = Field(50, description="Distance (m) for vulnerability")
    hotspot_radius: int = Field(100, description="Radius (m) for cluster detection")
    min_neighbors: int = Field(10, description="Min neighbors for hotspots")

class AnalysisResults(BaseModel):
    city_name: str
    total_buildings: int
    vulnerable_count: int
    vulnerability_rate: float
    hotspot_count: int
    top_hotspots: List[Dict]

# --- Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    """Welcome endpoint with metadata."""
    return {
        "message": "Welcome to the Flood Vulnerability Assessment API",
        "docs": "/docs",
        "status": "online"
    }

@app.post("/analyze", response_model=AnalysisResults, tags=["Analysis"])
async def run_analysis(request: AnalysisRequest):
    """
    Perform a complete flood risk analysis for the specified bounding box.
    This includes fetching data from OSM and running spatial algorithms.
    """
    bbox_tuple = (
        request.bbox.min_lat, request.bbox.min_lon,
        request.bbox.max_lat, request.bbox.max_lon
    )

    # 1. Fetch Data
    water_nodes = fetch_osm_data(bbox_tuple, query_type="water")
    buildings = fetch_osm_data(bbox_tuple, query_type="building")

    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found in the specified area.")
    
    if not water_nodes:
         raise HTTPException(status_code=404, detail="No water bodies found in the specified area.")

    # 2. Run Logic
    vulnerable, hotspots = perform_analysis(
        buildings, water_nodes,
        water_threshold_dist=request.water_threshold,
        hotspot_radius=request.hotspot_radius,
        hotspot_min_neighbors=request.min_neighbors
    )

    return AnalysisResults(
        city_name=request.city_name,
        total_buildings=len(buildings),
        vulnerable_count=len(vulnerable),
        vulnerability_rate=len(vulnerable) / len(buildings),
        hotspot_count=len(hotspots),
        top_hotspots=hotspots[:5]
    )

@app.get("/health", tags=["General"])
def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Local dev run
    uvicorn.run(app, host="0.0.0.0", port=8000)
