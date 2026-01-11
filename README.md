# Flood Vulnerability Assessment Tool

This project implements a vector-based geospatial workflow for flood vulnerability and hotspot analysis. It determines which buildings are at risk based on their proximity to water bodies and identifies "hotspots" of high vulnerability density.

## Overview
The workflow implements a strictly vector-based approach to:
1.  **Ingest Data**: Fetch buildings and water bodies from OpenStreetMap (Overpass API).
2.  **Assess Vulnerability**: Identify buildings within a critical distance of water bodies.
3.  **Detect Hotspots**: Find clusters of vulnerable buildings using density estimation.

**Key Technical Features:**
-   **No Rasters**: All analysis is performed on vector data (points/nodes).
-   **Custom Algorithms**: Implements a `KDTree` for efficient spatial search (O(log n)).
-   **Local Projection**: Projects Lat/Lon coordinates to a local metric plane for accurate distance calculation.

## Project Structure
-   `flood_tool/data_loader.py`: Fetches OSM data via API.
-   `flood_tool/algorithms/kdtree.py`: Custom KD-Tree implementation.
-   `flood_tool/analysis.py`: Core logic for vulnerability and hotspot detection.
-   `flood_tool/utils.py`: Spatial utilities (Haversine, Projection).
-   `flood_tool/visualization.py`: Advanced Plotly and Folium map generation.
-   `flood_tool/cli.py`: CLI entry point to run the workflow for any location.
-   `flood_tool/api.py`: REST API wrapper for the tool (FastAPI).
-   `OPENAPI_SPEC.json`: Static OpenAPI 3.0 specification for the project.
-   `API_DOCUMENTATION.md`: Detailed documentation for the API layer.
-   `notebooks/venice_exploration.ipynb`: Interactive Jupyter notebook for the Venice case study.
-   `tests/`: Unit tests (pytest).
-   `pyproject.toml`: Poetry dependency management.

> [!NOTE]
> **Recommended IDE:** [Visual Studio Code](https://code.visualstudio.com/) is the recommended IDE for this project, as it provides excellent support for Python, Jupyter notebooks, and Poetry environments.

## How to Run

### Prerequisites
Ensure dependencies are installed using Poetry (or pip):
```bash
poetry install
# OR
pip install .
```

> [!TIP]
> **Windows Users:** If you encounter errors related to "path too long" or failures during installation (especially with `jupyter-widgets`), please refer to the [Troubleshooting Guide](./TROUBLESHOOTING.md) for solutions.

### Running the Workflow
The CLI is generic and can analyze any city by providing its name and bounding box coordinates:

**Example (Amsterdam):**
```bash
python flood_tool/cli.py "Amsterdam" 52.36 4.88 52.38 4.92
```

This generates 4 interactive HTML visualizations in the `outputs/` directory:
-   **Dot Map**: Individual building markers.
-   **Heatmap**: Vulnerability density heatmap.
-   **Choropleth**: Zone-level aggregation.
-   **Dashboard**: Statistics and rankings.

### Running the API (OpenAPI)
The tool can also be run as a REST API with interactive documentation:
```bash
poetry run uvicorn flood_tool.api:app --reload
```
View the interactive docs at: `http://localhost:8000/docs`

### Interactive Visualization
Alternatively, open the notebook for a step-by-step exploration:
-   `notebooks/venice_exploration.ipynb`

### Running Tests
Run the automated test suite:
```bash
pytest tests
```


