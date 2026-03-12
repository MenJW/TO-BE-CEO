from __future__ import annotations

from flask import current_app, jsonify, request

from intelligent_brain_company.api import planning_bp
from intelligent_brain_company.domain.models import Stage, UserIntervention
from intelligent_brain_company.domain.project_state import ProjectStatus, TaskRecord


@planning_bp.route("/api/planning/generate", methods=["POST"])
def generate_plan():
    payload = request.get_json(silent=True) or {}
    project_id = payload.get("project_id")
    if not project_id:
        return jsonify({"success": False, "error": "project_id is required"}), 400

    project_store = current_app.extensions["project_store"]
    task_store = current_app.extensions["task_store"]
    orchestrator = current_app.extensions["planning_orchestrator"]

    project = project_store.get_project(project_id)
    if project is None:
        return jsonify({"success": False, "error": "project not found"}), 404

    task = TaskRecord.create(kind="generate_plan", project_id=project_id)
    task.mark_running()
    task_store.save_task(task)

    try:
        project.status = ProjectStatus.PLANNING
        project.touch()
        project_store.save_project(project)

        plan = orchestrator.build_plan(project.idea, project.interventions)
        markdown = orchestrator.render_plan(plan)
        version = project.register_plan(plan, markdown)
        project_store.save_project(project)

        task.mark_completed({"project_id": project_id, "version_id": version.version_id})
        task_store.save_task(task)
        return jsonify(
            {
                "success": True,
                "data": {
                    "task": task.to_dict(),
                    "project": project.to_dict(),
                    "latest_plan": version.to_dict(),
                },
            }
        )
    except Exception as exc:
        project.status = ProjectStatus.FAILED
        project.error = str(exc)
        project.touch()
        project_store.save_project(project)
        task.mark_failed(str(exc))
        task_store.save_task(task)
        return jsonify({"success": False, "error": str(exc), "task": task.to_dict()}), 500


@planning_bp.route("/api/planning/interventions", methods=["POST"])
def add_intervention_and_regenerate():
    payload = request.get_json(silent=True) or {}
    project_id = payload.get("project_id")
    if not project_id:
        return jsonify({"success": False, "error": "project_id is required"}), 400

    project_store = current_app.extensions["project_store"]
    task_store = current_app.extensions["task_store"]
    orchestrator = current_app.extensions["planning_orchestrator"]
    project = project_store.get_project(project_id)
    if project is None:
        return jsonify({"success": False, "error": "project not found"}), 404

    stage_value = payload.get("stage", Stage.RESEARCH.value)
    intervention = UserIntervention(
        stage=Stage(stage_value),
        speaker=payload.get("speaker", "user"),
        message=payload.get("message", ""),
        impact=payload.get("impact", "revise downstream conclusions"),
    )
    project.add_intervention(intervention)
    project_store.save_project(project)

    task = TaskRecord.create(kind="regenerate_plan", project_id=project_id)
    task.mark_running()
    task_store.save_task(task)

    try:
        plan = orchestrator.build_plan(project.idea, project.interventions)
        markdown = orchestrator.render_plan(plan)
        version = project.register_plan(plan, markdown)
        project_store.save_project(project)
        task.mark_completed({"project_id": project_id, "version_id": version.version_id})
        task_store.save_task(task)
        return jsonify(
            {
                "success": True,
                "data": {
                    "task": task.to_dict(),
                    "project": project.to_dict(),
                    "latest_plan": version.to_dict(),
                },
            }
        )
    except Exception as exc:
        task.mark_failed(str(exc))
        task_store.save_task(task)
        return jsonify({"success": False, "error": str(exc), "task": task.to_dict()}), 500


@planning_bp.route("/api/tasks/<task_id>", methods=["GET"])
def get_task(task_id: str):
    task_store = current_app.extensions["task_store"]
    task = task_store.get_task(task_id)
    if task is None:
        return jsonify({"success": False, "error": "task not found"}), 404
    return jsonify({"success": True, "data": task.to_dict()})