import json
import random
import copy
import math

def get_id():
    return "AAAAAA" + "".join(random.choices("0123456789ABCDEF", k=16))

def clone_view(template, new_id, parent_id, model_id):
    v = copy.deepcopy(template)
    old_id = v["_id"]
    id_map = {old_id: new_id}
    def generate_ids(obj):
        if isinstance(obj, dict):
            if "_id" in obj and obj["_id"] != old_id:
                id_map[obj["_id"]] = get_id()
            for val in obj.values(): generate_ids(val)
        elif isinstance(obj, list):
            for val in obj: generate_ids(val)
    generate_ids(v)
    def apply_ids(obj):
        if isinstance(obj, dict):
            if "_id" in obj: obj["_id"] = id_map.get(obj["_id"], obj["_id"])
            if "_parent" in obj and obj["_parent"]["$ref"] in id_map:
                obj["_parent"]["$ref"] = id_map[obj["_parent"]["$ref"]]
            if "$ref" in obj and obj["$ref"] in id_map:
                obj["$ref"] = id_map[obj["$ref"]]
            for val in obj.values(): apply_ids(val)
        elif isinstance(obj, list):
            for val in obj: apply_ids(val)
    apply_ids(v)
    v["_parent"] = {"$ref": parent_id}
    v["model"] = {"$ref": model_id}
    return v

def getPolar(p1, p2, p):
    """StarUML's exact Coord.getPolar function from graphics.js"""
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
    dist = math.sqrt((p1[0] - p[0])**2 + (p1[1] - p[1])**2)
    return alpha, dist

with open("7_collaboration_diagram_final.mdj") as f:
    d = json.load(f)

int1 = d["ownedElements"][0]["ownedElements"][0]["ownedElements"][0]
diag = [x for x in int1["ownedElements"] if x["_type"] == "UMLCommunicationDiagram"][0]

ll_tpl = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommLifelineView"][0]
path_tpl = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommunicationPathView"][0]
msg_tpl = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommMessageView"][0]

int1["ownedElements"] = [diag]
diag["ownedViews"] = []

# Spacious 3x3 layout
lifelines_def = {
    "Passenger": (100, 100, "#e8f5e9"),
    "Booking Service": (600, 100, "#fff9c4"),
    "Train Service": (1100, 100, "#e1f5fe"),
    "Web Portal": (100, 380, "#f5f5f5"),
    "Booking Engine": (600, 380, "#eeeeee"),
    "Payment Gateway": (1100, 380, "#f3e5f5"),
    "Notification Service": (100, 660, "#e8f5e9"),
    "Database": (600, 660, "#fff9c4"),
    "Loyalty Service": (1100, 660, "#fce4ec")
}

NODE_W = 180
NODE_H = 65

lifeline_models = {}
lifeline_views = {}

for name, (x, y, color) in lifelines_def.items():
    l_id = get_id()
    v_id = get_id()
    model = {
        "_type": "UMLLifeline",
        "_id": l_id,
        "_parent": {"$ref": int1["_id"]},
        "name": name
    }
    int1["ownedElements"].append(model)
    lifeline_models[name] = model
    
    view = clone_view(ll_tpl, v_id, diag["_id"], l_id)
    view["left"] = x
    view["top"] = y
    view["width"] = NODE_W
    view["height"] = NODE_H
    view["fillColor"] = color
    
    # Update name label text
    nc = view.get("nameCompartment")
    for sub in view.get("subViews", []):
        sub["left"] = x
        sub["top"] = y
        sub["width"] = NODE_W
        sub["height"] = NODE_H
        if sub.get("_type") == "UMLNameCompartmentView":
            for nsub in sub.get("subViews", []):
                nsub["left"] = x
                nsub["top"] = y
                nsub["width"] = NODE_W
                if nsub.get("font", "").endswith(";1"):  # bold name label
                    nsub["text"] = f": {name}"
                    nsub["visible"] = True
                    
    diag["ownedViews"].append(view)
    lifeline_views[name] = view

paths_def = [
    ("Passenger", "Booking Service"),
    ("Passenger", "Web Portal"),
    ("Web Portal", "Booking Service"),
    ("Booking Service", "Train Service"),
    ("Booking Service", "Payment Gateway"),
    ("Booking Service", "Loyalty Service"),
    ("Booking Service", "Booking Engine"),
    ("Booking Engine", "Database"),
    ("Booking Service", "Notification Service"),
    ("Notification Service", "Web Portal")
]

path_models = {}
path_views = {}

for src, tgt in paths_def:
    p_id = get_id()
    v_id = get_id()
    model = {
        "_type": "UMLCommunicationPath",
        "_id": p_id,
        "_parent": {"$ref": int1["_id"]},
        "end1": {
            "_type": "UMLAssociationEnd", "_id": get_id(),
            "_parent": {"$ref": p_id}, "reference": {"$ref": lifeline_models[src]["_id"]}
        },
        "end2": {
            "_type": "UMLAssociationEnd", "_id": get_id(),
            "_parent": {"$ref": p_id}, "reference": {"$ref": lifeline_models[tgt]["_id"]}
        }
    }
    int1["ownedElements"].append(model)
    view = clone_view(path_tpl, v_id, diag["_id"], p_id)
    view["head"] = {"$ref": lifeline_views[tgt]["_id"]}
    view["tail"] = {"$ref": lifeline_views[src]["_id"]}
    
    x1, y1, _ = lifelines_def[src]
    x2, y2, _ = lifelines_def[tgt]
    cx1, cy1 = x1 + NODE_W // 2, y1 + NODE_H // 2
    cx2, cy2 = x2 + NODE_W // 2, y2 + NODE_H // 2
    view["points"] = f"{cx1}:{cy1};{cx2}:{cy2}"
    
    diag["ownedViews"].append(view)
    path_models[(src, tgt)] = model
    path_models[(tgt, src)] = model
    path_views[(src, tgt)] = view
    path_views[(tgt, src)] = view

