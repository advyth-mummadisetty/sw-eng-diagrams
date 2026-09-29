"""
Utility library for generating and manipulating StarUML (.mdj) files.
"""

import copy
import math
import random
from typing import Any, Dict, Tuple


def get_id() -> str:
    """Generate a StarUML-compatible 22-character unique ID."""
    return "AAAAAA" + "".join(random.choices("0123456789ABCDEF", k=16))


def clone_view(
    template: Dict[str, Any],
    new_id: str,
    parent_id: str,
    model_id: str,
) -> Dict[str, Any]:
    """
    Recursively deep-clones a StarUML view object, assigning brand new IDs
    to all nested subViews while preserving the internal reference hierarchy.
    """
    v = copy.deepcopy(template)
    old_id = v["_id"]
    id_map = {old_id: new_id}

    def generate_ids(obj: Any):
        if isinstance(obj, dict):
            if "_id" in obj and obj["_id"] != old_id:
                id_map[obj["_id"]] = get_id()
            for val in obj.values():
                generate_ids(val)
        elif isinstance(obj, list):
            for val in obj:
                generate_ids(val)

    generate_ids(v)

    def apply_ids(obj: Any):
        if isinstance(obj, dict):
            if "_id" in obj:
                obj["_id"] = id_map.get(obj["_id"], obj["_id"])
            if "_parent" in obj and obj["_parent"]["$ref"] in id_map:
                obj["_parent"]["$ref"] = id_map[obj["_parent"]["$ref"]]
            if "$ref" in obj and obj["$ref"] in id_map:
                obj["$ref"] = id_map[obj["$ref"]]
            for val in obj.values():
                apply_ids(val)
        elif isinstance(obj, list):
            for val in obj:
                apply_ids(val)

    apply_ids(v)
    v["_parent"] = {"$ref": parent_id}
    v["model"] = {"$ref": model_id}
    return v


def calculate_polar(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p: Tuple[float, float],
) -> Tuple[float, float]:
    """
    StarUML's exact Coord.getPolar function reverse-engineered from graphics.js.
    Computes alpha (angle in radians) and distance (in pixels) for a point `p`
    relative to the directed line segment from `p1` to `p2`.
    """
    a = p2[1] - p1[1]
    b = p2[0] - p1[0] + 0.00001
    th1 = math.atan(a / b)
    if (a < 0 and b < 0) or (a > 0 and b < 0) or (a == 0 and b < 0):
        th1 = th1 + math.pi

    a = p[1] - p1[1]
    b = p[0] - p1[0] + 0.00001
    th2 = math.atan(a / b)
    if (a < 0 and b < 0) or (a > 0 and b < 0) or (a == 0 and b < 0):
        th2 = th2 + math.pi

    alpha = th1 - th2
    dist = math.sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2)
    return alpha, dist


def create_base_project(project_name: str) -> Dict[str, Any]:
    """Create a minimal valid StarUML project root dictionary."""
    proj_id = get_id()
    model_id = get_id()
    return {
        "_type": "Project",
        "_id": proj_id,
        "name": project_name,
        "ownedElements": [
            {
                "_type": "UMLModel",
                "_id": model_id,
                "_parent": {"$ref": proj_id},
                "name": f"{project_name} Model",
                "ownedElements": [],
            }
        ],
    }
