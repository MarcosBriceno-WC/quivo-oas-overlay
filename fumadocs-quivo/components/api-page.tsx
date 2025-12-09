import { openapi } from "@/lib/openapi";
import { createAPIPage } from "fumadocs-openapi/ui";
import defineClientConfig from "./api-page.client";

export const APIPage = createAPIPage(openapi, { client: defineClientConfig });
