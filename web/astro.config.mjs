import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://webglossdev.github.io/praca/",
  base: "/praca",
  build: {
    format: "directory",
  },
});
