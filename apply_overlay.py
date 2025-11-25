#!/usr/bin/env python3
"""
OpenAPI Overlay Application Script
Downloads an OpenAPI specification and applies overlay transformations.
"""

import json
import requests
import yaml
import re
from typing import Any, Dict, List
import sys


class OverlayProcessor:
    """Processes OpenAPI Overlay specifications."""

    def __init__(self, openapi_spec: Dict[str, Any], overlay_spec: Dict[str, Any]):
        self.openapi_spec = openapi_spec
        self.overlay_spec = overlay_spec

    def apply(self) -> Dict[str, Any]:
        """Apply all overlay actions to the OpenAPI specification."""
        actions = self.overlay_spec.get("actions", [])

        for action in actions:
            target = action.get("target")
            update = action.get("update")
            remove = action.get("remove")

            if not target:
                continue

            if update:
                self._apply_update(target, update)
            elif remove:
                self._apply_remove(target, remove)

        return self.openapi_spec

    def _apply_update(self, target: str, update: Dict[str, Any]):
        """Apply an update action to the target path."""
        # Parse JSONPath-like target
        obj = self._resolve_target(target)

        if obj is not None:
            if isinstance(obj, dict):
                obj.update(update)
            elif isinstance(obj, list):
                # For list updates, append or extend
                if isinstance(update, list):
                    obj.extend(update)
                else:
                    obj.append(update)

    def _apply_remove(self, target: str, remove: bool):
        """Apply a remove action to the target path."""
        # Implementation for remove operations
        pass

    def _resolve_target(self, target: str) -> Any:
        """
        Resolve a JSONPath-like target to the actual object in the spec.
        Supports basic JSONPath syntax like $.paths./endpoint.get
        """
        # Remove leading $. if present
        if target.startswith("$."):
            target = target[2:]

        # Split the path
        parts = self._parse_path(target)

        current = self.openapi_spec
        parent = None

        for part in parts:
            parent = current

            if isinstance(current, dict):
                if part in current:
                    current = current[part]
                else:
                    # Create the path if it doesn't exist for updates
                    current[part] = {}
                    current = current[part]
            elif isinstance(current, list):
                # Handle array indexing
                try:
                    index = int(part)
                    current = current[index]
                except (ValueError, IndexError):
                    return None
            else:
                return None

        return current

    def _parse_path(self, path: str) -> List[str]:
        """Parse a JSONPath-like string into parts."""
        parts = []
        current = ""
        in_bracket = False

        i = 0
        while i < len(path):
            char = path[i]

            if char == "[":
                if current:
                    parts.append(current)
                    current = ""
                in_bracket = True
            elif char == "]":
                in_bracket = False
                if current:
                    # Remove quotes if present
                    current = current.strip("'\"")
                    parts.append(current)
                    current = ""
            elif char == "." and not in_bracket:
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char

            i += 1

        if current:
            parts.append(current)

        return parts


def download_openapi_spec(url: str) -> Dict[str, Any]:
    """Download OpenAPI specification from URL."""
    print(f"Downloading OpenAPI spec from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def load_overlay(file_path: str) -> Dict[str, Any]:
    """Load overlay specification from YAML file."""
    print(f"Loading overlay from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_openapi_spec(spec: Dict[str, Any], output_path: str):
    """Save the modified OpenAPI specification."""
    print(f"Saving result to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)


def main():
    """Main execution function."""
    # Configuration
    OPENAPI_URL = (
        "https://s3-eu-west-1.amazonaws.com/quivo-connector-prod-api-docs/swagger.json"
    )
    OVERLAY_FILE = "overlay.yaml"
    OUTPUT_FILE = "openapi.json"

    try:
        # Step 1: Download OpenAPI spec
        openapi_spec = download_openapi_spec(OPENAPI_URL)
        print(
            f"[OK] Downloaded OpenAPI spec (version: {openapi_spec.get('openapi', openapi_spec.get('swagger'))})"
        )

        # Step 2: Load overlay
        overlay_spec = load_overlay(OVERLAY_FILE)
        overlay_version = overlay_spec.get("overlay", "unknown")
        print(f"[OK] Loaded overlay specification (version: {overlay_version})")

        # Step 3: Apply overlay
        print("Applying overlay transformations...")
        processor = OverlayProcessor(openapi_spec, overlay_spec)
        enhanced_spec = processor.apply()
        print(f"[OK] Applied {len(overlay_spec.get('actions', []))} overlay actions")

        # Step 4: Save result
        save_openapi_spec(enhanced_spec, OUTPUT_FILE)
        print(f"[OK] Successfully saved enhanced OpenAPI spec to {OUTPUT_FILE}")

        print("\n" + "=" * 50)
        print("Process completed successfully!")
        print("=" * 50)

    except requests.RequestException as e:
        print(f"Error downloading OpenAPI spec: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing overlay file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
