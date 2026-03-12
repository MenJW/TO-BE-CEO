from __future__ import annotations

from dataclasses import dataclass

from intelligent_brain_company.domain.models import Department


@dataclass(frozen=True, slots=True)
class AgentProfile:
    name: str
    department: Department
    responsibility: str
    deliverables: tuple[str, ...]


def department_profiles() -> dict[Department, AgentProfile]:
    return {
        Department.RESEARCH: AgentProfile(
            name="Research Lead",
            department=Department.RESEARCH,
            responsibility="Validate demand, competition, and market timing.",
            deliverables=("feasibility assessment", "risk register", "market view"),
        ),
        Department.HARDWARE: AgentProfile(
            name="Hardware Architect",
            department=Department.HARDWARE,
            responsibility="Define physical product concepts, supply constraints, and manufacturing paths.",
            deliverables=("hardware options", "BOM assumptions", "prototype strategy"),
        ),
        Department.SOFTWARE: AgentProfile(
            name="Software Architect",
            department=Department.SOFTWARE,
            responsibility="Define control systems, apps, telemetry, and system integration choices.",
            deliverables=("software architecture", "integration plan", "technical risks"),
        ),
        Department.DESIGN: AgentProfile(
            name="Design Director",
            department=Department.DESIGN,
            responsibility="Shape user experience, product form, service flow, and usability tradeoffs.",
            deliverables=("experience concepts", "design principles", "usability risks"),
        ),
        Department.MARKETING: AgentProfile(
            name="Marketing Strategist",
            department=Department.MARKETING,
            responsibility="Define positioning, launch narrative, channels, and audience segmentation.",
            deliverables=("go-to-market options", "segment strategy", "channel assumptions"),
        ),
        Department.FINANCE: AgentProfile(
            name="Finance Lead",
            department=Department.FINANCE,
            responsibility="Evaluate budget, cash cycle, pricing room, and capital exposure.",
            deliverables=("cost envelope", "capital plan", "unit economics assumptions"),
        ),
    }


def board_roles() -> tuple[str, ...]:
    return (
        "Chief Executive Officer",
        "Chief Technology Officer",
        "Chief Financial Officer",
        "Chief Operations Officer",
    )