"""Restricted public acquisition, independent of generation and semantic approval.

No default network client, activity grant, semantic assessor or model is installed.
Only configured academic concept keys can leave the process. Page text is inert.
"""

import asyncio
import hashlib
import ipaddress
import json
import re
import socket
import ssl
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from types import MappingProxyType
from typing import Protocol
from urllib.parse import quote, urljoin, urlsplit

NOTICE = "Voy a consultar información de Internet para completar esta explicación"


class WebFailure(ValueError):
    pass


@dataclass(frozen=True)
class PublicSource:
    url: str
    title: str
    entity: str
    edition: str | None = None
    conditions: str = "public documentation; no access bypass"


@dataclass(frozen=True)
class WebPolicy:
    activity: str
    version: int = 1
    enabled: bool = False
    mode: str = "self_study"
    # Host-authored vocabulary, never constructed from student input/history.
    concepts: tuple[str, ...] = ()
    destinations: tuple[str, ...] = ()
    max_searches: int = 2
    max_pages: int = 3
    max_bytes: int = 262144
    seconds: float = 15
    request_seconds: float = 5
    retries: int = 0
    redirects: int = 2

    def __post_init__(self):
        if (
            type(self.enabled) is not bool
            or type(self.version) is not int
            or not isinstance(self.activity, str)
            or not isinstance(self.concepts, tuple)
            or not isinstance(self.destinations, tuple)
        ):
            raise ValueError("immutable typed policy required")
        if not self.activity or self.version < 1 or self.mode not in {"self_study", "exam"}:
            raise ValueError("activity/version/mode required")
        for value, maximum in (
            (self.max_searches, 4),
            (self.max_pages, 8),
            (self.max_bytes, 1048576),
            (self.retries + 1, 3),
            (self.redirects + 1, 4),
        ):
            if type(value) is not int or not 1 <= value <= maximum:
                raise ValueError("finite bounded budget required")
        if not 0 < self.request_seconds <= self.seconds <= 60:
            raise ValueError("finite deadline required")
        for concept in self.concepts:
            if not re.fullmatch(r"[a-z][a-z -]{2,79}", concept):
                raise ValueError("host academic concept key required")
        for host in self.destinations:
            if not re.fullmatch(r"[a-z0-9.-]+", host) or "." not in host:
                raise ValueError("exact destination hostname required")

    @property
    def fingerprint(self):
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class LocalGap:
    activity: str
    concept: str
    scope: str
    status: str
    decision_id: str
    assessor: str
    reason: str
    local_receipt: str
    simulated: bool = False

    def validate(self, policy):
        if (
            self.activity != policy.activity
            or self.scope != "in_scope"
            or self.status != "insufficient"
            or self.concept not in policy.concepts
            or not all((self.decision_id, self.assessor, self.reason, self.local_receipt))
        ):
            raise WebFailure("explicit_in_scope_gap_required")


class SearchPort(Protocol):
    async def search(self, concept: str) -> tuple[PublicSource, ...]: ...


class AcquisitionPort(Protocol):
    async def fetch(self, url: str, *, limit: int, seconds: float, check, consume): ...


class CuratedPublicSearch:
    """Small host-curated original-source catalogue; search is local and replaceable.

    Avoids third-party search credentials and sending any user text to a service.
    Entries are discovery metadata, not assertions of validity or approval.
    """

    def __init__(self, catalog: dict[str, tuple[PublicSource, ...]]):
        self.catalog = dict(catalog)

    async def search(self, concept):
        return self.catalog.get(concept, ())


def validate_url(url, destinations):
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.port not in {None, 443}
        or parsed.fragment
        or parsed.query
        or parsed.hostname not in destinations
        or len(url) > 2048
        or any(c in url for c in "\r\n\\")
    ):
        raise WebFailure("destination_not_allowed")
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        address = None
    if address is not None and not public_ip(str(address)):
        raise WebFailure("non_public_destination")
    return parsed


async def public_addresses(host):
    records = await asyncio.get_running_loop().getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    addresses = tuple(dict.fromkeys(row[4][0] for row in records))
    if not addresses or any(not public_ip(ip) for ip in addresses):
        raise WebFailure("non_public_destination")
    return addresses


def public_ip(value):
    address = ipaddress.ip_address(value)
    return address.is_global and not address.is_multicast and not address.is_reserved


