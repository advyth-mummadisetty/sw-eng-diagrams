# UML Diagrams Reference Guide

This document contains the complete reference details of the 9 UML diagrams starting from page 33 (USECASE DIAGRAM) of the Lab Manual, serving as the guideline for the E-Ticketing project.

---


## USECASE DIAGRAM

Use case diagrams are used to gather the requirements of a system including internal and external influences. These requirements are mostly design requirements. Hence, when a system is analyzed to gather its functionalities, use cases are prepared and actors are identified. When the initial task is complete, use case diagrams are modelled to present the outside view.

The Passport Automation System Use Case Diagram shows the interactions between the Applicant, Passport Officer, and Administrator with the Passport Automation System.

Objectives Achieved

The Use Case Diagram satisfies the following objectives:

Automates passport application processing.

Reduces paperwork through online services.

Provides online registration and login.

Enables online document upload.

Supports online fee payment.

Allows appointment booking.

Provides application status tracking.

Enables passport verification and generation.

Helps administrators manage the entire system.

Elements of the Use Case Diagram

There are three main elements:

Actors

Use Cases

System Boundary

1. Actors

Actors are external users who interact with the Passport Automation System.


### A) Applicant

The Applicant is a citizen applying for a passport.

Responsibilities

Register

Login

Apply for Passport

Upload Documents

Pay Fees

Book Appointment

Track Application Status

Download Receipt


### B) Passport Officer

The Passport Officer verifies applications.

Responsibilities

Login
b
Verify Documents

Verify Applicant

Approve/Reject Application

Generate Passport


### C) Administrator

The Administrator manages the complete system.

Responsibilities

Login

Manage Users

Manage Officers

Generate Reports

Maintain Database

Working of the Use Case Diagram

The Applicant registers and logs into the system.

The Applicant submits a passport application.

Required documents are uploaded.

The Applicant pays the application fee.

The Applicant books an appointment.

The Passport Officer logs in and verifies the documents and applicant details.

The Passport Officer approves or rejects the application.

If approved, the system generates the passport.

The Applicant tracks the application status online.

The Administrator manages users, officers, reports, and the database.


**Fig 1: Use Case diagram for passport automation system**


## OBJECT DIAGRAM

Definition An Object Diagram is a UML structural diagram that represents the objects (instances of classes), their current values, and the relationships among them at a specific moment. It helps to understand how the system behaves with real data.

Object Diagram Used in Passport Automation System

The object diagram consists of the following objects:

applicant1 : Applicant

application1 : Application

document1 : Documents

officer1 : Officer

passport1 : Passport

admin1 : Administrator

Each object represents one real entity in the Passport Automation System.

Difference Between Class Diagram and Object Diagram

Class Diagram

Object Diagram

Shows classes

Shows objects (instances)

Represents the system design

Represents the system at a specific moment

Displays attributes and methods

Displays actual attribute values

Used during design

Used to visualize runtime examples

Example: Applicant

Example: applicant1 : Applicant

Advantages of the Object Diagram

Shows real-time instances of system objects.

Helps visualize how classes are used in practice.

Makes relationships between objects easier to understand.

Useful for testing and validating the system design.

Provides concrete examples that complement the class diagram.

Improves understanding of object-oriented concepts.


**Fig 2. Object diagram for passport automation system**


## CLASS DIAGRAM

Class diagram is a static diagram, describes the attributes and operations of a class and also the constraints imposed on the system. The class diagrams are widely used in the modeling of object oriented systems because they are the only UML diagrams, which can be mapped directly with object-oriented languages.

Class diagram shows a collection of classes, interfaces, associations, collaborations, and constraints. It is also known as a structural diagram.

Purpose of Class Diagrams

The purpose of the class diagram can be summarized as −

Analysis and design of the static view of an application.

Describe responsibilities of a system.

Base for component and deployment diagrams.

Forward and reverse engineering

In the Passport Automation System, the Class Diagram models all the major entities involved in passport application processing and illustrates how they interact to achieve the system objectives.

Working of the Class Diagram

The workflow represented by the class diagram is:

