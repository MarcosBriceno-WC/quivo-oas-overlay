import requests
from typing import Any, Dict, List
import sys
import json
import yaml


def download_and_convert_spec(url: str) -> Dict[str, Any]:
    """Download and convert OpenAPI specification to OpenAPI 3.0."""
    print(f"Downloading and converting spec from {url}...")
    converter_url = "https://converter.swagger.io/api/convert"

    try:
        response = requests.get(converter_url, params={"url": url}, timeout=60)
        response.raise_for_status()
        converted_spec = response.json()
        print(
            f"[OK] Downloaded and converted to OpenAPI {converted_spec.get('openapi', '3.0')}"
        )
        return converted_spec
    except requests.RequestException as e:
        print(f"Warning: Conversion failed: {e}", file=sys.stderr)
        print("Falling back to direct download...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()


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
        # Step 1: Download and convert to OpenAPI 3.0
        openapi_spec = download_and_convert_spec(OPENAPI_URL)

        save_openapi_spec(openapi_spec, OUTPUT_FILE)

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
