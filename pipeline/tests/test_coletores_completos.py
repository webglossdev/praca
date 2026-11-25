# SPDX-License-Identifier: AGPL-3.0-or-later
"""Testes completos dos coletores adicionais, notícias RSS e métricas de posicionamento."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from praca_pipeline.coletores.legislativo_extra import (
    coletar_cota_camara,
    coletar_eventos_camara,
    coletar_votacoes_camara,
    coletar_votacoes_senado,
    parsear_ceaps_senado_csv,
)
from praca_pipeline.coletores.tse_cgu import (
    normalizar_agentes_publicos,
    normalizar_emendas_cgu,
    normalizar_sancoes_cgu,
    parsear_bens_tse_csv,
    parsear_candidaturas_tse_csv,
    parsear_doacoes_tse_csv,
    parsear_filiacoes_tse_csv,
    parsear_qsa_receita_csv,
)
from praca_pipeline.modelos.dominio import (
    Mandato,
    Pessoa,
    Poder,
    Proveniencia,
    StatusMandato,
    Votacao,
    Voto,
    VotoNominal,
)
from praca_pipeline.noticias import (
    detectar_desfecho_processual,
    parsear_feed_rss,
    vincular_pessoas_noticia,
)
from praca_pipeline.posicionamento import (
    calcular_indice_alinhamento,
    filtrar_votacoes_relevantes,
    validar_pesquisa_eleitoral,
)


class FakeCliente:
    def __init__(self, respostas: dict[str, Any]) -> None:
        self._respostas = respostas

    def get_json(
        self,
        url: str,
        *,
        params: dict[str, str] | None = None,
        fresh_for: int | None = None,
    ) -> Any:
        for prefixo, payload in self._respostas.items():
            if url.endswith(prefixo):
                return payload
        for prefixo, payload in self._respostas.items():
            if prefixo in url:
                return payload
        raise KeyError(f"URL sem mock: {url}")


def test_camara_votacoes_rejeita_janela_maior_que_90_dias() -> None:
    cliente = FakeCliente({})
    with pytest.raises(ValueError, match="90 dias"):
        coletar_votacoes_camara(
            cliente,  # type: ignore[arg-type]
            data_inicio=date(2026, 1, 1),
            data_fim=date(2026, 5, 1),
        )


def test_camara_votacoes_cota_e_eventos() -> None:
    cliente = FakeCliente(
        {
            "/api/v2/votacoes": {
                "dados": [
                    {
                        "id": "2401-1",
                        "data": "2026-10-01",
                        "aprovacao": 1,
                        "descricao": "Aprovado substitutivo",
                        "resultado": "Aprovada",
                        "siglaOrgao": "PL 123/2026",
                        "proposicaoId": "123",
                    }
                ]
            },
            "/2401-1/votos": {
                "dados": [
                    {
                        "tipoVoto": "Sim",
                        "deputado_": {
                            "nome": "Fulana de Tal",
                            "siglaPartido": "PV",
                            "siglaUf": "SP",
                        },
                    }
                ]
            },
            "/despesas": {
                "dados": [
                    {
                        "tipoDespesa": "DIVULGAÇÃO",
                        "valorLiquido": 1250.5,
                        "ano": 2026,
                        "mes": 9,
                    }
                ]
            },
            "/eventos": {
                "dados": [
                    {
                        "id": 99,
                        "descricaoTipo": "Sessão Deliberativa",
                        "dataHoraInicio": "2026-11-14T14:00:00",
                        "situacao": "Em Andamento",
                        "orgaos": [{"sigla": "PLEN"}],
                    }
                ]
            },
        }
    )

    votacoes = coletar_votacoes_camara(
        cliente,  # type: ignore[arg-type]
        data_inicio=date(2026, 9, 1),
        data_fim=date(2026, 10, 15),
    )
    assert len(votacoes) == 1
    assert votacoes[0].votos[0].escolha == "sim"
    assert votacoes[0].votos[0].pid == "pid_fulana-de-tal-sp"

    despesas = coletar_cota_camara(
        cliente,  # type: ignore[arg-type]
        id_camara=12345,
        pid="pid_fulana-de-tal-sp",
        ano=2026,
        coletado_em=datetime(2026, 10, 5, 12, 0, tzinfo=UTC),
    )
    assert len(despesas) == 1
    assert despesas[0].valor == Decimal("1250.5")

    eventos = coletar_eventos_camara(
        cliente,  # type: ignore[arg-type]
        data_inicio=date(2026, 11, 14),
        data_fim=date(2026, 11, 15),
    )
    assert eventos == [
        {
            "id": "99",
            "titulo": "Sessão Deliberativa",
            "orgao": "PLEN",
            "inicio": "2026-11-14T14:00:00",
            "situacao": "Em Andamento",
        }
    ]


def test_senado_votacoes_e_ceaps_latin1_com_metadados() -> None:
    cliente = FakeCliente(
        {
            "/dadosabertos/votacao.json": {
                "votacoes": [
                    {
                        "codigoSessaoVotacao": "7788",
                        "codigoMateria": "5566",
                        "dataSessao": "2026-09-20",
                        "resultado": "Aprovada",
                        "identificacao": "PEC 10/2026",
                        "votos": [
                            {
                                "nomeParlamentar": "João da Silva",
                                "siglaUF": "SP",
                                "siglaPartido": "MDB",
                                "siglaVoto": "Não",
                            }
                        ],
                    }
                ]
            }
        }
    )
    votacoes = coletar_votacoes_senado(
        cliente,  # type: ignore[arg-type]
        data_inicio=date(2026, 9, 1),
        data_fim=date(2026, 9, 30),
    )
    assert len(votacoes) == 1
    assert votacoes[0].casa == "senado"
    assert votacoes[0].votos[0].escolha == "nao"

    csv_bruto = (
        "ULTIMA_ATUALIZACAO=\"05/10/2026\"\n"
        "ANO;MES;SENADOR;UF;TIPO_DESPESA;VALOR_REEMBOLSADO\n"
        "2026;8;João da Silva;SP;Passagens aéreas;1.840,75\n"
    ).encode("latin-1")
    ceaps = parsear_ceaps_senado_csv(
        csv_bruto,
        coletado_em=datetime(2026, 10, 5, 12, 0, tzinfo=UTC),
    )
    assert len(ceaps) == 1
    assert ceaps[0].valor == Decimal("1840.75")
    assert ceaps[0].pid == "pid_joao-da-silva-sp"


def test_tse_receita_cgu_stf_executivo() -> None:
    agora = datetime(2026, 10, 5, 12, 0, tzinfo=UTC)

    candidaturas = parsear_candidaturas_tse_csv(
        "NM_CANDIDATO;NM_URNA_CANDIDATO;DS_CARGO;SG_UF;SG_PARTIDO;NM_PARTIDO;"
        "NR_PARTIDO;ANO_ELEICAO;DS_SIT_TOT_TURNO\n"
        "Carla Mendes;Carla Mendes;DEPUTADO FEDERAL;MG;PSD;Partido Social Democrático;"
        "55;2026;ELEITO POR QP\n",
        coletado_em=agora,
        posse_iniciada=False,
    )
    assert len(candidaturas) == 1
    assert candidaturas[0].pid == "pid_carla-mendes-mg"
    assert candidaturas[0].mandatos[0].status == StatusMandato.ELEITO_AGUARDANDO_POSSE

    bens = parsear_bens_tse_csv(
        "PID;DS_BEM_CANDIDATO;VR_BEM_CANDIDATO;ANO_ELEICAO\n"
        "pid_carla-mendes-mg;Apartamento residencial;450.000,00;2026\n",
        coletado_em=agora,
    )
    assert bens[0].valor == Decimal("450000.00")

    doacoes = parsear_doacoes_tse_csv(
        "PID;NM_DOADOR;VR_RECEITA;ANO_ELEICAO\n"
        "pid_carla-mendes-mg;Direção Nacional PSD;120.000,00;2026\n",
        coletado_em=agora,
    )
    assert doacoes[0].valor == Decimal("120000.00")

    filiacoes = parsear_filiacoes_tse_csv(
        "PID;SG_PARTIDO;DT_FILIACAO;DT_DESFILIACAO\n"
        "pid_carla-mendes-mg;PSD;10/03/2019;\n",
        coletado_em=agora,
    )
    assert filiacoes[0].partido_sigla == "PSD"

    qsa = parsear_qsa_receita_csv(
        "CNPJ_BASICO;NOME_SOCIO;CPF_CNPJ_SOCIO;QUALIFICACAO_SOCIO\n"
        "12345678;Fulana de Tal;***123456**;Sócio-Administrador\n"
    )
    assert qsa["12345678"][0]["cpf_cnpj_mascarado"] == "***123456**"

    emendas = normalizar_emendas_cgu(
        [
            {
                "pid": "pid_carla-mendes-mg",
                "localidadeDoGasto": "Belo Horizonte - MG",
                "valor": 250000,
            }
        ],
        coletado_em=agora,
    )
    assert emendas[0].valor_empenhado == Decimal("250000")

    sancoes = normalizar_sancoes_cgu(
        [
            {
                "cnpj": "12.345.678/0001-90",
                "razaoSocial": "Empresa Exemplo Ltda",
                "cadastro": "ceis",
                "motivo": "Inidoneidade",
                "dataInicioSancao": "2025-01-10",
            }
        ],
        coletado_em=agora,
    )
    assert sancoes[0].cadastro == "CEIS"

    agentes = normalizar_agentes_publicos(
        [{"nome": "Ministra Exemplo", "cargo": "Ministra do STF", "inicio": "2020-03-01"}],
        poder=Poder.JUDICIARIO,
        fonte_id="stf",
        url="https://portal.stf.jus.br",
        coletado_em=agora,
    )
    assert agentes[0].pid == "pid_ministra-exemplo-stf"


def test_rss_vinculacao_contextual_e_desfecho() -> None:
    xml_imprensa = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"><channel><item>
      <guid>item-1</guid>
      <title>Câmara analisa relatório</title>
      <link>https://jornal.example.org/camara?utm_source=x&amp;id=10</link>
      <pubDate>Mon, 05 Oct 2026 12:00:00 GMT</pubDate>
      <description>&lt;p&gt;Texto completo que deve virar só trecho.&lt;/p&gt;</description>
    </item></channel></rss>"""

    noticias_imprensa = parsear_feed_rss(
        xml_imprensa,
        veiculo="Jornal Exemplo",
        tipo_fonte="imprensa",
        licenca_aberta="CC-BY-4.0",
    )
    assert len(noticias_imprensa) == 1
    assert noticias_imprensa[0].corpo_integral == []
    assert noticias_imprensa[0].licenca_texto_integral is None

    noticias_oficiais = parsear_feed_rss(
        xml_imprensa,
        veiculo="Agência Câmara",
        tipo_fonte="oficial",
        licenca_aberta="CC BY 3.0 BR",
    )
    assert len(noticias_oficiais[0].corpo_integral) == 1

    pessoa = Pessoa(
        pid="pid_fulana-de-tal-uf",
        nome="Fulana de Tal",
        nome_publico="Fulana",
        slug="fulana-de-tal-uf",
        mandatos=[
            Mandato(
                poder=Poder.LEGISLATIVO,
                cargo="Deputada federal",
                uf="SP",
                inicio=date(2023, 2, 1),
                status=StatusMandato.ATIVO,
            )
        ],
        apelidos=["Fulana"],
        fontes=[
            Proveniencia(
                valor="Câmara",
                fonte_id="camara",
                url="https://dadosabertos.camara.leg.br",
                coletado_em=datetime(2026, 10, 5, 12, 0, tzinfo=UTC),
                licenca="dados públicos",
            )
        ],
    )
    vinculos_amb = vincular_pessoas_noticia("Fulana visitou uma feira agrícola.", [pessoa])
    assert vinculos_amb == []

    vinculos_ok = vincular_pessoas_noticia(
        "A deputada Fulana de Tal apresentou substitutivo no plenário da Câmara em SP.",
        [pessoa],
    )
    assert vinculos_ok and vinculos_ok[0][0] == "pid_fulana-de-tal-uf"
    assert vinculos_ok[0][1] >= 0.95

    assert detectar_desfecho_processual("O tribunal determinou inquérito arquivado.") == (
        "Inquérito arquivado"
    )
    assert detectar_desfecho_processual("Sessão ordinária sem decisão.") is None