The Applicant registers and logs into the system.

The applicant submits a Passport Application.

Required Documents are uploaded.

The application fee is paid through the Payment module.

An Appointment is scheduled for verification.

The Passport Officer verifies the documents and applicant details.

If approved, a Passport is generated.

The Administrator manages users, officers, reports, and the database.

Advantages of this Class Diagram

Clearly represents the static structure of the Passport Automation System.

Separates system responsibilities into different classes.

Promotes modularity and easy maintenance.

Supports online registration, payment, document upload, and status tracking.

Reduces redundancy by organizing data into related classes.

Makes future enhancements, such as adding police verification or SMS notifications, easier.

Provides a blueprint for implementation in object-oriented programming languages like Java, C++, or Python.


**Fig 3. Class diagram for passport automation system**


## ACTIVITY DIAGRAM

An Activity Diagram is a UML behavioral diagram that illustrates the workflow of activities, decisions, and actions involved in a business process or software system. It represents the flow of control from the initial state to the final state.

Symbols Used in Activity Diagram

Symbol

Meaning

●

Initial (Start) Node

◎

Final (End) Node

▭ Rounded Rectangle

Activity or Action

◇ Diamond

Decision or Branch

→ Arrow

Flow of Control

▬ Thick Bar

Fork or Join (Parallel Activities)

Activities in the Passport Automation System

The Activity Diagram contains the following major activities:

Start

Register

Login

Fill Passport Application

Upload Documents

Validate Documents

Make Payment

Book Appointment

Verify Documents

Decision (Approved or Rejected)

Generate Passport

Update Application Status

Notify Applicant

End

Explanation of Decision Node

The Decision Node (◇) is used to determine the next step based on verification.

Approved: The passport is generated, the status is updated, and the applicant is notified.

Rejected: The applicant receives a rejection notification, and the process ends or the application can be corrected and resubmitted.


**Fig 4. Activity diagram for passport automation system**

Difference Between Activity Diagram and Flowchart

Activity Diagram

Flowchart

Part of UML

General process diagram

Models software workflows

Models any process

Supports parallel activities (fork/join)

Limited support for parallel activities

Uses UML symbols

Uses standard flowchart symbols

Focuses on system behavior

Focuses on procedural logic

Applications of Activity Diagram

Activity Diagrams are widely used in:

Passport Automation System

ATM System

Library Management System

Railway Reservation System

Hospital Management System

Banking Applications

Online Shopping Systems

Student Management Systems


## STATECHART DIAGRAM

A State Chart Diagram is a UML behavioral diagram that describes the various states of an object and the transitions between those states based on events or conditions.

Objective of State Chart Diagram

The State Chart Diagram helps to:

Model the life cycle of a passport application.

Show state transitions clearly.

Improve understanding of system behavior.

Reduce processing errors.

Track the application status at every stage.

Increase transparency for applicants.

Symbols Used in the State Chart Diagram

Symbol

Meaning

●

Initial State (Start)

◎

Final State (End)

Rounded Rectangle

State

Arrow (→)

Transition from one state to another

Decision/Guard

Determines the next state based on a condition (Approved/Rejected)

Advantages of the State Chart Diagram

Shows the complete life cycle of a passport application.

Clearly represents every state and transition.

Helps developers understand system behavior.

Makes it easier to identify missing or incorrect state transitions.

Supports automation and status tracking.

Improves transparency by defining application status at every stage.

Difference Between Activity Diagram and State Chart Diagram

Activity Diagram

State Chart Diagram

Represents the workflow of activities.

Represents the life cycle of an object through different states.

Focuses on actions performed in the system.

Focuses on state changes of an object.

Shows process flow.

Shows state transitions.

Used to model business processes.

Used to model object behavior.

Example: Registration → Login → Payment

Example: Submitted → Under Verification → Approved → Passport Generated


**Fig 5. State chart diagram for passport automation system**


## SEQUENCE DIAGRAM

A Sequence Diagram is a UML behavioral diagram that represents the interaction between objects in a time sequence. It shows the order in which messages are exchanged to complete a specific process.

