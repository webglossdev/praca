import { describe, expect, it } from "vitest";
import { formatBrl, initials } from "./pessoas";

describe("utilitários de dados de pessoas", () => {
  it("gera iniciais neutras a partir do nome público", () => {
    expect(initials("Maria da Silva")).toBe("MS");
  });

  it("formata valores válidos em reais", () => {
    expect(formatBrl(1234.5)).toBe("R$ 1.234,50");
  });

  it("preserva texto de valor não numérico", () => {
    expect(formatBrl("não informado")).toBe("não informado");
  });
});
