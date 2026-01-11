import json
import os
import sys

# Ensure we can find the flood_tool package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flood_tool.api import app

def generate_spec():
    print("Generating OpenAPI specification...")
    spec = app.openapi()
    with open("OPENAPI_SPEC.json", "w") as f:
        json.dump(spec, f, indent=2)
    print("[OK] OPENAPI_SPEC.json created.")

if __name__ == "__main__":
    generate_spec()
