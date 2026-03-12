from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from intelligent_brain_company.domain.models import Department, DepartmentSolution


@dataclass(frozen=True, slots=True)
class DepartmentContract:
    department: Department
    focus: str
    solution_count: int = 3
    json_schema_note: str = (
        "Return JSON with key 'solutions'. Each solution must include: "
        "name, summary, feasibility_score, dependencies, assumptions, rationale, implementation_steps, success_metrics."
    )


DEPARTMENT_CONTRACTS: dict[Department, DepartmentContract] = {
    Department.HARDWARE: DepartmentContract(
        department=Department.HARDWARE,
        focus="physical architecture, supply chain, manufacturability, certification, reliability",
    ),
    Department.SOFTWARE: DepartmentContract(
        department=Department.SOFTWARE,
        focus="embedded logic, control stack, apps, telemetry, integration risk, maintainability",
    ),
    Department.DESIGN: DepartmentContract(
        department=Department.DESIGN,
        focus="industrial design, user flow, safety cues, ergonomics, serviceability",
    ),
    Department.MARKETING: DepartmentContract(
        department=Department.MARKETING,
        focus="positioning, wedge market, launch narrative, channels, conversion economics",
    ),
    Department.FINANCE: DepartmentContract(
        department=Department.FINANCE,
        focus="capital envelope, pricing, unit economics, cash cycle, risk containment",
    ),
}


def department_contract_prompt(department: Department) -> str:
    contract = DEPARTMENT_CONTRACTS[department]
    return (
        f"You lead the {department.value} department. Focus on {contract.focus}. "
        f"Generate exactly {contract.solution_count} viable options. {contract.json_schema_note}"
    )


def parse_department_solutions(
    department: Department,
    data: dict[str, Any],
    fallback: list[DepartmentSolution],
) -> list[DepartmentSolution]:
    try:
        raw_solutions = list(data["solutions"])
    except (KeyError, TypeError, ValueError):
        return fallback

    parsed: list[DepartmentSolution] = []
    for raw in raw_solutions[: DEPARTMENT_CONTRACTS[department].solution_count]:
        try:
            parsed.append(
                DepartmentSolution(
                    department=department,
                    name=str(raw["name"]),
                    summary=str(raw["summary"]),
                    feasibility_score=max(1, min(10, int(raw["feasibility_score"]))),
                    dependencies=[Department(item) for item in raw.get("dependencies", [])],
                    assumptions=[str(item) for item in raw.get("assumptions", [])],
                    rationale=str(raw.get("rationale", "")),
                    implementation_steps=[str(item) for item in raw.get("implementation_steps", [])],
                    success_metrics=[str(item) for item in raw.get("success_metrics", [])],
                )
            )
        except (KeyError, TypeError, ValueError):
            return fallback
    return parsed or fallback