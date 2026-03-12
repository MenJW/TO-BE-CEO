from __future__ import annotations

import json
from pathlib import Path

from intelligent_brain_company.config import AppConfig
from intelligent_brain_company.domain.project_state import TaskRecord


class TaskStore:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.config.ensure_directories()

    def get_task(self, task_id: str) -> TaskRecord | None:
        path = self._task_path(task_id)
        if not path.exists():
            return None
        return self._load_file(path)

    def save_task(self, task: TaskRecord) -> TaskRecord:
        path = self._task_path(task.task_id)
        path.write_text(json.dumps(task.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return task

    def list_tasks_for_project(self, project_id: str) -> list[TaskRecord]:
        tasks: list[TaskRecord] = []
        for path in sorted(self.config.tasks_dir.glob("*.json")):
            task = self._load_file(path)
            if task.project_id == project_id:
                tasks.append(task)
        tasks.sort(key=lambda item: item.updated_at)
        return tasks

    def _task_path(self, task_id: str) -> Path:
        return self.config.tasks_dir / f"{task_id}.json"

    def _load_file(self, path: Path) -> TaskRecord:
        data = json.loads(path.read_text(encoding="utf-8"))
        return TaskRecord.from_dict(data)