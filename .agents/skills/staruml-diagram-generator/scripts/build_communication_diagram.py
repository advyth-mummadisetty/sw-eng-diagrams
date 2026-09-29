#!/usr/bin/env python3
"""
CLI script to build clean, overlap-free StarUML Collaboration/Communication Diagrams (.mdj).
Applies reverse-engineered StarUML geometry: edgePosition=1, polar quadrant offsets,
and deterministic grid layouts.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

# Ensure scripts dir is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from staruml_utils import get_id, clone_view


def build_communication_diagram(
    spec: Dict[str, Any],
    template_path: str,
    output_path: str,
) -> None:
    """
    Build a complete StarUML .mdj file containing a clean UMLCommunicationDiagram
    from a specification dictionary and base template.
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Base template not found at {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        d = json.load(f)

    # Locate interaction and diagram
    proj = d
    int1 = proj["ownedElements"][0]["ownedElements"][0]["ownedElements"][0]
    diag = [x for x in int1["ownedElements"] if x["_type"] == "UMLCommunicationDiagram"][0]

    # Extract presentation view templates
    ll_tpl = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommLifelineView"][0]
    path_tpl = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommunicationPathView"][0]
    msg_tpl = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommMessageView"][0]

    # Reset diagram views and interaction elements
    int1["ownedElements"] = [diag]
    diag["ownedViews"] = []

    node_w = spec.get("node_width", 180)
    node_h = spec.get("node_height", 65)

    lifelines_def = spec.get("lifelines", {})
    lifeline_models: Dict[str, Any] = {}
    lifeline_views: Dict[str, Any] = {}
    participant_refs: List[Dict[str, str]] = []

    # 1. Build Lifelines (Objects)
    for name, info in lifelines_def.items():
        x = info["x"]
        y = info["y"]
        color = info.get("color", "#f5f5f5")

        l_id = get_id()
        v_id = get_id()

        model = {
            "_type": "UMLLifeline",
            "_id": l_id,
            "_parent": {"$ref": int1["_id"]},
            "name": name,
        }
        int1["ownedElements"].append(model)
        lifeline_models[name] = model
        participant_refs.append({"$ref": l_id})

        view = clone_view(ll_tpl, v_id, diag["_id"], l_id)
        view["left"] = x
        view["top"] = y
        view["width"] = node_w
        view["height"] = node_h
        view["fillColor"] = color

        for sub in view.get("subViews", []):
            sub["left"] = x
            sub["top"] = y
            sub["width"] = node_w
            sub["height"] = node_h
            if sub.get("_type") == "UMLNameCompartmentView":
                for nsub in sub.get("subViews", []):
                    nsub["left"] = x
                    nsub["top"] = y
                    nsub["width"] = node_w
                    if nsub.get("font", "").endswith(";1"):  # Bold name label
                        nsub["text"] = f": {name}"
                        nsub["visible"] = True

        diag["ownedViews"].append(view)
        lifeline_views[name] = view

    # 2. Build Communication Paths (Connectors)
    paths_def = spec.get("paths", [])
    path_models: Dict[tuple, Any] = {}
    path_views: Dict[tuple, Any] = {}

    for path in paths_def:
        src = path["source"]
        tgt = path["target"]
        p_id = get_id()
        v_id = get_id()

        model = {
            "_type": "UMLCommunicationPath",
            "_id": p_id,
            "_parent": {"$ref": int1["_id"]},
            "end1": {
                "_type": "UMLAssociationEnd",
                "_id": get_id(),
                "_parent": {"$ref": p_id},
                "reference": {"$ref": lifeline_models[src]["_id"]},
            },
            "end2": {
                "_type": "UMLAssociationEnd",
                "_id": get_id(),
                "_parent": {"$ref": p_id},
                "reference": {"$ref": lifeline_models[tgt]["_id"]},
            },
        }
        int1["ownedElements"].append(model)

        view = clone_view(path_tpl, v_id, diag["_id"], p_id)
        view["head"] = {"$ref": lifeline_views[tgt]["_id"]}
        view["tail"] = {"$ref": lifeline_views[src]["_id"]}

        x1, y1 = lifelines_def[src]["x"], lifelines_def[src]["y"]
        x2, y2 = lifelines_def[tgt]["x"], lifelines_def[tgt]["y"]
        cx1, cy1 = x1 + node_w // 2, y1 + node_h // 2
        cx2, cy2 = x2 + node_w // 2, y2 + node_h // 2
        view["points"] = f"{cx1}:{cy1};{cx2}:{cy2}"

        diag["ownedViews"].append(view)
        path_models[(src, tgt)] = model
        path_models[(tgt, src)] = model
        path_views[(src, tgt)] = view
        path_views[(tgt, src)] = view

    # 3. Build Messages
    messages_def = spec.get("messages", [])
    message_refs: List[Dict[str, str]] = []

    for msg in messages_def:
        num = msg["seq"]
        name = msg["name"]
        src = msg["source"]
        tgt = msg["target"]
        sort = msg.get("sort", "synchCall")
        alpha = msg.get("alpha", 1.570796)
        dist = msg.get("dist", 35)
        lbl_alpha = msg.get("lbl_alpha", 1.570796)
        lbl_dist = msg.get("lbl_dist", 15)

        m_id = get_id()
        v_id = get_id()

        path_key = (src, tgt) if (src, tgt) in path_models else (tgt, src)
        path_model = path_models[path_key]
        host_path = path_views[path_key]

        model = {
            "_type": "UMLMessage",
            "_id": m_id,
            "_parent": {"$ref": int1["_id"]},
            "name": name,
            "sequenceNumber": str(num),
            "source": {"$ref": lifeline_models[src]["_id"]},
            "target": {"$ref": lifeline_models[tgt]["_id"]},
            "messageSort": sort,
            "connector": {"$ref": path_model["_id"]},
        }
        int1["ownedElements"].append(model)
        message_refs.append({"$ref": m_id})

        view = clone_view(msg_tpl, v_id, diag["_id"], m_id)
        view["hostEdge"] = {"$ref": host_path["_id"]}
        view["edgePosition"] = 1  # CRITICAL: EP_MIDDLE
        view["alpha"] = alpha
        view["distance"] = dist
        view["width"] = 40
        view["height"] = 20

        for i, sub in enumerate(view.get("subViews", [])):
            if i == 0:
                sub["text"] = f"{num}: {name}"
                sub["visible"] = True
                sub["alpha"] = lbl_alpha
                sub["distance"] = lbl_dist
            else:
                sub["visible"] = False
                sub["alpha"] = 1.570796
                sub["distance"] = 10

        diag["ownedViews"].append(view)

    # 4. Optional Notes & Legends
    for note in spec.get("notes", []):
        diag["ownedViews"].append({
            "_type": "UMLNoteView",
            "_id": get_id(),
            "_parent": {"$ref": diag["_id"]},
            "font": "Arial;13;0",
            "left": note.get("left", 1000),
            "top": note.get("top", 500),
            "width": note.get("width", 200),
            "height": note.get("height", 60),
            "text": note.get("text", ""),
        })

    int1["participants"] = participant_refs
    int1["messages"] = message_refs

    d["name"] = spec.get("project_name", "Software Engineering System")
    diag["name"] = spec.get("diagram_name", "Collaboration Diagram")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)

    print(f"Successfully generated '{output_path}'")
    print(f"Stats: {len(lifelines_def)} lifelines, {len(paths_def)} paths, {len(messages_def)} messages.")


def main():
    parser = argparse.ArgumentParser(description="Generate collision-free StarUML Collaboration Diagrams")
    parser.add_argument("--spec", help="Path to JSON specification file")
    parser.add_argument("--template", required=True, help="Path to base .mdj template file")
    parser.add_argument("--output", default="output_collaboration_diagram.mdj", help="Output .mdj file path")
    args = parser.parse_args()

    if not args.spec:
        print("Error: --spec JSON file must be provided. See examples for schema.", file=sys.stderr)
        sys.exit(1)

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    build_communication_diagram(spec, args.template, args.output)


if __name__ == "__main__":
    main()
