# SPDX-License-Identifier: AGPL-3.0-or-later
"""Contratos mínimos do domínio público do Praça."""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

T = TypeVar("T")


class Contrato(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class StatusMandato(StrEnum):
    ATIVO = "ativo"
    ELEITO_AGUARDANDO_POSSE = "eleito_aguardando_posse"
    LICENCIADO = "licenciado"
    SUPLENTE_EM_EXERCICIO = "suplente_em_exercicio"
    ENCERRADO = "encerrado"


class Poder(StrEnum):
    LEGISLATIVO = "legislativo"
    EXECUTIVO = "executivo"
    JUDICIARIO = "judiciario"


class Proveniencia[T](Contrato):
    valor: T
    fonte_id: str = Field(min_length=2)
    url: HttpUrl
    coletado_em: datetime
    licenca: str = Field(min_length=2)


class Fonte(Contrato):
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]+$")
    nome: str
    url: HttpUrl
    licenca: str
    frequencia: str


class Partido(Contrato):
    sigla: str = Field(min_length=2, max_length=32)
    nome: str
    numero: int | None = Field(default=None, ge=1, le=99)
    federacao: str | None = None
    historico_nomes: list[str] = Field(default_factory=list)


class Mandato(Contrato):
    poder: Poder
    cargo: str
    uf: str | None = Field(default=None, min_length=2, max_length=2)
    inicio: date
    fim: date | None = None
    status: StatusMandato
    titular_pid: str | None = None

    @field_validator("uf")
    @classmethod
    def uf_maiuscula(cls, value: str | None) -> str | None:
        return value.upper() if value else value


class Filiacao(Contrato):
    pid: str
    partido_sigla: str
    inicio: date
    fim: date | None = None
    fonte: Proveniencia[str]


class Proposicao(Contrato):
    id: str
    casa: str
    tipo: str
    numero: int
    ano: int = Field(ge=1900, le=2200)
    ementa: str
    url: HttpUrl


class Voto(Contrato):
    pid: str
    escolha: str = Field(pattern=r"^(sim|nao|abstencao|ausente|obstrucao|licenca)$")
    nome: str | None = None
    partido: str | None = None
    uf: str | None = None


class Votacao(Contrato):
    id: str
    proposicao_id: str
    data: date
    resultado: str
    votos: list[Voto]
    casa: str | None = None
    proposicao_label: str | None = None
    titulo: str | None = None
    tema: str | None = None
    url: HttpUrl | None = None


class VotoNominal(Contrato):
    votacao_id: str
    proposicao_label: str
    tema: str
    data: date
    escolha: str = Field(pattern=r"^(sim|nao|abstencao|ausente|obstrucao|licenca)$")
    orientacao_partido: str | None = None
    orientacao_governo: str | None = None
    resultado: str
    url: HttpUrl


class Despesa(Contrato):
    pid: str
    categoria: str
    valor: Decimal = Field(ge=0)
    competencia: date
    fonte: Proveniencia[Decimal]


class Doacao(Contrato):
    candidato_pid: str
    doador: str
    valor: Decimal = Field(gt=0)
    ano_eleitoral: int
    fonte: Proveniencia[Decimal]


class Bem(Contrato):
    pid: str
    descricao: str
    valor: Decimal = Field(ge=0)
    ano_eleitoral: int
    fonte: Proveniencia[Decimal]


class Emenda(Contrato):
    parlamentar_pid: str
    favorecido: str
    valor_empenhado: Decimal = Field(ge=0)
    ano: int
    fonte: Proveniencia[Decimal]


class SancaoEmpresa(Contrato):
    cnpj: str
    razao_social: str
    cadastro: str
    motivo: str
    data_inicio: date
    data_fim: date | None = None
    fonte: Proveniencia[str]


class Posicionamento(Contrato):
    autodeclaracao: Proveniencia[str] | None = None
    alinhamento_partido_pct: float | None = Field(default=None, ge=0, le=100)
    alinhamento_governo_pct: float | None = Field(default=None, ge=0, le=100)
    classificacao_partido: Proveniencia[str] | None = None
    metodologia_url: str = "/metodologia#posicionamento"


class PesquisaEleitoral(Contrato):
    registro_tse: str
    instituto: str
    cargo: str
    data_divulgacao: date
    margem_erro_pp: float = Field(gt=0)
    confianca_pct: float = Field(gt=0, le=100)
    percentual_candidato: float = Field(ge=0, le=100)
    fonte: Proveniencia[str]


class EventoAoVivo(Contrato):
    id: str
    poder: Poder
    orgao: str
    titulo: str
    status: str = Field(pattern=r"^(ao_vivo|agendado|encerrado|indisponivel)$")
    horario: str
    pauta: str
    youtube_id: str | None = None
    fonte: Proveniencia[str]


class CorrecaoPublica(Contrato):
    id: str
    data: date
    pagina: str
    campo: str
    alteracao: str
    motivo: str
    fonte_url: HttpUrl


class StatusColetor(Contrato):
    fonte_id: str
    nome: str
    status: str = Field(pattern=r"^(ativa|degradada|quebrada|planejada)$")
    ultima_coleta: datetime | None = None
    latencia_ms: int | None = Field(default=None, ge=0)
    circuit_breaker: str = Field(default="fechado", pattern=r"^(fechado|aberto|meio_aberto)$")
    observacao: str = ""


class Noticia(Contrato):
    id: str
    titulo: str
    veiculo: str
    publicado_em: datetime
    url: HttpUrl
    trecho: str = Field(max_length=500)
    pessoa_pids: list[str] = Field(default_factory=list)
    poder: Poder | None = None
    tema: str | None = None
    tipo_fonte: str = Field(default="imprensa", pattern=r"^(oficial|imprensa)$")
    licenca_texto_integral: str | None = None
    corpo_integral: list[str] = Field(default_factory=list)


class Atribuicao(Contrato):
    noticia_id: str
    rotulo: str = "Segundo a imprensa"
    desfecho: str | None = None
    atualizado_em: date | None = None
    status: str | None = None
    titulo_noticia: str | None = None
    veiculo: str | None = None
    data: date | None = None
    url: HttpUrl | None = None


class Pessoa(Contrato):
    pid: str = Field(pattern=r"^pid_[a-z0-9-]+$")
    nome: str
    nome_publico: str
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
    mandatos: list[Mandato] = Field(min_length=1)
    partido: Partido | None = None
    apelidos: list[str] = Field(default_factory=list)
    fontes: list[Proveniencia[str]] = Field(min_length=1)
    biografia: Proveniencia[str] | None = None
    resumo_numeros: dict[str, Proveniencia[str]] = Field(default_factory=dict)
    filiacoes: list[Filiacao] = Field(default_factory=list)
    proposicoes: list[Proposicao] = Field(default_factory=list)
    votos_recentes: list[VotoNominal] = Field(default_factory=list)
    despesas: list[Despesa] = Field(default_factory=list)
    emendas: list[Emenda] = Field(default_factory=list)
    doacoes: list[Doacao] = Field(default_factory=list)
    bens: list[Bem] = Field(default_factory=list)
    sancoes_empresas: list[SancaoEmpresa] = Field(default_factory=list)
    posicionamento: Posicionamento | None = None
    plano_governo: Proveniencia[str] | None = None
    pesquisas: list[PesquisaEleitoral] = Field(default_factory=list)
    noticias_ids: list[str] = Field(default_factory=list)
    atribuicoes: list[Atribuicao] = Field(default_factory=list)
