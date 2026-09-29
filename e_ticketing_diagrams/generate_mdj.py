import json
import random

id_map = {}
def get_id(prefix, num):
    key = f"{prefix}{num}"
    if key not in id_map:
        id_map[key] = "AAAAAA" + "".join(random.choices("0123456789ABCDEF", k=16))
    return id_map[key]

project_id = get_id("PROJ", 1)
model_id = get_id("MOD", 1)
collab_id = get_id("COL", 1)
interaction_id = get_id("INT", 1)
diagram_id = get_id("DIA", 1)

lifelines = [
    {"name": "Passenger", "x": 100, "y": 100},
    {"name": "UserInterface", "x": 400, "y": 100},
    {"name": "BookingController", "x": 750, "y": 100},
    {"name": "Database", "x": 400, "y": 450},
    {"name": "PaymentGateway", "x": 750, "y": 450},
    {"name": "NotificationServer", "x": 100, "y": 450},
]

lifeline_objs = []
lifeline_views = []
for i, ll in enumerate(lifelines):
    l_id = get_id("LIFE", i+1)
    view_id = get_id("LVIEW", i+1)
    nc_id = get_id("NAMC", i+1)
    
    lifeline_objs.append({
        "_type": "UMLLifeline",
        "_id": l_id,
        "_parent": {"$ref": interaction_id},
        "name": ll["name"]
    })
    
    lifeline_views.append({
        "_type": "UMLColLifelineView",
        "_id": view_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": l_id},
        "subViews": [
            {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": view_id},
                "model": {"$ref": l_id},
                "subViews": [
                    {
                        "_type": "LabelView",
                        "_id": get_id("LBLA", i+1),
                        "_parent": {"$ref": nc_id},
                        "visible": False,
                        "font": "Arial;13;0",
                        "parentStyle": True,
                        "left": ll["x"], "top": ll["y"], "width": 120, "height": 13
                    },
                    {
                        "_type": "LabelView",
                        "_id": get_id("LBLB", i+1),
                        "_parent": {"$ref": nc_id},
                        "font": "Arial;13;1",
                        "parentStyle": True,
                        "left": ll["x"]+5, "top": ll["y"]+7, "width": 110, "height": 13,
                        "text": f": {ll['name']}"
                    },
                    {
                        "_type": "LabelView",
                        "_id": get_id("LBLC", i+1),
                        "_parent": {"$ref": nc_id},
                        "visible": False,
                        "font": "Arial;13;0",
                        "parentStyle": True,
                        "left": ll["x"], "top": ll["y"], "width": 120, "height": 13,
                        "text": "(from Interaction1)"
                    },
                    {
                        "_type": "LabelView",
                        "_id": get_id("LBLD", i+1),
                        "_parent": {"$ref": nc_id},
                        "visible": False,
                        "font": "Arial;13;0",
                        "parentStyle": True,
                        "left": ll["x"], "top": ll["y"], "width": 120, "height": 13
                    }
                ],
                "font": "Arial;13;0",
                "parentStyle": True,
                "left": ll["x"], "top": ll["y"], "width": 140, "height": 40,
                "stereotypeLabel": {"$ref": get_id("LBLA", i+1)},
                "nameLabel": {"$ref": get_id("LBLB", i+1)},
                "namespaceLabel": {"$ref": get_id("LBLC", i+1)},
                "propertyLabel": {"$ref": get_id("LBLD", i+1)}
            }
        ],
        "font": "Arial;13;0",
        "fillColor": "#e8f4f8" if ll["name"] == "Passenger" else "#fff2cc" if ll["name"] == "UserInterface" else "#f8cecc" if ll["name"] == "Database" else "#e1d5e7",
        "left": ll["x"], "top": ll["y"], "width": 140, "height": 50,
        "stereotype": True,
        "nameCompartment": {"$ref": nc_id}
    })

