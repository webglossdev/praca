import { expect, test } from "@playwright/test";

test("home, search and people filters work", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page.goto("/pessoas");
  await expect(page.getByRole("heading", { name: "Pessoas" })).toBeVisible();
  await page.getByRole("button", { name: "Legislativo" }).click();
  await expect(page).toHaveURL(/poder=legislativo/);
  await page.goto("/busca?q=PEC");
  await expect(page.getByRole("heading", { name: "Buscar no Praça" })).toBeVisible();
});
