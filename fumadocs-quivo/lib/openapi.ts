// lib/openapi.ts
import { createOpenAPI } from 'fumadocs-openapi/server';

export const openapi = createOpenAPI({
  // Specify the path to your OpenAPI schema file(s) (JSON or YAML)
  input: ['../openapi.json'], 
  // Optionally, you can set a proxyUrl for the interactive playground 
  // if your API doesn't have CORS configured correctly.
  // proxyUrl: '/api/proxy', 
});