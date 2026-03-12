from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppConfig:
    data_dir: Path
    host: str = "127.0.0.1"
    port: int = 8000

    @classmethod
    def from_env(cls) -> "AppConfig":
        data_dir = Path(os.getenv("IBC_DATA_DIR", ".data")).resolve()
        host = os.getenv("IBC_HOST", "127.0.0.1")
        port = int(os.getenv("IBC_PORT", "8000"))
        return cls(data_dir=data_dir, host=host, port=port)

    @property
    def projects_dir(self) -> Path:
        return self.data_dir / "projects"

    @property
    def tasks_dir(self) -> Path:
        return self.data_dir / "tasks"

    def ensure_directories(self) -> None:
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_dir.mkdir(parents=True, exist_ok=True)