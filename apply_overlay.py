"""
OpenAPI Overlay Application Script
Downloads an OpenAPI specification and applies overlay transformations.
Supports advanced JSONPath filter expressions for bulk updates on parameters.
"""

import json
import requests
import yaml
from typing import Any, Dict, List
import sys
import re


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
        # Check if target contains filter expressions
        if self._is_filter_expression(target):
            self._apply_filter_update(target, update)
        else:
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

        for part in parts:

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

    def _is_filter_expression(self, target: str) -> bool:
        """Check if the target contains JSONPath filter expressions."""
        return '?(@.' in target or '[*]' in target or '.*' in target

    def _apply_filter_update(self, target: str, update: Dict[str, Any]):
        """Apply updates to all paths matching a filter expression."""
        # Parse the filter expression
        # Example: $.paths.*[?(@.parameters[?(@.name == 'sellerId')])]

        # Extract the base path and filter
        match = re.match(r'\$\.paths\.\*\[\?\(@\.parameters\[\?\(@\.name == [\'"](.+?)[\'"]\)\]\)\]', target)

        if match:
            param_name = match.group(1)
            # Find all matching parameter paths
            targets = find_parameter_paths(self.openapi_spec, param_name)

            print(f"  Filter expression matched {len(targets)} parameters for '{param_name}'")

            for target_info in targets:
                # Apply update to each matching parameter
                obj = self._resolve_target(target_info['target'])
                if obj is not None and isinstance(obj, dict):
                    obj.update(update)
            return

        # Handle more generic filter patterns
        # Example: $.paths.*.get.parameters[?(@.name == 'sellerId')]
        match = re.match(r'\$\.paths\.(.+?)\.(.+?)\.parameters\[\?\(@\.name == [\'"](.+?)[\'"]\)\]', target)

        if match:
            path_pattern = match.group(1)
            method_pattern = match.group(2)
            param_name = match.group(3)

            if path_pattern == '*' and method_pattern == '*':
                # Match all paths and methods
                targets = find_parameter_paths(self.openapi_spec, param_name)
            elif path_pattern == '*':
                # Match all paths with specific method
                targets = [t for t in find_parameter_paths(self.openapi_spec, param_name)
                          if t['method'] == method_pattern]
            elif method_pattern == '*':
                # Match specific path with all methods
                targets = [t for t in find_parameter_paths(self.openapi_spec, param_name)
                          if t['path'] == path_pattern]
            else:
                # Match specific path and method
                targets = [t for t in find_parameter_paths(self.openapi_spec, param_name)
                          if t['path'] == path_pattern and t['method'] == method_pattern]

            print(f"  Filter expression matched {len(targets)} parameters for '{param_name}'")

            for target_info in targets:
                obj = self._resolve_target(target_info['target'])
                if obj is not None and isinstance(obj, dict):
                    obj.update(update)
            return

        # If no pattern matched, log warning
        print(f"  Warning: Could not parse filter expression: {target}", file=sys.stderr)


def download_and_convert_spec(url: str) -> Dict[str, Any]:
    """Download and convert OpenAPI specification to OpenAPI 3.0."""
    print(f"Downloading and converting spec from {url}...")
    converter_url = "https://converter.swagger.io/api/convert"

    try:
        response = requests.get(
            converter_url,
            params={"url": url},
            timeout=60
        )
        response.raise_for_status()
        converted_spec = response.json()
        print(f"[OK] Downloaded and converted to OpenAPI {converted_spec.get('openapi', '3.0')}")
        return converted_spec
    except requests.RequestException as e:
        print(f"Warning: Conversion failed: {e}", file=sys.stderr)
        print("Falling back to direct download...")
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


def find_parameter_paths(openapi_spec: Dict[str, Any], param_name: str) -> List[Dict[str, Any]]:
    """Find all paths where a specific parameter appears.

    Used internally by the filter expression processor.
    """
    parameter_targets = []

    if 'paths' not in openapi_spec:
        return parameter_targets

    for path, path_item in openapi_spec['paths'].items():
        for method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace']:
            if method not in path_item:
                continue

            operation = path_item[method]
            if 'parameters' not in operation:
                continue

            for idx, param in enumerate(operation['parameters']):
                # Handle both inline parameters and $ref parameters
                param_name_check = param.get('name', '')
                if param_name_check == param_name:
                    target = f"$.paths.{path}.{method}.parameters[{idx}]"
                    parameter_targets.append({
                        'path': path,
                        'method': method,
                        'index': idx,
                        'target': target
                    })

    return parameter_targets


def main():
    """Main execution function."""
    # Configuration
    OPENAPI_URL = (
        "https://s3-eu-west-1.amazonaws.com/quivo-connector-prod-api-docs/swagger.json"
    )
    OVERLAY_FILE = "overlay.yaml"
    OUTPUT_FILE = "openapi.json"

    try:
        # Step 1: Download and convert to OpenAPI 3.0
        openapi_spec = download_and_convert_spec(OPENAPI_URL)

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
