# SPDX-License-Identifier: AGPL-3.0-or-later
"""Normalização, parser RSS, vinculação contextual e detecção de desfecho de notícias."""

from __future__ import annotations

import re
import unicodedata
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from praca_pipeline.modelos.dominio import Noticia, Pessoa, Poder

_PARAMETROS_RASTREAMENTO = {"fbclid", "gclid"}
_HTML_TAGS = re.compile(r"<[^>]+>")
_TOKENS_POLITICOS = (
    "deputad",
    "senad",
    "ministr",
    "governador",
    "president",
    "parlamentar",
    "congresso",
    "camara",
    "senado",
    "stf",
    "plenario",
    "bancada",
    "partido",
    "lider",
    "comissao",
)
_DESFECHOS = (
    ("inquerito arquivado", "Inquérito arquivado"),
    ("arquivamento do inquerito", "Inquérito arquivado"),
    ("absolvido", "Absolvido"),
    ("absolvida", "Absolvida"),
    ("extinta a punibilidade", "Extinção da punibilidade"),
    ("processo prescrito", "Processo prescrito"),
    ("denuncia rejeitada", "Denúncia rejeitada"),
    ("retratacao", "Retratação registrada"),
)


def _sem_acentos(texto: str) -> str:
    norm = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(norm.casefold().split())


def _limpar_query(query: str) -> str:
    if not query:
        return ""
    pares = [
        (chave, valor)
        for chave, valor in parse_qsl(query, keep_blank_values=True)
        if not chave.lower().startswith("utm_")
        and chave.lower() not in _PARAMETROS_RASTREAMENTO
    ]
    return urlencode(pares)


def _limpar_html(bruto: str) -> str:
    sem_tags = _HTML_TAGS.sub(" ", bruto)
    return " ".join(sem_tags.split())


def normalizar_noticia(
    *,
    noticia_id: str,
    titulo: str,
    url: str,
    publicado_em: datetime,
    trecho: str,
    veiculo: str,
    poder: Poder | None = None,
    tema: str | None = None,
    tipo_fonte: str = "imprensa",
    licenca_texto_integral: str | None = None,
    corpo_integral: list[str] | None = None,
    pessoa_pids: list[str] | None = None,
) -> Noticia:
    partes = urlsplit(url.strip())
    if partes.scheme not in {"http", "https"} or not partes.netloc:
        raise ValueError("notícia exige URL HTTP válida")
    query_limpa = _limpar_query(partes.query)
    url_canonica = urlunsplit((partes.scheme, partes.netloc, partes.path, query_limpa, ""))
    if publicado_em.tzinfo is None:
        publicado_em = publicado_em.replace(tzinfo=UTC)

    paragrafos: list[str] = []
    if corpo_integral and tipo_fonte == "oficial" and licenca_texto_integral:
        paragrafos = [p.strip() for p in corpo_integral if p.strip()]

    return Noticia(
        id=noticia_id,
        titulo=" ".join(titulo.split()),
        veiculo=veiculo.strip(),
        publicado_em=publicado_em,
        url=url_canonica,
        trecho=" ".join(trecho.split())[:500],
        pessoa_pids=pessoa_pids or [],
        poder=poder,
        tema=tema,
        tipo_fonte=tipo_fonte,
        licenca_texto_integral=licenca_texto_integral if paragrafos else None,
        corpo_integral=paragrafos,
    )


def remover_duplicatas(noticias: list[Noticia]) -> list[Noticia]:
    """Mantém a primeira ocorrência de cada URL canônica, preservando a ordem."""

    vistas: set[str] = set()
    resultado: list[Noticia] = []
    for noticia in noticias:
        chave = str(noticia.url)
        if chave not in vistas:
            vistas.add(chave)
            resultado.append(noticia)
    return resultado


