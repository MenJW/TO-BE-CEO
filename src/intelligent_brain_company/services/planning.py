from __future__ import annotations

from intelligent_brain_company.domain.models import IdeaBrief, ProjectPlan, UserIntervention
from intelligent_brain_company.workflows.pipeline import CompanyPipeline


class PlanningOrchestrator:
    def __init__(self, pipeline: CompanyPipeline | None = None) -> None:
        self.pipeline = pipeline or CompanyPipeline()

    def build_plan(
        self,
        brief: IdeaBrief,
        interventions: list[UserIntervention] | None = None,
    ) -> ProjectPlan:
        return self.pipeline.run(brief=brief, interventions=interventions)

    def render_plan(self, plan: ProjectPlan) -> str:
        return self.pipeline.render_markdown(plan)