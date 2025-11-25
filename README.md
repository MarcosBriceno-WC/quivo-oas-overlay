# Quivo OpenAPI Overlay

This repository contains a process to download the Quivo API OpenAPI specification and enhance it using OpenAPI Overlays.

## What is an OpenAPI Overlay?

An OpenAPI Overlay is a specification that allows you to apply modifications to an existing OpenAPI document without directly editing it. This is useful for:
- Adding descriptions and documentation
- Adding examples to requests/responses
- Enhancing metadata (tags, operation IDs, etc.)
- Maintaining customizations separately from the source spec

## Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Customize the Overlay

Edit `overlay.yaml` to add your desired modifications. The file contains examples for common operations:

```yaml
overlay: 1.0.0
info:
  title: Quivo API Overlay
  version: 1.0.0
actions:
  # Add description to an endpoint
  - target: $.paths./your-endpoint.get
    update:
      description: "Your description here"
      summary: "Brief summary"

  # Add request body example
  - target: $.paths./your-endpoint.post.requestBody.content.application/json
    update:
      example:
        field1: "value"
        field2: 123
```

### 2. Run the Process

Execute the script to download, enhance, and save the OpenAPI specification:

```bash
python apply_overlay.py
```

This will:
1. Download the OpenAPI spec from: `https://s3-eu-west-1.amazonaws.com/quivo-connector-prod-api-docs/swagger.json`
2. Apply the transformations defined in `overlay.yaml`
3. Save the enhanced specification to `openapi-enhanced.json`

### 3. View the Results

The enhanced OpenAPI specification will be saved as `openapi-enhanced.json` in the current directory.

## Overlay Syntax

The overlay file uses JSONPath-like syntax to target specific parts of the OpenAPI spec:

- `$.info` - Targets the info object
- `$.paths./endpoint.get` - Targets a specific GET operation
- `$.paths./endpoint.post.requestBody.content.application/json` - Targets request body content
- `$.paths./endpoint.get.responses.200` - Targets a specific response

### Common Actions

#### Update API Information
```yaml
- target: $.info
  update:
    description: "Enhanced API description"
```

#### Add Endpoint Description
```yaml
- target: $.paths./users.get
  update:
    summary: "List all users"
    description: "Retrieves a paginated list of all users"
```

#### Add Request Example
```yaml
- target: $.paths./users.post.requestBody.content.application/json
  update:
    example:
      name: "John Doe"
      email: "john@example.com"
```

#### Add Response Example
```yaml
- target: $.paths./users.get.responses.200.content.application/json
  update:
    example:
      - id: 1
        name: "John Doe"
      - id: 2
        name: "Jane Smith"
```

## File Structure

```
.
├── apply_overlay.py      # Main script to download and apply overlay
├── overlay.yaml          # Overlay specification with your customizations
├── requirements.txt      # Python dependencies
├── openapi-enhanced.json # Output file (generated)
└── README.md            # This file
```

## Troubleshooting

### Connection Errors
If you get connection errors when downloading the spec, check:
- Your internet connection
- The URL is accessible: `https://s3-eu-west-1.amazonaws.com/quivo-connector-prod-api-docs/swagger.json`

### Overlay Not Applied
If your overlay changes aren't showing up:
- Verify the target path matches the structure in the original spec
- Check the YAML syntax in `overlay.yaml`
- Look at the console output for any error messages

### Python Version
Make sure you're using Python 3.7 or higher:
```bash
python --version
```

## Next Steps

1. Explore the downloaded `openapi-enhanced.json` to see your API structure
2. Add more overlay actions to enhance documentation
3. Use the enhanced spec with tools like Swagger UI, Redoc, or API clients

## References

- [OpenAPI Overlay Specification](https://github.com/OAI/Overlay-Specification)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
