# StarUML `.mdj` JSON Schema Reference

StarUML projects are stored as UTF-8 JSON files with the `.mdj` extension. Understanding the exact relationship between the semantic model and the visual presentation view hierarchy is critical for programmatically generating and manipulating diagrams.

---

## 1. Top-Level Hierarchy

Every `.mdj` file is organized as a nested tree with strict parent-child references:

```text
Project (_type: "Project")
└── ownedElements: [
      UMLModel (_type: "UMLModel")
      ├── ownedElements: [
      │     UMLClass / UMLActor / UMLUseCase / UMLComponent / UMLNode ...
      │     UMLCollaboration (_type: "UMLCollaboration")
      │     └── ownedElements: [
      │           UMLInteraction (_type: "UMLInteraction")
      │           ├── participants: [...]
      │           ├── messages: [...]
      │           └── ownedElements: [
      │                 UMLLifeline, UMLCommunicationPath, UMLMessage ...
      │                 UMLCommunicationDiagram / UMLSequenceDiagram ...
      │               ]
      │         ]
      │   ]
      └── ownedElements: [
            UMLClassDiagram / UMLUseCaseDiagram ...
          ]
    ]
```

### Identifier Format (`_id` and `$ref`)
- StarUML generates 22-character unique identifiers:
  ```python
  "AAAAAA" + "".join(random.choices("0123456789ABCDEF", k=16))
  ```
- Any reference to another element in the JSON is written as:
  ```json
  "model": { "$ref": "AAAAAAF..." }
  ```
- Every element must specify its parent:
  ```json
  "_parent": { "$ref": "AAAAAAF..." }
  ```

---

## 2. Models vs. Views (The Dual Architecture)

StarUML strictly decouples **Semantic Models** from **Visual Views**:

| Element Category | Semantic Model (`int1["ownedElements"]`) | Visual Presentation (`diag["ownedViews"]`) |
| :--- | :--- | :--- |
| **Lifeline / Role** | `_type: "UMLLifeline"` | `_type: "UMLCommLifelineView"` or `UMLSeqLifelineView"` |
| **Path / Link** | `_type: "UMLCommunicationPath"` | `_type: "UMLCommunicationPathView"` |
| **Message** | `_type: "UMLMessage"` | `_type: "UMLCommMessageView"` or `UMLSeqMessageView"` |
| **Class** | `_type: "UMLClass"` | `_type: "UMLClassView"` |
| **Use Case** | `_type: "UMLUseCase"` | `_type: "UMLUseCaseView"` |
| **Actor** | `_type: "UMLActor"` | `_type: "UMLActorView"` |
| **Component** | `_type: "UMLComponent"` | `_type: "UMLComponentView"` |
| **Node** | `_type: "UMLNode"` | `_type: "UMLNodeView"` |
| **Note / Annotation**| *(View only)* | `_type: "UMLNoteView"` |

### View-to-Model Binding
A visual view references its semantic model via the `model` field:
```json
{
  "_type": "UMLCommLifelineView",
  "_id": "AAAAAAG...",
  "_parent": { "$ref": "<diagram_id>" },
  "model": { "$ref": "<lifeline_model_id>" },
  "left": 220,
  "top": 100,
  "width": 180,
  "height": 65
}
```

---

## 3. Communication Diagram Structure

### Semantic Lifeline:
```json
{
  "_type": "UMLLifeline",
  "_id": "AAAAAAG...",
  "_parent": { "$ref": "<interaction_id>" },
  "name": "Booking Service"
}
```

### Semantic Communication Path (Connector):
```json
{
  "_type": "UMLCommunicationPath",
  "_id": "AAAAAAG...",
  "_parent": { "$ref": "<interaction_id>" },
  "end1": {
    "_type": "UMLAssociationEnd",
    "_id": "AAAAAAG...",
    "_parent": { "$ref": "<path_id>" },
    "reference": { "$ref": "<source_lifeline_id>" }
  },
  "end2": {
    "_type": "UMLAssociationEnd",
    "_id": "AAAAAAG...",
    "_parent": { "$ref": "<path_id>" },
    "reference": { "$ref": "<target_lifeline_id>" }
  }
}
```

### Semantic Message:
```json
{
  "_type": "UMLMessage",
  "_id": "AAAAAAG...",
  "_parent": { "$ref": "<interaction_id>" },
  "name": "searchTrains()",
  "sequenceNumber": "1",
  "source": { "$ref": "<source_lifeline_id>" },
  "target": { "$ref": "<target_lifeline_id>" },
  "messageSort": "synchCall",  // "synchCall" (solid arrow) or "reply" (dashed arrow)
  "connector": { "$ref": "<path_model_id>" }
}
```

### Visual Message View:
```json
{
  "_type": "UMLCommMessageView",
  "_id": "AAAAAAG...",
  "_parent": { "$ref": "<diagram_id>" },
  "model": { "$ref": "<message_model_id>" },
  "hostEdge": { "$ref": "<path_view_id>" },
  "edgePosition": 1, // MANDATORY: 1 = EP_MIDDLE
  "alpha": 1.570796,  // Polar angle relative to line vector
  "distance": 35,     // Radial distance from edge center
  "subViews": [
    {
      "_type": "EdgeLabelView",
      "_id": "AAAAAAG...",
      "_parent": { "$ref": "<message_view_id>" },
      "model": { "$ref": "<message_model_id>" },
      "visible": true,
      "text": "1: searchTrains()",
      "alpha": 1.570796,
      "distance": 15
    }
  ]
}
```

---

## 4. Class Diagram Structure

In a `UMLClass`:
- Attributes live in `"attributes": [ { "_type": "UMLAttribute", "name": "...", "type": "int" } ]`
- Methods live in `"operations": [ { "_type": "UMLOperation", "name": "...", "parameters": [...] } ]`

In `UMLClassView`:
- Contains `subViews`:
  1. `UMLNameCompartmentView`: Contains stereotype, name label, namespace.
  2. `UMLAttributeCompartmentView`: Holds visible attribute item views.
  3. `UMLOperationCompartmentView`: Holds visible operation item views.
  4. `UMLReceptionCompartmentView`, `UMLTemplateParameterCompartmentView`.

---

## 5. Notes and Legend Boxes

Notes do not require a semantic model and can be added directly to any diagram's `ownedViews`:

```json
{
  "_type": "UMLNoteView",
  "_id": "AAAAAAG...",
  "_parent": { "$ref": "<diagram_id>" },
  "font": "Arial;13;0",
  "left": 1190,
  "top": 660,
  "width": 240,
  "height": 130,
  "text": "Legend:\n\u27f6  Synchronous Message\n---\u2794  Return Message\n\nObject / Participant:\n: ObjectName\n\nSequence: 1, 2, 3 in chronological order"
}
```
