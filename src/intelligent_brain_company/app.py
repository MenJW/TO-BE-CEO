from __future__ import annotations

from flask import Flask, jsonify

from intelligent_brain_company.api import planning_bp, projects_bp
from intelligent_brain_company.config import AppConfig
from intelligent_brain_company.services.planning import PlanningOrchestrator
from intelligent_brain_company.services.project_store import ProjectStore
from intelligent_brain_company.services.task_store import TaskStore


def create_app(config: AppConfig | None = None) -> Flask:
    app_config = config or AppConfig.from_env()
    app_config.ensure_directories()

    app = Flask(__name__)
    app.config["IBC_CONFIG"] = app_config
    app.extensions["project_store"] = ProjectStore(app_config)
    app.extensions["task_store"] = TaskStore(app_config)
    app.extensions["planning_orchestrator"] = PlanningOrchestrator()

    app.register_blueprint(projects_bp)
    app.register_blueprint(planning_bp)

    @app.get("/health")
    def healthcheck():
        return jsonify({"success": True, "status": "ok"})

    return app


def main() -> None:
    config = AppConfig.from_env()
    app = create_app(config)
    app.run(host=config.host, port=config.port, debug=True)


if __name__ == "__main__":
    main()