class PublicHTTPS:
    """HTTPS GET, pinned public DNS address + verified original TLS hostname.

    No cookies, proxy environment, credentials, compression, redirects or retries
    inside the transport. Cancellation closes its own stream. Only HTTP/1.1 is used.
    """

    def __init__(self, destinations, resolver=public_addresses):
        self.destinations = destinations
        self.resolver = resolver

    async def fetch(self, url, *, limit, seconds, check, consume):
        parsed = validate_url(url, self.destinations)
        writer = None
        async with asyncio.timeout(seconds):
            check()
            addresses = await self.resolver(parsed.hostname)
            if not addresses or any(not public_ip(ip) for ip in addresses):
                raise WebFailure("non_public_destination")
            check()
            reader, writer = await asyncio.open_connection(
                addresses[0],
                443,
                ssl=ssl.create_default_context(),
                server_hostname=parsed.hostname,
                limit=16384,
            )
            try:
                check()
                path = quote(parsed.path or "/", safe="/%:@-._~!$&'()*+,;=")
                writer.write(
                    (
                        f"GET {path} HTTP/1.1\r\nHost: {parsed.hostname}\r\n"
                        "User-Agent: ORALIA-public-document-inspection/1\r\n"
                        "Accept: text/html,text/plain\r\nAccept-Encoding: identity\r\n"
                        "Connection: close\r\n\r\n"
                    ).encode("ascii")
                )
                await writer.drain()
                header = await reader.readuntil(b"\r\n\r\n")
                if len(header) > 16384:
                    raise WebFailure("headers_too_large")
                lines = header.decode("iso-8859-1").split("\r\n")
                status = int(lines[0].split()[1])
                headers = {}
                for line in lines[1:]:
                    if line:
                        key, value = line.split(":", 1)
                        key = key.lower()
                        if key in headers:
                            # Link is a repeatable list field (RFC 8288/9110).
                            # We record it as metadata; no link is followed here.
                            if key == "link":
                                headers[key] += ", " + value.strip()
                                continue
                            raise WebFailure("ambiguous_headers")
                        headers[key] = value.strip()
                # Redirect/error bodies are neither needed nor followed here.
                if status != 200:
                    return status, headers, b""
                if headers.get("content-encoding", "identity") != "identity":
                    raise WebFailure("compressed_content_rejected")
                if int(headers.get("content-length", "0")) > limit:
                    raise WebFailure("byte_budget")
                data = bytearray()
                if headers.get("transfer-encoding") == "chunked":
                    while True:
                        check()
                        line = await reader.readuntil(b"\r\n")
                        if len(line) > 128:
                            raise WebFailure("chunk_header_limit")
                        size = int(line.split(b";", 1)[0], 16)
                        if not size:
                            break
                        if len(data) + size > limit:
                            raise WebFailure("byte_budget")
                        chunk = await reader.readexactly(size)
                        consume(len(chunk))
                        data.extend(chunk)
                        if await reader.readexactly(2) != b"\r\n":
                            raise WebFailure("invalid_chunk")
                elif "transfer-encoding" in headers:
                    raise WebFailure("unsupported_transfer_encoding")
                else:
                    while chunk := await reader.read(min(8192, limit + 1 - len(data))):
                        check()
                        consume(len(chunk))
                        data.extend(chunk)
                        if len(data) > limit:
                            raise WebFailure("byte_budget")
                    if "content-length" in headers and len(data) != int(headers["content-length"]):
                        raise WebFailure("incomplete_download")
                check()
                return status, headers, bytes(data)
            except (asyncio.IncompleteReadError, asyncio.LimitOverrunError) as error:
                raise WebFailure("incomplete_or_oversized_http") from error
            finally:
                if writer is not None:
                    writer.close()


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []
        self.title = []
        self.in_title = False
        self.main_depth = 0
        self.primary_indices = []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.main_depth += 1
        if tag in {"script", "style", "noscript", "svg"}:
            self.hidden += 1
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "main":
            self.main_depth = max(0, self.main_depth - 1)
        if tag in {"script", "style", "noscript", "svg"}:
            self.hidden = max(0, self.hidden - 1)
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if not self.hidden and data.strip():
            if self.main_depth:
                self.primary_indices.append(len(self.parts))
            self.parts.append(data.strip())
            if self.in_title:
                self.title.append(data.strip())


def main_text_ranges(body, content_type, text):
    if content_type.split(";", 1)[0] != "text/html":
        return []
    parser = _Text()
    parser.feed(body.decode("utf8"))
    if "\n".join(parser.parts) != text:
        raise WebFailure("extraction_offset_mismatch")
    ranges = []
    cursor = 0
    indices = set(parser.primary_indices)
    for index, part in enumerate(parser.parts):
        if index in indices:
            if ranges and ranges[-1][1] + 1 == cursor:
                ranges[-1][1] = cursor + len(part)
            else:
                ranges.append([cursor, cursor + len(part)])
        cursor += len(part) + 1
    return ranges


