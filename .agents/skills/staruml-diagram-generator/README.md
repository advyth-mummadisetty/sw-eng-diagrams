# StarUML Diagram Generator (Antigravity Skill)

An expert **Antigravity Skill** for programmatically designing, generating, repairing, and headlessly validating clean, professional UML diagrams in **StarUML (`.mdj` format)** from system requirements or lab manuals.

---

## Highlights & Capabilities

- **Zero-Overlap Geometry**: Solves StarUML's notorious `EdgeParasiticView` bug by setting `edgePosition: 1` (`EP_MIDDLE`), preventing all message arrows and labels from collapsing onto destination node corners.
- **Polar Angle Math**: Automatically handles canvas inverted Y-axis math and coordinates for connector lines.
- **Label Masking Defense**: Utilizes 4-quadrant radial separation to eliminate StarUML's opaque white text bounding boxes (`canvas.fillRect`) from wiping out neighboring arrows or text.
- **Deterministic 2D Grid Architecture**: Generates clean, well-spaced 3x3 grids and hub-and-spoke topologies instead of messy auto-layouts.
- **Headless CLI Validation**: Integrates directly with `staruml image` CLI to export high-res diagrams and bypass StarUML desktop in-memory RAM caching issues.
- **Supports All 9 Standard SE UML Diagrams**:
  1. Use Case Diagram
  2. Object Diagram
  3. Class Diagram
  4. Activity Diagram
  5. Statechart Diagram
  6. Sequence Diagram
  7. Collaboration / Communication Diagram
  8. Component Diagram
  9. Deployment Diagram

---

## Directory Structure

```text
staruml-diagram-generator/
├── SKILL.md                                 # Primary skill instructions & 6-step runbook
├── references/
│   ├── geometry_and_layout_rules.md        # Deep dive into polar math, EP_MIDDLE, & label masking
│   ├── staruml_mdj_schema.md               # StarUML internal JSON schema & view-model mapping
│   └── nine_uml_diagrams_standards.md      # Standards for all 9 SE UML diagrams
├── scripts/
│   ├── staruml_utils.py                    # ID generator, deep view cloner, and polar math tools
│   ├── build_communication_diagram.py      # Standalone CLI generator for collision-free collaboration diagrams
│   └── export_and_verify.py                # Headless StarUML CLI compiler & visual inspection tool
└── examples/
    ├── sample_communication_spec.json      # Declarative input specification schema
    └── collaboration_template.mdj          # Valid StarUML base view template
```

---

## Installation for Antigravity Users

### Option 1: Workspace Installation (Project-Specific)
Clone or copy this repository into your project's `.agents/skills/` directory:

```bash
mkdir -p .agents/skills
git clone https://github.com/advyth-mummadisetty/staruml-diagram-generator.git .agents/skills/staruml-diagram-generator
```

### Option 2: Global Installation (Available across all projects on your machine)
Clone or copy this repository into your Antigravity global configuration:

```bash
mkdir -p ~/.gemini/config/skills
git clone https://github.com/advyth-mummadisetty/staruml-diagram-generator.git ~/.gemini/config/skills/staruml-diagram-generator
```

Once installed, your Antigravity agent will automatically discover the skill and trigger it whenever you ask to generate, fix, layout, or export StarUML diagrams.

---

## Standalone Script Usage

You can also use the bundled scripts directly from your terminal:

### 1. Generate a Clean Collaboration Diagram (.mdj)
```bash
python3 scripts/build_communication_diagram.py \
  --spec examples/sample_communication_spec.json \
  --template examples/collaboration_template.mdj \
  --output my_collaboration_diagram.mdj
```

### 2. Headlessly Export to Image & Verify Quality
```bash
python3 scripts/export_and_verify.py my_collaboration_diagram.mdj -o diagram.png
```

---

## License
MIT License
