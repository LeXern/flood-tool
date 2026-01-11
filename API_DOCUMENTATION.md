# API Documentation & OpenAPI Specification

This project includes a RESTful API layer that allows programmatic access to the flood vulnerability analysis tool. It automatically provides interactive documentation via **FastAPI** and **Swagger UI**.

## 1. OpenAPI Specification

The formal API specification is provided in standard JSON format:
-   **File**: `OPENAPI_SPEC.json`

This file can be imported into tools like **Postman**, **Insomnia**, or any OpenAPI/Swagger editor for testing and code generation.

## 2. Running the API Server

You can start the interactive documentation server using Poetry:

```bash
poetry run uvicorn flood_tool.api:app --reload
```

Once running, you can access the documentation at:
-   **Interactive Swagger UI**: `http://localhost:8000/docs`

## 3. Endpoints Overview

### `GET /`
-   **Purpose**: Health check and metadata.
-   **Response**: Basic JSON status.

### `POST /analyze`
-   **Purpose**: Run a full flood risk analysis for a bounding box.
-   **Request Body**:
    ```json
    {
      "city_name": "Venice",
      "bbox": {
        "min_lat": 45.43,
        "min_lon": 12.31,
        "max_lat": 45.445,
        "max_lon": 12.34
      },
      "water_threshold": 50,
      "hotspot_radius": 100,
      "min_neighbors": 10
    }
    ```
-   **Response**: Quantitative results including percentage vulnerability and top hotspots.

### `GET /health`
-   **Purpose**: Basic uptime check.

## 4. Why provide an API?
In modern geospatial sciences, interoperability is key. By exposing our `KDTree` and analysis logic via a RESTful API, we allow other systems (Dashboards, Mobile Apps, or other Scientific pipelines) to leverage our work without needing to integrate the Python code directly.