def extract_public(body, content_type):
    if content_type.split(";", 1)[0] not in {"text/html", "text/plain"}:
        raise WebFailure("unsupported_extraction")
    text = body.decode("utf-8", errors="strict")
    parser = _Text()
    if content_type.startswith("text/html"):
        parser.feed(text)
        text = "\n".join(parser.parts)
    if len(text.strip()) < 100:
        raise WebFailure("insufficient_extraction")
    # A diagnostic only: absence of these patterns never establishes safety.
    injection = bool(
        re.search(
            r"ignore (?:all |previous )?instructions|system prompt|"
            r"ignora .*instrucciones|send .*credentials",
            text,
            re.I,
        )
    )
    return text, " ".join(parser.title), injection


@dataclass
class WebUsage:
    searches: int = 0
    pages: int = 0
    bytes: int = 0
    attempts: int = 0
    started: float | None = None


class WebEvidence:
    def __init__(self, policy, *, current_policy, search: SearchPort, acquisition: AcquisitionPort):
        self.policy = policy
        self.current_policy = current_policy
        self.search = search
        self.acquisition = acquisition
        self.usage = WebUsage()
        self.receipts = {}
        self.cache = {}
        self.busy = False
        self.activity_scope = None
        self.current_activity_scope = lambda: None

    def check_activity_scope(self):
        if self.activity_scope is None or self.current_activity_scope() != self.activity_scope:
            raise WebFailure("activity_scope_revoked")

    def check_policy(self):
        live = self.current_policy()
        if (
            not self.policy.enabled
            or self.policy.mode != "self_study"
            or live is None
            or live.fingerprint != self.policy.fingerprint
            or not live.enabled
        ):
            self.cache.clear()
            for receipt in self.receipts.values():
                receipt["documents"] = []
            raise WebFailure("offline_or_revoked")

    def check(self):
        self.check_policy()
        if self.usage.started is not None and time.monotonic() - self.usage.started >= self.policy.seconds:
            raise WebFailure("web_deadline")

    def for_turn(self):
        """Independent bounded acquisition per chat turn; legacy inspection TTL stays unchanged."""
        self.check_policy()
        return WebEvidence(
            self.policy, current_policy=self.current_policy, search=self.search, acquisition=self.acquisition
        )

    def consume(self, count):
        self.usage.bytes += count
        if self.usage.bytes > self.policy.max_bytes:
            raise WebFailure("byte_budget")

    async def acquire(self, identifier, gap: LocalGap, notify):
        if identifier in self.receipts:
            raise WebFailure("duplicate_request")
        if self.busy:
            raise WebFailure("web_busy")
        if len(self.receipts) >= 32:
            raise WebFailure("attempt_budget")
        row = {
            "id": identifier,
            "policy": asdict(self.policy),
            "policy_sha256": self.policy.fingerprint,
            "decision": asdict(gap),
            "status": "blocked",
            "documents": [],
            "errors": [],
            "delivered_to_model": [],
            "approved_content": [],
            "publication_allowed": False,
            "external_support": "unknown",
            "teacher_compatibility": "unknown",
        }
        self.receipts[identifier] = row
        self.busy = True
        try:
            self.check()
            gap.validate(self.policy)
            if self.usage.searches >= self.policy.max_searches:
                raise WebFailure("search_budget")
            if self.usage.started is None:
                self.usage.started = time.monotonic()
            # Host must commit a visible notice before acquisition starts.
            notice_remaining = self.policy.seconds - (time.monotonic() - self.usage.started)
            if await asyncio.wait_for(notify(NOTICE), timeout=notice_remaining) is not True:
                raise WebFailure("visible_notice_required")
            self.check()
            self.usage.searches += 1
            remaining = self.policy.seconds - (time.monotonic() - self.usage.started)
            async with asyncio.timeout(remaining):
                sources = await self.search.search(gap.concept)
                self.check()
                row["discovered_sources"] = [asdict(source) for source in sources[: self.policy.max_pages]]
                row["discovery_omitted_by_budget"] = max(0, len(sources) - self.policy.max_pages)
                for source in sources[: self.policy.max_pages]:
                    if self.usage.pages >= self.policy.max_pages:
                        row["errors"].append("page_budget")
                        break
                    self.usage.pages += 1
                    try:
                        document = await self._download(source)
                        document["duplicate_of"] = next(
                            (
                                d["capture_sha256"]
                                for d in row["documents"]
                                if d["text_sha256"] == document["text_sha256"]
                            ),
                            None,
                        )
                        row["documents"].append(document)
                    except (ValueError, OSError, UnicodeError) as error:
                        row["errors"].append(
                            type(error).__name__ if not isinstance(error, WebFailure) else str(error)
                        )
                self.check()
                row["status"] = "acquired_unreviewed" if row["documents"] else "no_evidence"
        except asyncio.CancelledError:
            row["status"] = "cancelled"
            raise
        except TimeoutError:
            row["status"] = "timeout"
        except (ValueError, OSError) as error:
            row["errors"].append(str(error) if isinstance(error, WebFailure) else type(error).__name__)
        finally:
            # Revocation never leaves reusable external content in cache/receipt.
            live = self.current_policy()
            if live is None or live.fingerprint != self.policy.fingerprint or not live.enabled:
                row["documents"] = []
                row["status"] = "revoked"
                self.cache.clear()
            row["usage"] = asdict(self.usage)
            self.busy = False
        return row

    async def _download(self, source):
        if not source.title or not source.entity or not source.conditions:
            raise WebFailure("unidentified_source")
        url = source.url
        for hop in range(self.policy.redirects + 1):
            self.check()
            validate_url(url, self.policy.destinations)
            if self.usage.bytes >= self.policy.max_bytes:
                raise WebFailure("byte_budget")
            for attempt in range(self.policy.retries + 1):
                self.check()
                self.usage.attempts += 1
                try:
                    status, headers, body = await self.acquisition.fetch(
                        url,
                        limit=self.policy.max_bytes - self.usage.bytes,
                        seconds=min(
                            self.policy.request_seconds,
                            self.policy.seconds - (time.monotonic() - self.usage.started),
                        ),
                        check=self.check,
                        consume=self.consume,
                    )
                    break
                except OSError:
                    if attempt == self.policy.retries:
                        raise
            self.check()
            if status in {301, 302, 303, 307, 308}:
                if hop == self.policy.redirects:
                    raise WebFailure("redirect_budget")
                url = urljoin(url, headers.get("location", ""))
                continue
            if status != 200:
                raise WebFailure("access_not_available")
            text, title, injection = extract_public(body, headers.get("content-type", ""))
            document = {
                "title": title or source.title,
                "catalog_title": source.title,
                "entity": source.entity,
                "edition": source.edition,
                "url": url,
                "requested_url": source.url,
                "conditions": source.conditions,
                "captured_at": datetime.now(UTC).isoformat(),
                "last_modified": headers.get("last-modified"),
                "capture_sha256": hashlib.sha256(body).hexdigest(),
                "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "capture_hex": body.hex(),
                "fragments": [text],
                "primary_text_ranges": main_text_ranges(body, headers.get("content-type", ""), text),
                "coverage": "HTML text only; tables/images/navigation may be incomplete",
                "injection_detected": injection,
                "trusted_instructions": False,
                "approval": "quarantined" if injection else "unreviewed",
            }
            self.cache[document["capture_sha256"]] = document
            return document
        raise WebFailure("redirect_budget")


