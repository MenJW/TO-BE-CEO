from intelligent_brain_company.domain.models import IdeaBrief
from intelligent_brain_company.services.planning import PlanningOrchestrator


def test_pipeline_generates_selected_solution_for_each_department() -> None:
    orchestrator = PlanningOrchestrator()
    plan = orchestrator.build_plan(
        IdeaBrief(
            title="Electric Tricycle",
            summary="A short-distance cargo vehicle for local merchants.",
            user_constraints=["Target affordable operations", "Fast pilot launch"],
        )
    )

    assert len(plan.selected_solutions) == 5
    assert plan.board_decision.conditions


def test_pipeline_renders_markdown_output() -> None:
    orchestrator = PlanningOrchestrator()
    plan = orchestrator.build_plan(IdeaBrief(title="Neighborhood Delivery Robot"))
    output = orchestrator.render_plan(plan)

    assert "# Project Plan" in output
    assert "## Board Decision" in output