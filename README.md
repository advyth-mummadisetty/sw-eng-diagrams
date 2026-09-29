# Software Engineering Diagrams: E-Ticketing System

A comprehensive Software Engineering (SE) design and modeling repository containing the complete set of **9 UML Diagrams** for an **E-Ticketing System**, compliant with standard academic lab guidelines and UML 2.x specifications.

Includes the built-in **Antigravity Skill** [`staruml-diagram-generator`](./.agents/skills/staruml-diagram-generator/) for programmatic generation, collision-free geometry, and headless validation of StarUML (`.mdj`) models.

---

## The 9 Standard UML Diagrams

| # | Diagram Name | StarUML Model File | Exported High-Res Image |
| :-: | :--- | :--- | :--- |
| **1** | **Use Case Diagram** | [`1_usecase_diagram.mdj`](./e_ticketing_diagrams/1_usecase_diagram.mdj) | [`Use Case Diagram.jpg`](./UML%20TO%20JPG/Use%20Case%20Diagram.jpg) |
| **2** | **Object Diagram** | [`2_object_diagram.mdj`](./e_ticketing_diagrams/2_object_diagram.mdj) | [`Object Diagram.jpg`](./UML%20TO%20JPG/Object%20Diagram.jpg) |
| **3** | **Class Diagram** | [`3_class_diagram.mdj`](./e_ticketing_diagrams/3_class_diagram.mdj) | [`Class Diagram.jpg`](./UML%20TO%20JPG/Class%20Diagram.jpg) |
| **4** | **Activity Diagram** | [`4_activity_diagram.mdj`](./e_ticketing_diagrams/4_activity_diagram.mdj) | [`Activity Diagram.jpg`](./UML%20TO%20JPG/Activity%20Diagram.jpg) |
| **5** | **Statechart Diagram** | [`5_statechart_diagram.mdj`](./e_ticketing_diagrams/5_statechart_diagram.mdj) | [`Statechart Diagram.jpg`](./UML%20TO%20JPG/Statechart%20Diagram.jpg) |
| **6** | **Sequence Diagram** | [`6_sequence_diagram.mdj`](./e_ticketing_diagrams/6_sequence_diagram.mdj) | [`Sequence Diagram.jpg`](./UML%20TO%20JPG/Sequence%20Diagram.jpg) |
| **7** | **Collaboration Diagram** | [`7_collaboration_diagram_eticketing.mdj`](./e_ticketing_diagrams/7_collaboration_diagram_eticketing.mdj) | [`Collaboration Diagram.jpg`](./UML%20TO%20JPG/Collaboration%20Diagram.jpg) |
| **8** | **Component Diagram** | [`8_component_diagram.mdj`](./e_ticketing_diagrams/8_component_diagram.mdj) | [`Component Diagram.jpg`](./UML%20TO%20JPG/Component%20Diagram.jpg) |
| **9** | **Deployment Diagram** | [`9_deployment_diagram.mdj`](./e_ticketing_diagrams/9_deployment_diagram.mdj) | [`Deployment Diagram.jpg`](./UML%20TO%20JPG/Deployment%20Diagram.jpg) |

---

## Project Context & References

- **Project Specification**: [`project_context.md`](./project_context.md) - Exact problem statement, objectives, limitations of traditional booking systems, and proposed feature set for the modern E-Ticketing platform.
- **Reference Guide**: [`uml_diagrams_reference_guide.md`](./uml_diagrams_reference_guide.md) - Detailed breakdown of all 9 UML diagrams based on the SE Lab Manual.
- **Lab Manual**: [`SE_R25_LAB_MANUAL.docx`](./SE_R25_LAB_MANUAL.docx).
- **Reference Images**: [`lab-reference-images/`](./lab-reference-images/) and [`context-images/`](./context-images/).

---

## Included Antigravity Skill

This workspace comes pre-configured with the **StarUML Diagram Generator** skill in [`.agents/skills/staruml-diagram-generator/`](./.agents/skills/staruml-diagram-generator/).

When opening this workspace in Google Antigravity, the AI assistant will automatically load the skill to:
- Generate and manipulate StarUML `.mdj` files programmatically.
- Automatically prevent message and label overlaps using `edgePosition: 1` (`EP_MIDDLE`) and 4-quadrant radial separation.
- Headlessly export diagrams via `staruml image` CLI.

---

## Building the Diagrams

To regenerate the flawless collaboration diagram with zero overlaps:

```bash
cd e_ticketing_diagrams
python3 build_clean_diagram.py
```

To headlessly export the `.mdj` to PNG/JPG using StarUML CLI:

```bash
staruml image 7_collaboration_diagram_eticketing.mdj -o output.png
```

---

## License
MIT License
