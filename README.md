# Flood Vulnerability Assessment Tool

This project implements a vector-based geospatial workflow for flood vulnerability and hotspot analysis. It determines which buildings are at risk based on their proximity to water bodies and identifies "hotspots" of high vulnerability density.

## Overview
The workflow implements a strictly vector-based approach to:
1.  **Ingest Data**: Fetch buildings and water bodies from OpenStreetMap (Overpass API).
2.  **Assess Vulnerability**: Identify buildings within a critical distance of water bodies.
3.  **Detect Hotspots**: Find clusters of vulnerable buildings using density estimation.
4.  **Simulate Collaboration**: A comprehensive Git history was generated to demonstrate a multi-user workflows.

**Key Technical Features:**
-   **No Rasters**: All analysis is performed on vector data (points/nodes).
-   **Custom Algorithms**: Implements a `KDTree` for efficient spatial search ($O(log n)$).
-   **Local Projection**: Projects Lat/Lon coordinates to a local metric plane for accurate distance calculation.

## Project Structure
-   `flood_tool/data_loader.py`: Fetches OSM data via API.
-   `flood_tool/algorithms/kdtree.py`: Custom KD-Tree implementation.
-   `flood_tool/analysis.py`: Core logic for vulnerability and hotspot detection.
-   `flood_tool/utils.py`: Spatial utilities (Haversine, Projection).
-   `flood_tool/visualization.py`: Folium map generation.
-   `flood_tool/cli.py`: CLI entry point to run the workflow.
-   `notebooks/venice_exploration.ipynb`: Interactive Jupyter notebook for the Venice case study.
-   `tests/`: Unit tests (pytest).
-   `pyproject.toml`: Poetry dependency management.

## How to Run

### Prerequisites
Ensure dependencies are installed using Poetry (or pip):
```bash
pip install .
# OR
poetry install
```

### Running the Workflow
Run `cli.py` to execute the analysis for Venice:
```bash
python flood_tool/cli.py
```

### Interactive Visualization
Open the notebook in VS Code or Jupyter:
-   `notebooks/venice_exploration.ipynb`

**Expected Output:**
The script/notebook will print the number of fetched features, vulnerable buildings found, and list the top hotspot locations by density.

### Running Tests
Run the automated test suite (8 tests covering KDTree and Analysis logic).
```bash
pytest tests
```