def parsear_feed_rss(
    xml_texto: str,
    *,
    veiculo: str,
    tipo_fonte: str = "imprensa",
    licenca_aberta: str | None = None,
    poder: Poder | None = None,
) -> list[Noticia]:
    """Converte feed RSS/Atom para itens normalizados sem republicar matéria sem licença."""

    raiz = ET.fromstring(xml_texto)
    itens = raiz.findall(".//item") or raiz.findall(".//{http://www.w3.org/2005/Atom}entry")
    noticias: list[Noticia] = []

    for indice, item in enumerate(itens, start=1):
        titulo = (
            item.findtext("title")
            or item.findtext("{http://www.w3.org/2005/Atom}title")
            or ""
        )
        link = item.findtext("link")
        if not link:
            atom_link = item.find("{http://www.w3.org/2005/Atom}link")
            link = atom_link.attrib.get("href", "") if atom_link is not None else ""
        descricao = (
            item.findtext("description")
            or item.findtext("{http://www.w3.org/2005/Atom}summary")
            or titulo
        )
        data_raw = (
            item.findtext("pubDate")
            or item.findtext("{http://www.w3.org/2005/Atom}updated")
            or ""
        )
        try:
            publicado_em = parsedate_to_datetime(data_raw) if data_raw else datetime.now(UTC)
        except (TypeError, ValueError):
            publicado_em = datetime.fromisoformat(data_raw) if data_raw else datetime.now(UTC)

        limpo = _limpar_html(descricao)
        corpo = [limpo] if (tipo_fonte == "oficial" and licenca_aberta and limpo) else None
        guid = item.findtext("guid") or f"{veiculo.lower().replace(' ', '-')}-{indice}"
        noticias.append(
            normalizar_noticia(
                noticia_id=re.sub(r"[^a-z0-9-]+", "-", guid.lower()).strip("-")[:48],
                titulo=titulo,
                url=link,
                publicado_em=publicado_em,
                trecho=limpo,
                veiculo=veiculo,
                poder=poder,
                tipo_fonte=tipo_fonte,
                licenca_texto_integral=licenca_aberta,
                corpo_integral=corpo,
            )
        )
    return remover_duplicatas(noticias)


def vincular_pessoas_noticia(texto: str, pessoas: list[Pessoa]) -> list[tuple[str, float]]:
    """Vincula nomes/apelidos a perfis apenas quando confiança >= 0.95 (regra anti-homônimo)."""

    normalizado = _sem_acentos(texto)
    tem_contexto = any(token in normalizado for token in _TOKENS_POLITICOS)
    candidatos: list[tuple[str, float]] = []

    for pessoa in pessoas:
        nomes_completos = [_sem_acentos(pessoa.nome), _sem_acentos(pessoa.nome_publico)]
        apelidos = [_sem_acentos(a) for a in pessoa.apelidos if a.strip()]

        melhor_confianca = 0.0
        for candidato in nomes_completos:
            palavras = candidato.split()
            if len(palavras) >= 2 and re.search(rf"\b{re.escape(candidato)}\b", normalizado):
                score = 0.85 + (0.14 if tem_contexto else 0.0)
                melhor_confianca = max(melhor_confianca, score)

        for apelido in apelidos:
            if apelido and re.search(rf"\b{re.escape(apelido)}\b", normalizado):
                if len(apelido.split()) < 2:
                    continue
                uf_match = bool(
                    pessoa.mandatos[0].uf
                    and re.search(rf"\b{pessoa.mandatos[0].uf.lower()}\b", normalizado)
                )
                score = 0.65 + (0.18 if tem_contexto else 0.0) + (0.14 if uf_match else 0.0)
                melhor_confianca = max(melhor_confianca, score)

        if melhor_confianca >= 0.95:
            candidatos.append((pessoa.pid, round(min(1.0, melhor_confianca), 2)))

    if not candidatos:
        return []
    candidatos.sort(key=lambda item: item[1], reverse=True)
    melhor = candidatos[0][1]
    empatados = [item for item in candidatos if melhor - item[1] < 0.05]
    if len(empatados) > 1:
        return []

    return [candidatos[0]]


def detectar_desfecho_processual(texto: str) -> str | None:
    """Identifica termos jurídicos que disparam atualização prioritária em atribuições."""

    normalizado = _sem_acentos(texto)
    for chave, rotulo in _DESFECHOS:
        if chave in normalizado:
            return rotulo
    return None
