import json

with open("7_collaboration_diagram_eticketing.mdj") as f:
    d = json.load(f)

int1 = d["ownedElements"][0]["ownedElements"][0]["ownedElements"][0]
diag = [x for x in int1["ownedElements"] if x["_type"] == "UMLCommunicationDiagram"][0]

# For each message view, explicitly set the nameLabel's left, top, width, height!
for v in diag["ownedViews"]:
    if v["_type"] == "UMLCommMessageView":
        lbl = v["subViews"][0]
        text = lbl.get("text", "")
        # Approx width: 7.5px per character in Arial 13
        text_w = max(int(len(text) * 7.5) + 10, 80)
        text_h = 16
        
        # Message arrow center is (v['left'] + 20, v['top'] + 10)
        cx = v["left"] + 20
        cy = v["top"] + 10
        
        # Check if label is above or below arrow
        if lbl.get("alpha", 0) > 0: # above
            lbl_x = int(cx - text_w // 2)
            lbl_y = int(cy - 20)
        else: # below
            lbl_x = int(cx - text_w // 2)
            lbl_y = int(cy + 8)
            
        lbl["left"] = lbl_x
        lbl["top"] = lbl_y
        lbl["width"] = text_w
        lbl["height"] = text_h
        print(f"{text}: arrow=({cx}, {cy}), label=({lbl_x}, {lbl_y}, {text_w}, {text_h})")

with open("7_collaboration_diagram_eticketing.mdj", "w") as f:
    json.dump(d, f, indent=2)

print("Updated MDJ labels!")
