# The 9 Standard Software Engineering UML Diagrams

In software engineering academic curricula and professional architectural design, systems are modeled using 9 core UML diagrams spanning structural, behavioral, and architectural viewpoints.

---

## Cross-Diagram Consistency Rules

Before constructing individual diagrams, ensure strict consistency across the model:
1. **Methods $\leftrightarrow$ Messages**: Every method invoked in a Sequence or Collaboration diagram must exist as an operation in the corresponding class of the Class Diagram.
2. **Classes $\leftrightarrow$ Objects**: Object instances in Object/Collaboration diagrams must adhere to types defined in the Class Diagram (syntax: `InstanceName : ClassName`).
3. **States $\leftrightarrow$ Activities**: States in Statechart diagrams correspond to stable stages between activities executed in the Activity Diagram.
4. **Components $\leftrightarrow$ Deployment**: Components modeled in the Component Diagram must reside on execution nodes/devices in the Deployment Diagram.

---

## 1. Use Case Diagram (`UMLUseCaseDiagram`)
- **Purpose**: Captures functional requirements and external boundary interactions.
- **Key Elements**:
  - **Actors (`UMLActor`)**: External personas or subsystems initiating or receiving actions (e.g., *Passenger*, *Administrator*, *Payment Gateway*).
  - **Use Cases (`UMLUseCase`)**: Specific user goals drawn as ellipses within the boundary.
  - **System Boundary (`UMLSystemBoundaryView`)**: Encloses use cases, with actors outside.
  - **Relationships**:
    - `Association`: Plain connection between Actor and Use Case.
    - `<<include>>`: Mandatory sub-routine (dashed arrow pointing from base to included case).
    - `<<extend>>`: Optional or conditional branch (dashed arrow pointing from extension to base case).

## 2. Object Diagram (`UMLCompositeStructureDiagram` or `UMLObjectDiagram`)
- **Purpose**: Models a snapshot of system objects and slot attribute values at a specific instant in time.
- **Key Elements**:
  - **Objects/ClassifierRoles**: Box with underlined name `objectName: ClassName`.
  - **Slots/Values**: Explicit runtime attribute values (e.g., `bookingId = "TK-94012"`, `seatNumber = "12A"`).
  - **Links**: Runtime instances of associations between objects.

## 3. Class Diagram (`UMLClassDiagram`)
- **Purpose**: Static structural blueprint showing classes, attributes, methods, and relationships.
- **Key Elements**:
  - **Class (`UMLClass`)**: 3-compartment box (Name, Attributes, Operations).
  - **Visibility**: `+` (public), `-` (private), `#` (protected), `~` (package).
  - **Relationships**:
    - `Association`: Solid line with optional multiplicities (`1`, `0..*`, `1..*`).
    - `Generalization (Inheritance)`: Solid line with hollow triangular arrowhead.
    - `Aggregation`: Hollow diamond on container end (loose ownership).
    - `Composition`: Filled solid diamond on container end (strict lifecycle ownership).
    - `Dependency`: Dashed arrow with open head.

## 4. Activity Diagram (`UMLActivityDiagram`)
- **Purpose**: Business and computational workflows showing data/control flow step-by-step.
- **Key Elements**:
  - **Initial Node (`UMLInitialNode`)**: Solid black circle.
  - **Action / Activity States (`UMLActionView`)**: Rounded rectangles describing discrete operations.
  - **Decision / Merge Diamonds (`UMLDecisionNode`)**: Diamond routing flows based on guard conditions `[condition]`.
  - **Fork and Join Bars (`UMLForkNode` / `UMLJoinNode`)**: Horizontal or vertical black bars representing parallel concurrent threads.
  - **Activity Final Node (`UMLActivityFinalNode`)**: Solid circle enclosed in an outer ring (bullseye).

## 5. Statechart / State Machine Diagram (`UMLStatechartDiagram`)
- **Purpose**: Models dynamic lifecycle states of a single entity (e.g., a *Ticket* or *Order*) reacting to events.
- **Key Elements**:
  - **Initial State (`UMLPseudostate`)**: Solid black dot.
  - **States (`UMLState`)**: Rounded rectangles representing steady states (e.g., *Initiated*, *SeatReserved*, *PaymentPending*, *Confirmed*, *Cancelled*).
  - **Transitions (`UMLTransition`)**: Directed arrows with the syntax: `Event [Guard] / Action`.
  - **Final State (`UMLFinalState`)**: Bullseye.

## 6. Sequence Diagram (`UMLSequenceDiagram`)
- **Purpose**: Chronological interaction between participants along vertical timelines.
- **Key Elements**:
  - **Lifelines (`UMLLifelineView`)**: Participant box at top with vertical dashed lifeline.
  - **Execution Occurrences / Activations (`UMLActivationView`)**: Narrow vertical rectangle on the lifeline indicating active processing.
  - **Messages**:
    - `synchCall`: Solid line with filled arrow head.
    - `asynchCall`: Solid line with open arrow head.
    - `reply`: Dashed line with open arrow head.

## 7. Collaboration / Communication Diagram (`UMLCommunicationDiagram`)
- **Purpose**: Structural view of interacting objects emphasizing topology and numbered message sequence.
- **Key Elements**:
  - **Lifelines (`UMLCommLifelineView`)**: Labeled `: ObjectName`.
  - **Communication Paths (`UMLCommunicationPathView`)**: Connecting lines between communicating objects.
  - **Messages (`UMLCommMessageView`)**: Small directional arrow beside link labeled with sequence number and call (e.g., `1: register()`, `2: authResult`).
  - *Layout Requirement*: Requires explicit `edgePosition: 1` and polar math to avoid node edge crowding.

## 8. Component Diagram (`UMLComponentDiagram`)
- **Purpose**: High-level structural modularity showing subsystems, libraries, and interface contracts.
- **Key Elements**:
  - **Components (`UMLComponent`)**: Box with component stereotype `<<component>>` and two small rectangular tabs on the left edge.
  - **Provided Interface (Ball / Lollipop)**: Realized by the component for consumers.
  - **Required Interface (Socket / Cup)**: Required by the component from providers.
  - **Dependencies (`UMLDependencyView`)**: Dashed arrow connecting socket to ball.

## 9. Deployment Diagram (`UMLDeploymentDiagram`)
- **Purpose**: Physical hardware nodes, servers, client devices, and deployed software artifacts.
- **Key Elements**:
  - **Nodes (`UMLNode`)**: 3D cube representing hardware servers, virtual machines, or devices (e.g., *Client Mobile Device*, *Web Application Server*, *Primary DB Cluster*).
  - **Artifacts (`UMLArtifact`)**: Software executables, `.war` files, or packages deployed on nodes (`<<artifact>>`).
  - **Communication Paths (`UMLCommunicationPath`)**: Lines labeled with protocols (e.g., `HTTPS / TLS 1.3`, `JDBC / TCP:3306`, `AMQP / Port 5672`).
