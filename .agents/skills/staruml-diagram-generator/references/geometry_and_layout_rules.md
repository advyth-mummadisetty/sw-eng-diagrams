# StarUML Diagram Geometry & Layout Rules

This reference document details the mathematical rules, geometry formulas, and internal StarUML rendering quirks discovered by reverse-engineering the StarUML canvas rendering engine (`core.js`, `graphics.js`, `elements.js` in `/opt/StarUML/resources/app.asar`).

---

## 1. The Core Dilemma: Normal Views vs Parasitic Views

In StarUML, diagram elements are divided into two fundamental classes:

1. **Standalone Views (`UMLClassView`, `UMLNodeView`, `UMLCommLifelineView`, `UMLNoteView`)**:
   - Positioned using standard Cartesian coordinates: `left`, `top`, `width`, `height`.
   - What you set is where it renders.
   
2. **Edge Parasitic Views (`UMLCommMessageView`, `LabelView` on edges)**:
   - Attached to connector lines / paths (`UMLCommunicationPathView`, `UMLConnectorView`, `UMLAssociationView`).
   - **StarUML completely ignores standard `left` and `top` properties for these views!**
   - Instead, positions are dynamically computed during canvas paint cycles using **polar coordinates** relative to a reference point on the host edge.

---

## 2. Polar Math for Edge Parasitic Views

When StarUML renders a message or label on an edge, it computes its coordinates using:

$$\text{anchor} = \text{EdgePoint}(\text{edgePosition})$$
$$\text{x} = \text{anchor.x} + \text{distance} \times \cos(\text{lineAngle} - \text{alpha})$$
$$\text{y} = \text{anchor.y} + \text{distance} \times \sin(\text{lineAngle} - \text{alpha})$$

### The Crucial Properties:
- `hostEdge`: Reference (`$ref`) to the parent edge view.
- `edgePosition`: The anchor point along the host line segment:
  - `0` = `EP_HEAD` (Destination endpoint, clamped to the target node boundary).
  - `1` = `EP_MIDDLE` (Center / midpoint of the connector line).
  - `2` = `EP_TAIL` (Source endpoint, clamped to the source node boundary).
- `alpha`: Angle in radians relative to the vector of the connector line.
- `distance`: Radial distance (offset in pixels) from the line anchor.

> [!CAUTION]
> ### The Hidden Default Trap (`edgePosition: 0`)
> When creating or cloning an `.mdj` without explicitly specifying `"edgePosition": 1`, StarUML defaults to `0` (`EP_HEAD`).
> This causes **all messages on a link to crowd right against the destination box corner**, overlapping each other into an unreadable knot.
> **Rule: Always set `"edgePosition": 1` for all `UMLCommMessageView` elements.**

---

## 3. Inverted Canvas Coordinate System

In computer graphics (including StarUML's HTML5 Canvas), the origin $(0,0)$ is at the **top-left**:
- **X-axis**: Increases from left to right.
- **Y-axis**: Increases from top to **down**.

### Implications for Angles ($\alpha$):
- In Cartesian math, $+90^\circ$ points upwards.
- **On the Canvas, $+90^\circ$ ($+1.570796$ rad) points DOWNWARDS**, and $-90^\circ$ ($-1.570796$ rad) points UPWARDS.
- When placing a message above a horizontal line (left-to-right), use `alpha = 1.570796` (counter-clockwise offset from line direction) or `-1.570796` depending on vector orientation.
- For labels on messages, keep their subview label offsets close: `lbl_alpha = 1.570796`, `lbl_dist = 15`.

---

## 4. The Opaque Text Masking Trap ("Wipeout" Effect)

In StarUML's canvas renderer:
- Every text label automatically draws an **opaque white background rectangle** (`canvas.fillRect`) behind itself so that connector lines don't show through the text.
- If two message labels on the same line are within 30–40px of each other, one label's opaque white box will **completely wipe out the arrows and text of the neighboring message**.

### The Solution: 4-Quadrant Separation
For paths carrying multiple messages (e.g., between an orchestrator and database):
1. **Upper-Left Quadrant**: $\alpha = -120^\circ$ ($-2.094$ rad), distance $= 65\text{px}$, label offset $= 80\text{px}$.
2. **Upper-Right Quadrant**: $\alpha = -60^\circ$ ($-1.047$ rad), distance $= 65\text{px}$, label offset $= 85\text{px}$.
3. **Lower-Left Quadrant**: $\alpha = +120^\circ$ ($+2.094$ rad), distance $= 65\text{px}$, label offset $= 65\text{px}$.
4. **Lower-Right Quadrant**: $\alpha = +60^\circ$ ($+1.047$ rad), distance $= 65\text{px}$, label offset $= 80\text{px}$.

This ensures each label has at least 50px clearance in both X and Y, preventing white-box collisions.

---

## 5. Architectural Layout Best Practices

Never rely on StarUML's automated auto-layout tool—it does not account for message parasitic views and creates overlapping lines. Instead, use a deterministic grid or hub-and-spoke coordinate system.

### Recommended Node Dimensions & Spacing:
- **Node Size**:
  - Minimum width: `180px`
  - Minimum height: `65px`
- **Grid Layout (e.g., 3x3 Grid)**:
  - Left margin: `150px - 220px`
  - Top margin: `100px`
  - Horizontal inter-column spacing ($\Delta X$): `450px - 650px`
  - Vertical inter-row spacing ($\Delta Y$): `300px - 380px`
  - Total canvas footprint: approximately $1800\text{px} \times 1000\text{px}$
- **Connector Points**:
  - Connect node centers:
    $$\text{cx} = \text{left} + \frac{\text{width}}{2}, \quad \text{cy} = \text{top} + \frac{\text{height}}{2}$$
  - Format: `"points": "{cx1}:{cy1};{cx2}:{cy2}"`
  - For non-adjacent nodes, use 90-degree orthogonal bend points (`cx1:cy1;cx2:cy1;cx2:cy2`) to route around intermediary nodes.

---

## 6. StarUML In-Memory Desktop Caching Trap

> [!WARNING]
> ### StarUML Does Not Hot-Reload Disk Edits!
> If StarUML is currently running and viewing a project:
> - Modifying the `.mdj` file on disk via Python or JSON editing **will NOT update the screen**.
> - StarUML holds the model in RAM. Saving inside the GUI will **overwrite and wipe out** external edits!
> 
> **Standard Procedure:**
> 1. Close StarUML or use `File -> Open...` to re-read the file after running generation scripts.
> 2. Always verify generated `.mdj` files headlessly via CLI:
>    ```bash
>    staruml image <file.mdj> -o <output_directory>
>    ```
