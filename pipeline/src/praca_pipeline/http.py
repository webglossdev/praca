# SPDX-License-Identifier: AGPL-3.0-or-later
"""Cliente HTTP resiliente para fontes públicas."""

from __future__ import annotations

import hashlib
import json
import random
import time
from collections.abc import Callable
from pathlib import Path

import httpx


class HttpFonteError(RuntimeError):
    """Erro de coleta após esgotar as tentativas configuradas."""


class CircuitoFonteAberto(HttpFonteError):
    """A fonte está temporariamente bloqueada após falhas consecutivas."""


class CircuitBreaker:
    """Bloqueia chamadas após falhas consecutivas e permite uma sonda após cooldown."""

    def __init__(
        self,
        threshold: int = 3,
        cooldown: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if threshold < 1:
            raise ValueError("threshold deve ser maior que zero")
        if cooldown < 0:
            raise ValueError("cooldown não pode ser negativo")
        self.threshold = threshold
        self.cooldown = cooldown
        self.clock = clock
        self.failures = 0
        self.opened_at: float | None = None

    def before_request(self) -> None:
        if self.opened_at is None:
            return
        if self.clock() - self.opened_at < self.cooldown:
            raise CircuitoFonteAberto("circuito da fonte está aberto")
        self.opened_at = None

    def record_success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.opened_at = self.clock()


class DiskCache:
    """Cache JSON simples e atômico, indexado pela URL e parâmetros."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.directory / f"{digest}.json"

    def get(self, key: str) -> dict | list | None:
        path = self._path(key)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise HttpFonteError(f"cache corrompido: {path}") from exc

    def get_with_age(self, key: str) -> tuple[dict | list | None, float | None]:
        value = self.get(key)
        if value is None:
            return None, None
        try:
            age = max(0.0, time.time() - self._path(key).stat().st_mtime)
        except OSError as exc:
            path = self._path(key)
            raise HttpFonteError(f"não foi possível ler a idade do cache: {path}") from exc
        return value, age

    def set(self, key: str, value: dict | list) -> None:
        path = self._path(key)
        temporary = path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(path)


class TokenBucket:
    """Limita chamadas por segundo sem bloquear na primeira chamada."""

    def __init__(self, rate: float, clock: Callable[[], float] = time.monotonic) -> None:
        if rate <= 0:
            raise ValueError("rate deve ser maior que zero")
        self.rate = rate
        self.clock = clock
        self.available_at = 0.0

    def wait(self, sleeper: Callable[[float], None] = time.sleep) -> None:
        now = self.clock()
        delay = max(0.0, self.available_at - now)
        if delay:
            sleeper(delay)
            now += delay
        self.available_at = now + (1 / self.rate)


class ClienteFonte:
    """GET JSON com User-Agent, cache local, retry e backoff com jitter."""

    def __init__(
        self,
        cache: DiskCache,
        *,
        user_agent: str = "PracaBot/0.1 (+https://praca.example)",
        rate: float = 2.0,
        attempts: int = 3,
        base_delay: float = 0.5,
        client: httpx.Client | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        random_fn: Callable[[], float] = random.random,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        if attempts < 1:
            raise ValueError("attempts deve ser maior que zero")
        self.cache = cache
        self.client = client or httpx.Client()
        self.headers = {"User-Agent": user_agent, "Accept": "application/json"}
        self.bucket = TokenBucket(rate)
        self.attempts = attempts
        self.base_delay = base_delay
        self.sleeper = sleeper
        self.random_fn = random_fn
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.degraded = False
        self.last_snapshot_age: float | None = None

    def get_json(
        self,
        url: str,
        *,
        params: dict[str, str] | None = None,
        fresh_for: float | None = None,
    ) -> dict | list:
        if fresh_for is not None and fresh_for < 0:
            raise ValueError("fresh_for não pode ser negativo")
        query = httpx.QueryParams(params or {})
        key = f"{url}?{query}"
        cached, age = self.cache.get_with_age(key)
        self.degraded = False
        self.last_snapshot_age = age
        if cached is not None and (fresh_for is None or age is not None and age <= fresh_for):
            return cached

        try:
            self.circuit_breaker.before_request()
        except CircuitoFonteAberto:
            if cached is not None:
                self.degraded = True
                return cached
            raise
        last_error: Exception | None = None
        for attempt in range(self.attempts):
            self.bucket.wait(self.sleeper)
            try:
                response = self.client.get(url, params=params, headers=self.headers)
                if response.status_code == 429 or response.status_code >= 500:
                    response.raise_for_status()
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, (dict, list)):
                    raise HttpFonteError("resposta JSON deve ser objeto ou lista")
                self.cache.set(key, data)
                self.circuit_breaker.record_success()
                self.last_snapshot_age = 0.0
                return data
            except (httpx.HTTPError, ValueError, HttpFonteError) as exc:
                last_error = exc
                if attempt == self.attempts - 1:
                    break
                self.sleeper(self.base_delay * (2**attempt) * (0.5 + self.random_fn()))
        self.circuit_breaker.record_failure()
        if cached is not None:
            self.degraded = True
            return cached
        raise HttpFonteError(f"falha ao coletar {url}") from last_error

    def close(self) -> None:
        self.client.close()
