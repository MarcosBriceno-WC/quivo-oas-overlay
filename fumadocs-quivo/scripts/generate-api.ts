// scripts/generate-docs.ts
import { generateFiles } from 'fumadocs-openapi';
import { createOpenAPI } from 'fumadocs-openapi/server';

const openapi = createOpenAPI({
  input: ['../content/docs/api-reference/openapi.json'], 
});

void generateFiles({
  input: openapi,
  output: '../content/docs/api-reference/endpoints', 
  includeDescription: true, 
});

