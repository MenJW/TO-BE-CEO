from __future__ import annotations

from pathlib import Path

from intelligent_brain_company.app import create_app
from intelligent_brain_company.config import AppConfig


def make_test_app(tmp_path: Path):
    config = AppConfig(data_dir=tmp_path / "runtime", host="127.0.0.1", port=8000)
    app = create_app(config)
    app.config.update(TESTING=True)
    return app


def test_create_project_and_generate_plan(tmp_path: Path) -> None:
    app = make_test_app(tmp_path)
    client = app.test_client()

    response = client.post(
        "/api/projects",
        json={
            "title": "Electric Tricycle",
            "summary": "Cargo mobility for short-distance distribution.",
            "constraints": ["Keep acquisition cost low"],
        },
    )
    assert response.status_code == 201
    project_id = response.get_json()["data"]["project_id"]

    generation = client.post("/api/planning/generate", json={"project_id": project_id})
    assert generation.status_code == 200
    payload = generation.get_json()["data"]
    assert payload["task"]["status"] == "completed"
    assert payload["project"]["latest_plan_markdown"]


def test_intervention_creates_new_plan_version(tmp_path: Path) -> None:
    app = make_test_app(tmp_path)
    client = app.test_client()

    created = client.post("/api/projects", json={"title": "Neighborhood Delivery Robot"}).get_json()["data"]
    project_id = created["project_id"]
    client.post("/api/planning/generate", json={"project_id": project_id})

    revised = client.post(
        "/api/planning/interventions",
        json={
            "project_id": project_id,
            "stage": "roundtable",
            "speaker": "founder",
            "message": "Battery maintenance must be simplified.",
            "impact": "prioritize maintainability over feature density",
        },
    )
    assert revised.status_code == 200
    project = revised.get_json()["data"]["project"]
    assert len(project["plans"]) == 2
    assert len(project["interventions"]) == 1