def load_web_evidence(path):
    """Explicit new-process opt-in. Any file edit revokes the original binding.

    Restart with a new version to enable again; editing a live file cannot grant
    permission or refresh the process budget. No SQL/session migration occurs.
    """
    path = Path(path)
    original = path.read_bytes()
    config = json.loads(original)
    fields = dict(config["policy"])
    for key in ("concepts", "destinations"):
        fields[key] = tuple(fields.get(key, ()))
    policy = WebPolicy(**fields)
    if policy.mode != "self_study":
        raise ValueError("Web is not available in exam")
    catalog = {
        key: tuple(PublicSource(**source) for source in values) for key, values in config["sources"].items()
    }
    if set(catalog) - set(policy.concepts):
        raise ValueError("catalog concepts outside policy")
    for sources in catalog.values():
        for source in sources:
            validate_url(source.url, policy.destinations)

    def current():
        try:
            return policy if path.read_bytes() == original else None
        except OSError:
            return None

    scope = config.get("activity_scope")
    if scope is not None:
        if (
            set(scope) != {"activity", "version", "concepts", "exclusive", "basis"}
            or type(scope["version"]) is not int
            or scope["activity"] != policy.activity
            or scope["version"] < 1
            or scope["concepts"] != list(policy.concepts)
            or scope["exclusive"] is not True
            or not isinstance(scope["basis"], str)
            or not scope["basis"].strip()
        ):
            raise ValueError("Explicit activity scope does not match the versioned policy")
    port = WebEvidence(
        policy,
        current_policy=current,
        search=CuratedPublicSearch(catalog),
        acquisition=PublicHTTPS(policy.destinations),
    )
    port.activity_scope = (
        MappingProxyType({k: tuple(v) if k == "concepts" else v for k, v in scope.items() if k != "basis"})
        if scope is not None
        else None
    )

    frozen_scope = port.activity_scope

    def current_scope():
        try:
            live = json.loads(path.read_bytes())
            if (
                live.get("activity_scope") == scope
                and live["policy"]["activity"] == policy.activity
                and live["policy"]["mode"] == policy.mode
            ):
                return frozen_scope
        except (OSError, ValueError, KeyError, TypeError):
            pass
        return None

    port.current_activity_scope = current_scope
    return port