Symbols Used in Sequence Diagram

Symbol

Meaning

Actor

External user interacting with the system (Applicant)

Object

System components such as Payment Gateway or Passport Database

Lifeline

Vertical dashed line showing the existence of an object over time

Activation Bar

Thin rectangle showing when an object is performing an operation

Message Arrow

Communication between objects

Return Message

Response sent back after processing (optional dashed arrow)

Advantages of the Sequence Diagram

Clearly shows the order of interactions between objects.

Helps developers understand communication among system components.

Makes the processing sequence easy to follow.

Identifies missing interactions during software design.

Supports system testing and debugging.

Improves documentation and communication among stakeholders.

Difference Between Sequence Diagram and Activity Diagram

Sequence Diagram

Activity Diagram

Shows interactions between objects.

Shows the workflow of activities.

Focuses on message exchange.

Focuses on process flow.

Time is represented from top to bottom.

Flow is represented through activities and decisions.

Uses lifelines and message arrows.

Uses activities, decisions, and control flows.

Emphasizes object communication.

Emphasizes business process logic.


**Fig 6. Sequence diagram for passport automation system**


## COLLABORATION DIAGRAM

A Collaboration Diagram is a UML behavioral diagram that represents the interaction among objects through message passing. It emphasizes the structural organization of objects and their communication to accomplish a particular function.

Difference Between Collaboration Diagram and Sequence Diagram

Collaboration Diagram

Sequence Diagram

Focuses on object relationships and communication.

Focuses on the chronological order of interactions.

Objects are connected through communication links.

Objects are represented with vertical lifelines.

Uses numbered messages to indicate sequence.

Uses messages arranged from top to bottom to indicate sequence.

Emphasizes structural organization.

Emphasizes the timing of message exchange.

Easier to understand object collaboration.

Easier to understand execution flow over time.


**Fig 7. Collaboration diagram for passport automation system**


## COMPONENT DIAGRAM

A Component Diagram is a UML structural diagram that illustrates the organization and interaction of software components in a system. It helps developers understand the system architecture by showing components and their dependencies.

Components Used in the Passport Automation System

The main software components are:

User Interface (UI)

Authentication Component

Application Processing Component

Document Management Component

Payment Component

Verification Component

Passport Generation Component

Database Component

Notification Component

Difference Between Class Diagram and Component Diagram

Class Diagram

Component Diagram

Shows classes, attributes, methods, and relationships.

Shows software components and their dependencies.

Represents the logical design.

Represents the physical software architecture.

Used in object-oriented design.

Used in software architecture and deployment planning.

Focuses on objects and classes.

Focuses on software modules.


**Fig 8. Component diagram for passport automation system**


## DEPLOYMENT DIAGRAM

A Deployment Diagram is a UML structural diagram that illustrates the physical deployment of hardware nodes, software components, and communication links in a system.

Hardware Nodes in the Passport Automation System

The Deployment Diagram contains the following hardware nodes:

Applicant Computer / Mobile

Internet

Web Server

Application Server

Database Server

Payment Gateway Server

Notification Server

Hardware Node

Software Components

Applicant Computer

Web Browser / Mobile App

Web Server

Registration Module, Login Module, User Interface

Application Server

Authentication, Application Processing, Verification, Passport Generation

Database Server

Passport Database

Payment Gateway

Online Payment Module

Notification Server

SMS and Email Service

Advantages of Deployment Diagram

Shows the physical architecture of the system.

Explains where software components are deployed.

Improves understanding of system communication.

Helps in network planning.

Supports system scalability.

Helps identify hardware requirements.

Improves security planning.

Useful during software deployment and maintenance.

Difference Between Component Diagram and Deployment Diagram

Component Diagram

Deployment Diagram

Shows software components.

Shows hardware nodes and deployed components.

Represents logical software architecture.

Represents physical system architecture.

Focuses on software modules.

Focuses on hardware devices and network communication.

Used during software design.

Used during deployment and implementation.


**Fig 9. Deployment diagram for passport automation system**