messages_data = [
    (0, 1, "1: register()/login()", "synchCall"),
    (0, 1, "2: searchTrains()", "synchCall"),
    (0, 1, "3: selectSeat()", "synchCall"),
    (1, 2, "4: holdSeat()", "synchCall"),
    (2, 3, "5: tempReserveSeat()", "synchCall"),
    (3, 2, "6: seatReserved()", "reply"),
    (2, 1, "7: holdConfirmed()", "reply"),
    (0, 1, "8: makePayment(amount)", "synchCall"),
    (1, 4, "9: processPayment()", "synchCall"),
    (4, 1, "10: paymentSuccess()", "reply"),
    (1, 3, "11: commitBooking()", "synchCall"),
    (3, 1, "12: bookingConfirmed()", "reply"),
    (1, 5, "13: sendNotification()", "synchCall"),
    (5, 0, "14: notifyPassenger()", "synchCall"),
    (1, 0, "15: generateTicket()", "reply")
]

message_objs = []
message_views = []
paths = {}
path_objs = []

for i, (src_idx, tgt_idx, name, sort) in enumerate(messages_data):
    m_id = get_id("MSG", i+1)
    mv_id = get_id("MSGV", i+1)
    
    pair = tuple(sorted([src_idx, tgt_idx]))
    if pair not in paths:
        p_id = get_id("PATH", len(paths)+1)
        paths[pair] = p_id
        path_objs.append({
            "_type": "UMLCommunicationPath",
            "_id": p_id,
            "_parent": {"$ref": interaction_id},
            "end1": {
                "_type": "UMLAssociationEnd",
                "_id": get_id("END", len(paths)*2-1),
                "_parent": {"$ref": p_id},
                "reference": {"$ref": get_id("LIFE", pair[0]+1)}
            },
            "end2": {
                "_type": "UMLAssociationEnd",
                "_id": get_id("END", len(paths)*2),
                "_parent": {"$ref": p_id},
                "reference": {"$ref": get_id("LIFE", pair[1]+1)}
            }
        })
    
    message_objs.append({
        "_type": "UMLMessage",
        "_id": m_id,
        "_parent": {"$ref": interaction_id},
        "name": name,
        "messageSort": sort,
        "source": {"$ref": get_id("LIFE", src_idx+1)},
        "target": {"$ref": get_id("LIFE", tgt_idx+1)}
    })
    
    src = lifelines[src_idx]
    tgt = lifelines[tgt_idx]
    
    x1, y1 = src["x"] + 70, src["y"] + 25
    x2, y2 = tgt["x"] + 70, tgt["y"] + 25
    
    message_views.append({
        "_type": "UMLColMessageView",
        "_id": mv_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": m_id},
        "source": {"$ref": get_id("LVIEW", src_idx+1)},
        "target": {"$ref": get_id("LVIEW", tgt_idx+1)},
        "font": "Arial;12;0",
        "lineColor": "#000000",
        "points": f"{x1},{y1} {x2},{y2}"
    })

diagram = {
    "_type": "UMLCommunicationDiagram",
    "_id": diagram_id,
    "_parent": {"$ref": interaction_id},
    "name": "E-Ticketing Collaboration Diagram",
    "ownedViews": lifeline_views + message_views
}

interaction = {
    "_type": "UMLInteraction",
    "_id": interaction_id,
    "_parent": {"$ref": collab_id},
    "name": "Interaction1",
    "ownedElements": lifeline_objs + path_objs + message_objs + [diagram]
}

collab = {
    "_type": "UMLCollaboration",
    "_id": collab_id,
    "_parent": {"$ref": model_id},
    "name": "Collaboration1",
    "ownedElements": [interaction]
}

model = {
    "_type": "UMLModel",
    "_id": model_id,
    "_parent": {"$ref": project_id},
    "name": "E-Ticketing System Model",
    "ownedElements": [collab]
}

project = {
    "_type": "Project",
    "_id": project_id,
    "name": "E-Ticketing",
    "ownedElements": [model]
}

with open("7_collaboration_diagram_eticketing.mdj", "w") as f:
    json.dump(project, f, indent=2)

print("Generated MDJ successfully!")
