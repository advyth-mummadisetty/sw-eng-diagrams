import json
with open("7_collaboration_diagram_final.mdj") as f: d = json.load(f)
int1 = d["ownedElements"][0]["ownedElements"][0]["ownedElements"][0]
diag = [x for x in int1["ownedElements"] if x["_type"] == "UMLCommunicationDiagram"][0]
path = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommunicationPathView"][0]
ll1 = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommLifelineView" and v["_id"] == path["head"]["$ref"]][0]
ll2 = [v for v in diag["ownedViews"] if v["_type"] == "UMLCommLifelineView" and v["_id"] == path["tail"]["$ref"]][0]
print("LL1 left:", ll1.get("left"))
print("LL2 left:", ll2.get("left"))