# Exact message definitions with target arrow center (cx, cy) and label position
# (num, name, src, tgt, sort, target_center, label_above)
msgs_def = [
    # Path: Passenger <-> Booking Service (Midpoint: 440, 132)
    (1, "register()/login()", "Passenger", "Booking Service", "synchCall", (440, 102), True),
    (2, "authentication result", "Booking Service", "Passenger", "reply", (440, 162), False),
    (17, "bookingStatus()", "Booking Service", "Passenger", "reply", (440, 202), False),
    
    # Path: Passenger <-> Web Portal (Midpoint: 190, 276)
    (3, "searchTrains()", "Passenger", "Web Portal", "synchCall", (125, 276), True),
    
    # Path: Web Portal <-> Booking Service (Midpoint: 440, 276)
    (4, "requestBooking()", "Web Portal", "Booking Service", "synchCall", (395, 235), True),
    
    # Path: Booking Service <-> Train Service (Midpoint: 940, 132)
    (5, "checkAvailability()", "Booking Service", "Train Service", "synchCall", (940, 102), True),
    (6, "availabilityStatus()", "Train Service", "Booking Service", "reply", (940, 162), False),
    
    # Path: Booking Service <-> Payment Gateway (Midpoint: 940, 276)
    (7, "makePayment(amount)", "Booking Service", "Payment Gateway", "synchCall", (975, 240), True),
    (8, "paymentConfirmation()", "Payment Gateway", "Booking Service", "reply", (905, 310), False),
    
    # Path: Booking Service <-> Loyalty Service (Midpoint: 940, 416)
    (9, "applyLoyalty()", "Booking Service", "Loyalty Service", "synchCall", (980, 380), True),
    (10, "loyaltyApplied()", "Loyalty Service", "Booking Service", "reply", (900, 450), False),
    
    # Path: Booking Service <-> Booking Engine (Midpoint: 690, 276)
    (11, "forwardBooking()", "Booking Service", "Booking Engine", "synchCall", (620, 276), True),
    (16, "updateStatus()", "Booking Engine", "Booking Service", "reply", (760, 276), True),
    
    # Path: Booking Engine <-> Database (Midpoint: 690, 556)
    (12, "getBookingDetails()", "Booking Engine", "Database", "synchCall", (615, 510), True),
    (13, "bookingDetails", "Database", "Booking Engine", "reply", (765, 510), True),
    (14, "updateBookingStatus()", "Booking Engine", "Database", "synchCall", (615, 600), True),
    (15, "updateConfirmation()", "Database", "Booking Engine", "reply", (765, 600), True),
    
    # Path: Booking Service <-> Notification Service (Midpoint: 440, 416)
    (18, "sendNotification()", "Booking Service", "Notification Service", "synchCall", (360, 520), True),
    
    # Path: Notification Service <-> Web Portal (Midpoint: 190, 556)
    (19, "notifyPassenger()", "Notification Service", "Web Portal", "reply", (125, 556), True)
]

for num, name, src, tgt, sort, target_center, label_above in msgs_def:
    m_id = get_id()
    v_id = get_id()
    model = {
        "_type": "UMLMessage",
        "_id": m_id,
        "_parent": {"$ref": int1["_id"]},
        "name": f"{num}: {name}",
        "messageSort": sort,
        "source": {"$ref": lifeline_models[src]["_id"]},
        "target": {"$ref": lifeline_models[tgt]["_id"]}
    }
    int1["ownedElements"].append(model)
    view = clone_view(msg_tpl, v_id, diag["_id"], m_id)
    
    path_key = (src, tgt) if (src, tgt) in paths_def else (tgt, src)
    host_path = path_views[path_key]
    view["hostEdge"] = {"$ref": host_path["_id"]}
    
    # Points of the host edge
    edge_src = lifelines_def[path_key[0]]
    edge_tgt = lifelines_def[path_key[1]]
    c1 = (edge_src[0] + NODE_W // 2, edge_src[1] + NODE_H // 2)
    c2 = (edge_tgt[0] + NODE_W // 2, edge_tgt[1] + NODE_H // 2)
    p1 = ((c1[0] + c2[0]) // 2, (c1[1] + c2[1]) // 2)
    p2 = c2
    
    alpha, distance = getPolar(p1, p2, target_center)
    view["alpha"] = alpha
    view["distance"] = distance
    view["left"] = int(target_center[0] - 20)
    view["top"] = int(target_center[1] - 10)
    view["width"] = 40
    view["height"] = 20
    
    # Subviews: 0 is nameLabel, 1 is stereotypeLabel, 2 is propertyLabel
    for i, sub in enumerate(view.get("subViews", [])):
        if i == 0:
            sub["text"] = f"{num}: {name}"
            sub["visible"] = True
            # Label position relative to arrow
            sub["alpha"] = math.pi / 2 if label_above else -math.pi / 2
            sub["distance"] = 14
        else:
            sub["visible"] = False
            sub["alpha"] = math.pi / 2
            sub["distance"] = 10
            
    diag["ownedViews"].append(view)

d["name"] = "E-Ticketing System"
diag["name"] = "E-Ticketing Collaboration Diagram"

with open("7_collaboration_diagram_eticketing.mdj", "w") as f:
    json.dump(d, f, indent=2)

print("Generated 7_collaboration_diagram_eticketing.mdj successfully!")
