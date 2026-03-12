from __future__ import annotations

from flask import Blueprint

projects_bp = Blueprint("projects", __name__)
planning_bp = Blueprint("planning", __name__)

from . import planning  # noqa: E402,F401
from . import projects  # noqa: E402,F401