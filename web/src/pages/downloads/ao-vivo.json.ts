import type { APIRoute } from "astro";
import { aoVivo } from "../../data/portal";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(aoVivo, null, 2) + "\n", {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
