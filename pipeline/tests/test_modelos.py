# SPDX-License-Identifier: AGPL-3.0-or-later
from datetime import datetime

import pytest
from praca_pipeline.convencoes import pid_para_slug, slugificar
from praca_pipeline.modelos import Partido, Pessoa
from pydantic import ValidationError


def test_slug_e_pid_sao_estaveis() -> None:
    assert slugificar("Fulana de Tal", "UF") == "fulana-de-tal-uf"
    assert pid_para_slug("pid_fulana-de-tal-uf") == "fulana-de-tal-uf"


def test_fixture_de_pessoa_valida() -> None:
    pessoa = Pessoa.model_validate_json(
        '{"pid":"pid_fulana-de-tal-uf","nome":"Fulana de Tal","nome_publico":"Fulana",'
        '"slug":"fulana-de-tal-uf","mandatos":[{"poder":"legislativo","cargo":"Deputada federal",'
        '"uf":"uf","inicio":"2023-02-01","status":"ativo"}],"fontes":[{"valor":"Câmara",'
        '"fonte_id":"camara","url":"https://dadosabertos.camara.leg.br","coletado_em":'
        '"2026-10-05T12:00:00Z","licenca":"dados públicos"}]}'
    )
    assert pessoa.mandatos[0].uf == "UF"
    assert pessoa.fontes[0].coletado_em == datetime.fromisoformat("2026-10-05T12:00:00+00:00")


def test_partido_aceita_nome_real_com_mais_de_12_caracteres() -> None:
    partido = Partido(sigla="SOLIDARIEDADE", nome="Solidariedade")
    assert partido.sigla == "SOLIDARIEDADE"


def test_extra_nao_e_silenciosamente_aceito() -> None:
    with pytest.raises(ValidationError):
        Pessoa.model_validate({"pid": "pid_a", "nome": "A", "nome_publico": "A",
                               "slug": "a-b", "mandatos": [], "fontes": [], "campo": "x"})
