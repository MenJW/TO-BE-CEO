from __future__ import annotations

import json
from pathlib import Path

from intelligent_brain_company.config import AppConfig
from intelligent_brain_company.domain.project_state import ProjectRecord


class ProjectStore:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.config.ensure_directories()

    def list_projects(self) -> list[ProjectRecord]:
        projects: list[ProjectRecord] = []
        for path in sorted(self.config.projects_dir.glob("*.json")):
            projects.append(self._load_file(path))
        projects.sort(key=lambda item: item.updated_at, reverse=True)
        return projects

    def get_project(self, project_id: str) -> ProjectRecord | None:
        path = self._project_path(project_id)
        if not path.exists():
            return None
        return self._load_file(path)

    def save_project(self, project: ProjectRecord) -> ProjectRecord:
        path = self._project_path(project.project_id)
        path.write_text(json.dumps(project.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return project

    def _project_path(self, project_id: str) -> Path:
        return self.config.projects_dir / f"{project_id}.json"

    def _load_file(self, path: Path) -> ProjectRecord:
        data = json.loads(path.read_text(encoding="utf-8"))
        return ProjectRecord.from_dict(data)