def test_posicionamento_alinhamento_relevancia_e_pesquisa() -> None:
    votos = [
        VotoNominal(
            votacao_id="v1",
            proposicao_label="PL 100/2026",
            tema="Economia",
            data=date(2026, 10, 1),
            escolha="sim",
            orientacao_partido="Sim",
            orientacao_governo="Sim",
            resultado="Aprovada",
            url="https://dadosabertos.camara.leg.br/votacoes/v1",
        ),
        VotoNominal(
            votacao_id="v2",
            proposicao_label="PL 200/2026",
            tema="Educação",
            data=date(2026, 10, 2),
            escolha="nao",
            orientacao_partido="Sim",
            orientacao_governo="Não",
            resultado="Rejeitada",
            url="https://dadosabertos.camara.leg.br/votacoes/v2",
        ),
    ]
    assert calcular_indice_alinhamento(votos, alvo="partido", n_minimo=2) == 50.0
    assert calcular_indice_alinhamento(votos, alvo="governo", n_minimo=2) == 100.0

    votacoes = [
        Votacao(
            id="apertada",
            proposicao_id="p1",
            data=date(2026, 10, 1),
            resultado="Aprovada",
            votos=[
                Voto(pid="p1", escolha="sim"),
                Voto(pid="p2", escolha="sim"),
                Voto(pid="p3", escolha="nao"),
                Voto(pid="p4", escolha="nao"),
                Voto(pid="p5", escolha="sim"),
            ],
        ),
        Votacao(
            id="unanime",
            proposicao_id="p2",
            data=date(2026, 10, 2),
            resultado="Aprovada",
            votos=[Voto(pid=f"p{i}", escolha="sim") for i in range(10)],
        ),
    ]
    relevantes = filtrar_votacoes_relevantes(votacoes, margem_maxima=0.25, n_minimo=5)
    assert [v.id for v in relevantes] == ["apertada"]

    pesquisa = validar_pesquisa_eleitoral(
        {
            "registro_tse": "BR-01234/2026",
            "instituto": "Instituto Exemplo",
            "cargo": "Presidente",
            "data_divulgacao": "2026-09-25",
            "margem_erro_pp": 2.0,
            "percentual_candidato": 31.5,
        }
    )
    assert pesquisa.registro_tse == "BR-01234/2026"
    assert pesquisa.margem_erro_pp == 2.0
