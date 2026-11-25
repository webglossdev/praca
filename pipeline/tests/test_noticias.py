# SPDX-License-Identifier: AGPL-3.0-or-later
from datetime import UTC, datetime

from praca_pipeline.noticias import normalizar_noticia, remover_duplicatas


def test_normaliza_trecho_e_remove_duplicatas_por_url() -> None:
    kwargs = {
        "titulo": "  Título   público ",
        "url": "https://news.example/materia?utm_source=rss#parte",
        "publicado_em": datetime(2026, 10, 6, tzinfo=UTC),
        "trecho": "  Um trecho curto.  ",
        "veiculo": "Agência Exemplo",
    }
    primeira = normalizar_noticia(noticia_id="n1", **kwargs)
    segunda = normalizar_noticia(noticia_id="n2", **kwargs)
    resultado = remover_duplicatas([primeira, segunda])
    assert primeira.titulo == "Título público"
    assert primeira.trecho == "Um trecho curto."
    assert len(resultado) == 1


def test_remove_parametros_de_rastreamento_ao_deduplicar() -> None:
    base = {
        "titulo": "Mesma notícia",
        "publicado_em": datetime(2026, 10, 6, tzinfo=UTC),
        "trecho": "Resumo curto.",
        "veiculo": "Agência Exemplo",
    }
    primeira = normalizar_noticia(
        noticia_id="n1",
        url="https://news.example/materia?id=123&utm_source=rss&fbclid=abc#topo",
        **base,
    )
    segunda = normalizar_noticia(
        noticia_id="n2",
        url="https://news.example/materia?id=123&utm_source=twitter&utm_medium=social&gclid=xyz",
        **base,
    )
    terceira = normalizar_noticia(
        noticia_id="n3",
        url="https://news.example/materia?id=456&utm_source=rss",
        **base,
    )
    resultado = remover_duplicatas([primeira, segunda, terceira])
    assert str(primeira.url) == "https://news.example/materia?id=123"
    assert str(primeira.url) == str(segunda.url)
    assert [item.id for item in resultado] == ["n1", "n3"]
