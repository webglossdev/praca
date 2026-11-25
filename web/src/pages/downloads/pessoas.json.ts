import type { APIRoute } from "astro";
import { pessoas } from "../../data/pessoas";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(pessoas, null, 2) + "\n", {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
