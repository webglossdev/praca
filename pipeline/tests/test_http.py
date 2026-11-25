# SPDX-License-Identifier: AGPL-3.0-or-later
import httpx
from praca_pipeline.http import (
    CircuitBreaker,
    CircuitoFonteAberto,
    ClienteFonte,
    DiskCache,
    HttpFonteError,
)


def test_cliente_re_tenta_e_salva_no_cache(tmp_path) -> None:
    chamadas = 0
    user_agents: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal chamadas
        chamadas += 1
        user_agents.append(request.headers["user-agent"])
        if chamadas == 1:
            return httpx.Response(503, request=request)
        return httpx.Response(200, json={"ok": True}, request=request)

    sleeps: list[float] = []
    client = httpx.Client(transport=httpx.MockTransport(handler))
    fonte = ClienteFonte(
        DiskCache(tmp_path),
        client=client,
        attempts=2,
        base_delay=0,
        sleeper=sleeps.append,
        random_fn=lambda: 0,
    )

    assert fonte.get_json("https://example.test/dados") == {"ok": True}
    assert chamadas == 2
    assert user_agents == ["PracaBot/0.1 (+https://praca.example)"] * 2
    assert fonte.get_json("https://example.test/dados") == {"ok": True}
    assert chamadas == 2


def test_cliente_explica_falha_depois_das_tentativas(tmp_path) -> None:
    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(500, request=request))
    )
    fonte = ClienteFonte(
        DiskCache(tmp_path),
        client=client,
        attempts=2,
        base_delay=0,
        sleeper=lambda _: None,
    )

    try:
        fonte.get_json("https://example.test/indisponivel")
    except HttpFonteError as error:
        assert "indisponivel" in str(error)
    else:
        raise AssertionError("era esperada falha após as tentativas")


def test_circuit_breaker_abre_apos_falhas_e_sonda_apos_cooldown() -> None:
    agora = [0.0]
    circuito = CircuitBreaker(threshold=3, cooldown=10, clock=lambda: agora[0])
    for _ in range(3):
        circuito.record_failure()
    try:
        circuito.before_request()
    except CircuitoFonteAberto:
        pass
    else:
        raise AssertionError("era esperado circuito aberto")
    agora[0] = 10.0
    circuito.before_request()
    circuito.record_success()
    circuito.before_request()


def test_fallback_stale_preserva_snapshot_e_marca_degradacao(tmp_path) -> None:
    cache = DiskCache(tmp_path)
    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(503, request=request))
    )
    fonte = ClienteFonte(
        cache,
        client=client,
        attempts=1,
        sleeper=lambda _: None,
        circuit_breaker=CircuitBreaker(threshold=1, cooldown=60),
    )
    cache.set("https://example.test/snapshot?", {"versao": 1})

    assert fonte.get_json("https://example.test/snapshot", fresh_for=0) == {"versao": 1}
    assert fonte.degraded is True
    assert fonte.last_snapshot_age is not None
