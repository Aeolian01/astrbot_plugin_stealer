from __future__ import annotations

import pytest

from core.event_handler import EventHandler
from core.image_processor_service import ImageProcessorService
import core.image_processor_service as image_processor_module


class _Image:
    def __init__(self, *, file: str = "", url: str = "") -> None:
        self.file = file
        self.url = url


def test_image_caption_sources_use_forward_context_alias_rules() -> None:
    handler = EventHandler.__new__(EventHandler)

    sources = handler._image_caption_cache_sources(
        _Image(file="image.png", url="https://example.com/component?fileid=abc&rkey=temp"),
        {
            "fileid": "abc",
            "file": "image.png",
            "url": "https://example.com/component?fileid=abc&rkey=temp&size=large",
        },
    )

    assert sources == [
        "fileid:abc",
        "https://example.com/component?fileid=abc&rkey=temp&size=large",
        "https://example.com/component?fileid=abc&size=large",
        "image.png",
        "https://example.com/component?fileid=abc&rkey=temp",
        "https://example.com/component?fileid=abc",
    ]


@pytest.mark.asyncio
async def test_caption_hint_uses_batch_forward_context_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = ImageProcessorService.__new__(ImageProcessorService)
    seen: dict[str, object] = {}

    async def get_cached(source_or_sources: object) -> str:
        seen["sources"] = source_or_sources
        return "shared caption"

    monkeypatch.setattr(
        image_processor_module,
        "forward_get_cached_image_caption",
        get_cached,
    )
    extra_meta = {"image_caption_sources": ["source-a", "source-b"]}

    caption = await service._get_forward_context_caption_hint(None, extra_meta)

    assert caption == "shared caption"
    assert seen["sources"] == ["source-a", "source-b"]
    assert extra_meta["forward_context_caption"] == "shared caption"
