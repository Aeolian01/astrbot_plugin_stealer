from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

if importlib.util.find_spec("astrbot") is None:
    astrbot_mod = types.ModuleType("astrbot")
    api_mod = types.ModuleType("astrbot.api")
    event_mod = types.ModuleType("astrbot.api.event")
    components_mod = types.ModuleType("astrbot.api.message_components")

    class _Logger:
        def debug(self, *args, **kwargs):
            pass

        def info(self, *args, **kwargs):
            pass

        def warning(self, *args, **kwargs):
            pass

        def error(self, *args, **kwargs):
            pass

    class AstrMessageEvent:
        pass

    class MessageChain(list):
        pass

    class Image:
        def __init__(self, *, file: str = "", url: str = "") -> None:
            self.file = file
            self.url = url

    class Plain:
        def __init__(self, text: str = "") -> None:
            self.text = text

    api_mod.logger = _Logger()
    event_mod.AstrMessageEvent = AstrMessageEvent
    event_mod.MessageChain = MessageChain
    components_mod.Image = Image
    components_mod.Plain = Plain
    astrbot_mod.api = api_mod
    api_mod.event = event_mod
    api_mod.message_components = components_mod

    sys.modules.update(
        {
            "astrbot": astrbot_mod,
            "astrbot.api": api_mod,
            "astrbot.api.event": event_mod,
            "astrbot.api.message_components": components_mod,
        }
    )
