# Complete Scrum guide

> **Human reference (onboarding).** Not an operational source for the Meridian protocol.  
> For agent work, use **[scrum-meridian-map.md](./scrum-meridian-map.md)**.  
> Read this guide when you want full Scrum fundamentals; agents should open it only if the manager explicitly asks.

### Epics, user stories, versions, and more

---

## Table of contents

1. [Scrum overview](#1-scrum-overview)
2. [Artifact hierarchy](#2-artifact-hierarchy)
3. [Epics](#3-epics)
4. [Features](#4-features)
5. [User stories](#5-user-stories)
6. [Tasks and subtasks](#6-tasks-and-subtasks)
7. [Bugs](#7-bugs)
8. [Spikes](#8-spikes)
9. [Versions and releases](#9-versions-and-releases)
10. [Sprints](#10-sprints)
11. [The product backlog](#11-the-product-backlog)
12. [Scrum ceremonies](#12-scrum-ceremonies)
13. [Scrum roles](#13-scrum-roles)
14. [Essential concepts](#14-essential-concepts)
15. [How versions, epics, and sprints relate](#15-how-versions-epics-and-sprints-relate)
16. [Frequently asked questions](#16-frequently-asked-questions)
17. [Visual summary](#17-visual-summary)

---

## 1. Scrum overview

Scrum is an agile framework for software development (and other products) based on short delivery cycles called **sprints**, continuous inspection of what is being done, and constant adaptation of the plan.

Scrum is not a rigid process with immutable rules. It is a framework — it gives you structure but expects the team to adapt the details to their reality. Different teams can apply Scrum in slightly different ways, and that is fine as long as the fundamental principles are respected.

### Fundamental principles

- **Transparency** — All aspects of the process must be visible to those responsible for the outcome.
- **Inspection** — The team frequently inspects progress toward the sprint goal.
- **Adaptation** — If something is drifting from expectations, the team adjusts as quickly as possible.

### Why use Scrum?

Software projects are complex and full of uncertainty. Scrum accepts that reality instead of pretending an upfront plan will survive intact to the end. Rather than planning everything at once, the team plans in short cycles, delivers value often, and adjusts course based on what it learns.

---

## 2. Artifact hierarchy

In Scrum and complementary frameworks (SAFe, LeSS, or tools like Jira and Linear), work items are organized in a hierarchy. From largest to smallest:

```
Product
  └── Epic
        └── Feature / Capability
              └── User Story
                    ├── Task / Subtask
                    └── Bug / Fix

Special types (at any level):
  └── Spike (research / investigation)
```

Each level has a different purpose:

| Level | Scope | Typical duration |
|---|---|---|
| Epic | Large product value area | Weeks to months |
| Feature | Specific capability within an epic | Weeks |
| User Story | Deliverable work unit | Within one sprint (1–2 weeks) |
| Task | Technical step inside a story | Hours |
| Bug | Incorrect behavior to fix | Hours to days |
| Spike | Investigation with a defined timebox | Hours to days |

---

## 3. Epics

### What is an epic?

An epic is a large slice of value that is too big to fit in a single sprint. It represents a significant, cohesive body of work — something that, when complete, delivers an important capability to the product or user.

Example epics:

- Authentication system
- Checkout module
- Analytics dashboard
- Payment gateway integration
- Notification system

### Do epics persist across versions?

**Yes.** An epic exists while there is work associated with it. It can span multiple sprints and multiple versions without issue. A version is a delivery milestone to end users; an epic is a way to organize work. These two concepts coexist independently.

An epic is closed when the team decides it is sufficiently complete. That criterion should be defined explicitly — usually from the epic’s Definition of Done, which may include: all epic stories delivered, epic acceptance criteria validated, and no material planned work left in the near horizon.

### Can epics be reopened?

Technically a “completed” epic can be reopened, but the recommended practice is to **create a new epic** referencing the previous one.

**Why create a new epic instead of reopening the old one?**

- Keeps the original epic history clean.
- Makes clear this is evolution or expansion, not a planning failure fix.
- Helps velocity metrics and historical retrospectives.
- Avoids confusion about original scope vs. what was added later.

**Practical example:**

- Original epic: `[CLOSED] Authentication system` — email/password login, password recovery, session.
- Future epic: `Advanced authentication` — Google/Apple login, biometrics, two-factor authentication.

If future work is small (one or two stories), a new epic may not be justified — it can fold into a related epic such as “Security and access”.

### Epic vs. project

Do not confuse epic with project. A project is an initiative with a defined start and end involving multiple areas. An epic is a product backlog organization unit within a project. A project can have dozens of epics.

---

## 4. Features

### What is a feature?

A feature (or capability) is an intermediate level between epic and user story. Not every team uses this level explicitly — it is more common in scale frameworks like SAFe or in teams working on large, complex products.

**When a feature is useful:**

- When an epic is too large and contains many unrelated stories.
- When you need a grouping level to communicate capabilities to stakeholders without story-level detail.
- When multiple teams work in parallel, each owning a feature within an epic.

**Example:**

```
Epic: Authentication system
  ├── Feature: Email and password login
  │     ├── Story: As a user, I want to log in with my email and password
  │     └── Story: As a user, I want a clear error message if I enter the wrong password
  ├── Feature: Password recovery
  │     ├── Story: As a user, I want to receive a recovery email
  │     └── Story: As a user, I want to reset my password via a secure link
  └── Feature: Social login
        ├── Story: As a user, I want to log in with my Google account
        └── Story: As a user, I want to log in with my Apple account
```

For smaller products or small teams, you can skip the feature level and go straight from epic to stories. That is fully valid.

---

## 5. User stories

### What is a user story?

A user story is the fundamental unit of work in Scrum. It describes a piece of functionality from the perspective of the user who benefits — not from a technical perspective.

The classic format is:

> **As a** [type of user], **I want** [to perform an action], **so that** [I get a benefit].

**Examples:**

- As a customer, I want to add products to the cart so I can buy multiple items at once.
- As an administrator, I want a sales report by period so I can track store performance.
- As a user, I want a notification when my order ships so I know when to expect delivery.

### Why the “As… I want… so that…” format?

The format forces three important things:

1. **Who** benefits (avoids generic stories with no owner).
2. **What** the person wants to do (desired behavior).
3. **Why** it matters (value delivered).

The “so that” is especially important. It helps the team understand intent behind the story, enabling better solutions or simpler alternatives that meet the same goal.

### Acceptance criteria

Each user story should have **acceptance criteria** — specific conditions that must be true for the story to be considered done.

Acceptance criteria are specific to each story (unlike Definition of Done, which is global for the team).

**Example:**

Story: *As a user, I want to log in with my email and password.*

Acceptance criteria:

- Given the user is on the login screen, when they enter correct email and password and click “Sign in”, then they are redirected to the home page while logged in.
- Given the user enters an incorrect password, when they click “Sign in”, then an error message is shown (without revealing whether the email exists).
- Given the user enters the wrong password 5 times in a row, then the account is temporarily locked for 15 minutes.
- Login response time must be under 2 seconds.

The “Given… When… Then…” format is known as **Gherkin** and is widely used because it is clear, testable, and understandable by both developers and non-technical stakeholders.

### INVEST: what makes a good user story?

The INVEST acronym summarizes characteristics of a good user story:

| Letter | Meaning |
|---|---|
| **I** | **Independent** — As independent of other stories as possible |
| **N** | **Negotiable** — Scope can be negotiated between PO and team |
| **V** | **Valuable** — Delivers value to user or business |
| **E** | **Estimable** — Team can estimate effort |
| **S** | **Small** — Small enough to fit in one sprint |
| **T** | **Testable** — Clear criteria for when it is done |

### Story points

Stories are estimated in **story points** — a relative unit of complexity/effort, not time. The most common scale is modified Fibonacci: 1, 2, 3, 5, 8, 13, 21.

- A 1-point story is trivial.
- An 8-point story is significantly complex.
- A 13+ point story should probably be split.

Story points measure relative effort, not hours. “This story is twice as complex as that one” is more reliable than “this story will take 4 hours”.

---

## 6. Tasks and subtasks

### What are tasks?

Tasks are the technical steps needed to complete a user story. They do not use the “As… I want…” format; they are simply descriptions of technical work.

**Example tasks for the story “Login with email and password”:**

- Create `POST /auth/login` endpoint
- Implement JWT validation on the backend
- Build login screen on the frontend
- Integrate screen with authentication API
- Write unit tests for the authentication service
- Write integration tests for the endpoint
- Update API documentation

### Who creates tasks?

Usually the development team creates tasks during Sprint Planning, after the Product Owner presents and clarifies stories selected for the sprint.

### Are tasks mandatory?

No. Mature teams often work at story level without formal tasks because they already know what to do. Less experienced teams or complex stories benefit from tasks to avoid gaps and distribute work.

---

## 7. Bugs

### Are bugs different from stories and tasks?

Yes. A bug is unexpected or incorrect system behavior — something that should work one way and does not. It does not deliver new value; it restores value that should already exist.

### Where do bugs enter the process?

Bugs can enter the process in several ways:

**1. Bug found during the current sprint:**  
If introduced during the sprint in progress, the team fixes it immediately without extra ceremony. It is part of completing the story.

**2. Bug found in already delivered functionality:**  
It enters the Product Backlog, is prioritized by the Product Owner by impact, and is included in a future sprint. It may be recorded as:

- A technical story: *“Fix incorrect shipping calculation for Northeast ZIP codes”*.
- A task inside a related story.

**3. Critical production bug:**  
May justify interrupting current planning and an urgent correction release (hotfix), depending on impact.

### Severity vs. priority

It is important to distinguish:

- **Severity**: How much the bug affects system behavior (critical, high, medium, low).
- **Priority**: How urgent it is to fix from a business perspective (a low-severity bug can be high priority for brand or contract reasons).

---

## 8. Spikes

### What is a spike?

A spike is a special backlog item for **research, investigation, or proof of concept**. It exists to reduce uncertainty when the team does not know how to estimate or implement something.

The name comes from Extreme Programming (XP) and refers to a concentrated, time-limited burst of effort.

**When to use a spike:**

- “We do not know which payment library to use — we need to evaluate options.”
- “We have never integrated with that legacy system — we need to investigate their API before estimating.”
- “Report performance is poor — we need to find the bottleneck before knowing what to change.”

### Spike characteristics

- **Defined timebox**: The team decides how much time to spend — e.g. “2 days”. When time is up, the spike ends and the team shares what was learned.
- **Clear objective**: The question to answer is defined before starting.
- **Outcome is knowledge, not production code**: May produce a document, a decision, an estimate, or a proof of concept (usually not shipped to production).

**Example spike:**

> *Evaluate PDF generation library options (pdfkit, puppeteer, weasyprint) and recommend one for this project considering performance, maintenance, and cost. Timebox: 1 day.*

---

## 9. Versions and releases

### What is a version (release)?

A version or release is a milestone of software delivery to end users. It groups a set of capabilities that will be made available together.

Versions sit at a different level than sprints — you can have multiple sprints within a version, and a sprint can contribute to multiple versions (less common).

### Version naming

The most common pattern is **Semantic Versioning** (SemVer): `MAJOR.MINOR.PATCH`

| Part | When it increments | Example |
|---|---|---|
| MAJOR | Incompatible change / rewrite / major milestone | 1.0 → 2.0 |
| MINOR | New backward-compatible functionality | 1.0 → 1.1 |
| PATCH | Bug fix / hotfix | 1.1 → 1.1.1 |

### Can we create intermediate versions?

**Absolutely yes.** That is not only allowed but very common and recommended.

Imagine you plan:

```
v1.0 → v2.0 → v3.0
```

Midway, a critical production bug appears or a stakeholder asks for a small urgent feature. You create:

```
v1.0 → v1.1 (hotfix/urgent) → v2.0 → v3.0
```

Or a more elaborate scenario:

```
v1.0 (initial launch)
  └── v1.1 (critical bug fixes — 1 sprint)
  └── v1.2 (small user-requested improvements — 2 sprints)
v2.0 (major refactor + new features — 6 sprints)
  └── v2.1 (post-launch adjustments — 1 sprint)
v3.0 ...
```

### Planned vs. actual versions

A good practice is a **version roadmap** — high-level planning of what goes in each version. It does not need to be fixed; it is adjusted as the team learns.

The roadmap answers questions such as:

- When will the MVP be ready? (v1.0)
- When will enterprise customers get SSO? (v2.0)
- When do we ship internationalization? (v3.0)

### Releases and sprints are not the same thing

A common mistake is equating sprint with release. They are independent:

- A sprint always has fixed duration (1–4 weeks).
- A release can happen anytime — end of a sprint, mid-sprint, or spanning multiple sprints.
- Not every sprint produces a public release. A sprint always produces an **increment** (working, tested software), but you may hold that increment until more features are ready.

---

## 10. Sprints

### What is a sprint?

A sprint is a fixed-duration work cycle — usually 1 to 4 weeks, with 2 weeks most common. It is the heart of Scrum.

At the end of each sprint, the team should have produced an **increment** — new functionality that is tested and “potentially releasable”.

### Sprint goal

Each sprint should have a **Sprint Goal** — a short sentence describing the value the sprint will deliver. It gives cohesion to selected stories.

**Example Sprint Goal:**

> *“By the end of this sprint, a user can register, log in, and recover their password if they forget it.”*

The Sprint Goal matters because:

- It gives the team a shared direction, not just a task list.
- It helps the team decide during the sprint (if something goes wrong, what matters most to preserve the goal?).
- It communicates value to stakeholders more clearly than a ticket list.

### Sprint backlog

The Sprint Backlog is the list of items selected from the Product Backlog for the current sprint, plus the plan for how the team will deliver them (tasks).

Unlike the Product Backlog (owned by the Product Owner), the Sprint Backlog belongs to the development team. The PO cannot add items to the Sprint Backlog during the sprint — new demands go to the Product Backlog and are considered in the next Sprint Planning.

### Sprint capacity

Sprint capacity is calculated from the team’s historical **velocity** — average story points delivered per sprint. In early sprints, the team estimates and adjusts as it learns real velocity.

Other factors affecting capacity:

- Holidays during the sprint.
- Team members on vacation or away.
- Time spent on other responsibilities (support, external meetings, etc.).

---

## 11. The product backlog

### What is the Product Backlog?

The Product Backlog is the ordered list of everything that needs to be done on the product. It is the single source of work for the Scrum team.

Product Backlog characteristics:

- **Prioritized**: Most important items at the top.
- **Dynamic**: Updated constantly as product and business evolve.
- **Detailed by proximity**: Items for upcoming sprints are detailed and estimated. Distant items stay high level.
- **Owned by the Product Owner**: The PO decides prioritization.

### Backlog refinement (grooming)

Backlog refinement is the activity (usually weekly) where the team reviews backlog items:

- Adds detail and acceptance criteria.
- Splits epics into stories when they are closer to being worked.
- Estimates story points for unestimated items.
- Removes obsolete items.
- Reorders when priorities change.

Refinement is not an official Scrum Guide ceremony, but it is universally considered good practice.

---

## 12. Scrum ceremonies

### 1. Sprint planning

**When:** At the start of each sprint.  
**Duration:** Up to 8 hours for a one-month sprint (proportionally less for shorter sprints).  
**Participants:** Full Scrum team (PO, Scrum Master, development team).

Sprint Planning answers two questions:

1. **What** will be delivered this sprint? (Story selection from the backlog)
2. **How** will the work be done? (Task creation)

The PO presents priority backlog items and answers questions. The team estimates and selects what fits the sprint based on historical velocity.

### 2. Daily Scrum (stand-up)

**When:** Every day, same time.  
**Duration:** Maximum 15 minutes.  
**Participants:** Development team (SM facilitates; PO may listen but is not required).

Goal: Synchronize the team and surface impediments. Classic three questions:

1. What did I do yesterday that contributed to the Sprint Goal?
2. What will I do today to contribute to the Sprint Goal?
3. Is anything blocking me?

**Important:** The Daily is not a status meeting for the manager. It is team synchronization for the team. Longer technical discussions happen after the Daily with relevant people.

### 3. Sprint review

**When:** At the end of each sprint.  
**Duration:** Up to 4 hours for a one-month sprint.  
**Participants:** Scrum team + invited stakeholders.

The team demonstrates what was delivered during the sprint. Stakeholders give feedback. The backlog may be adjusted based on what was learned.

**Important:** Sprint Review is not approval. It is collaboration and learning. The goal is to inspect the increment and adapt the backlog.

### 4. Sprint retrospective

**When:** After Sprint Review, before the next Sprint Planning.  
**Duration:** Up to 3 hours for a one-month sprint.  
**Participants:** Scrum team (no external stakeholders).

The retrospective focuses on the **process**, not the product. The team asks:

- What went well and should continue?
- What did not work and should change?
- What can we try again or differently?

The outcome should be **concrete actions** — specific items the team will implement next sprint to improve.

### 5. Backlog refinement

**When:** During the sprint (often mid-sprint).  
**Duration:** Usually 1–2 hours per week.  
**Participants:** PO + development team (SM facilitates).

Preparation for upcoming sprints. Discuss, detail, and estimate items that will be worked soon.

---

## 13. Scrum roles

### Product Owner (PO)

The PO represents business and user interests. Responsible for:

- Maximizing product value.
- Managing and prioritizing the Product Backlog.
- Ensuring the team understands what is being built and why.
- Scope decisions and accepting (or rejecting) deliveries.

The PO **does not** dictate how things should be built technically — that is the team’s responsibility.

### Scrum Master (SM)

The Scrum Master facilitates and guards the process. Responsible for:

- Ensuring Scrum is applied correctly.
- Removing impediments blocking the team.
- Protecting the team from external interference during the sprint.
- Facilitating ceremonies.
- Helping the team improve continuously.

The SM **is not** a traditional project manager. They do not assign tasks or chase individual results.

### Development team

The development team is self-managing and cross-functional. Responsible for:

- Estimating and committing to sprint work.
- Deciding how stories will be implemented.
- Ensuring quality of the increment produced.
- Creating and maintaining tasks.

“Development team” in Scrum includes everyone who contributes to building the product: developers, designers, QA, etc.

### Stakeholders

Not part of the Scrum team, but important:

- Participate in Sprint Reviews.
- Provide feedback and define business priorities (via the PO).
- Should not contact the team directly during the sprint to request changes — everything goes through the PO.

---

## 14. Essential concepts

### Definition of Done (DoD)

Definition of Done is the team’s agreement on what “done” means. Without it, “done” is subjective and a constant source of rework.

Typical DoD example:

- Code implemented and reviewed (code review approved).
- Unit tests written and passing.
- Integration tests written and passing.
- Tested in staging.
- No known high-severity bugs.
- Documentation updated (if applicable).
- Approved by the Product Owner.

DoD differs from acceptance criteria: DoD applies to **every item**; acceptance criteria are specific to each story.

### Velocity

Velocity is the average story points the team delivers per sprint. It is calculated over multiple sprints and used to predict how much work fits in future sprints.

**Example:**

- Sprint 1: 32 points delivered
- Sprint 2: 28 points delivered
- Sprint 3: 35 points delivered
- Average velocity: ~32 points

With that, when planning how many sprints a version needs, you divide total story points by velocity.

**Note:** Velocity is not an individual productivity metric. Do not use it to compare teams or pressure people. It is a planning tool.

### Burndown chart

A burndown chart shows remaining work in the sprint over time. The X axis is sprint days; the Y axis is remaining story points (or tasks).

A reference line shows the ideal expected pace. If the actual line is above reference, the team is behind plan; below means ahead.

### Increment

The increment is the sum of all Product Backlog items completed during a sprint, plus the value of all previous increments. It must be “potentially releasable” — functional, tested, and of quality suitable for production.

### Timebox

A timebox is the maximum time allocated for an activity. In Scrum, all events are timeboxed: sprints, dailies, planning, review, retrospective. When time is up, the event ends — even without a perfect conclusion. That forces the team to stay focused and efficient.

---

## 15. How versions, epics, and sprints relate

This is one of the most important points for seeing the full picture.

```
ROADMAP (high level — months/quarters)
│
├── v1.0 (MVP) ──────────── Sprint 1 ── Sprint 2 ── Sprint 3
│     ├── Epic: Registration              │            │
│     │     └── Stories...                │            │
│     └── Epic: Login ────────────────────┘            │
│           └── Stories...                             │
│                                                      │
├── v1.1 (urgent hotfix) ──────────────────────────────┘ (emergency sprint)
│     └── Critical production bug
│
├── v2.0 ──────────── Sprint 4 ── Sprint 5 ── Sprint 6 ── Sprint 7
│     ├── Epic: Checkout             │            │           │
│     │     └── Stories...           │            │           │
│     ├── Epic: Notifications ───────┘            │           │
│     │     └── Stories...                        │           │
│     └── Epic: Dashboard ────────────────────────┘           │
│           └── Stories...                                    │
│                                                             │
└── v2.1 (post-launch adjustments) ───────────────────────────┘
      └── Emergent stories
```

**Important points:**

- An epic can start in one version and finish in another.
- A sprint can contribute stories from multiple epics.
- A version can span multiple sprints.
- Intermediate versions (hotfixes) can be created anytime without “breaking” the plan.
- Future version planning is intentionally approximate — the farther out, the less detail.

---

## 16. Frequently asked questions

**“The team may not deliver everything planned for the sprint. What do we do?”**

If the team realizes during the sprint it will not finish everything, it should communicate immediately to the PO. Together they decide what can drop from the sprint without compromising the Sprint Goal. Incomplete stories return to the backlog — they are never counted as delivered.

**“Can the PO change requirements mid-sprint?”**

They should not. The sprint has closed scope to give the team stability to deliver. New demands enter the backlog and are considered in the next planning. In exceptional cases the PO can cancel a sprint — that should be rare.

**“How do we split a large story that does not fit in one sprint?”**

Common splitting techniques:

- By workflow (user process steps).
- By data variations (different input or output types).
- By acceptance criteria (each criterion becomes a story).
- By interface vs. logic (one story for backend, one for frontend — use carefully, as it hurts independence).
- Happy path first, then error cases.

**“Does Scrum work for small teams, like two people?”**

Yes, with adaptations. Very small teams can simplify ceremonies (e.g. 5-minute daily, monthly retrospective) and one person may wear PO and developer hats. What matters is keeping the principles: short iterations, frequent feedback, continuous adaptation.

**“What tool should we use to manage the backlog?”**

Depends on team and context. Popular options:

- **Jira**: Most complete and configurable; steep learning curve.
- **Linear**: Modern, fast; popular with tech teams.
- **Notion**: Flexible; good if the team already uses Notion for docs.
- **Trello**: Simple; good for small teams with basic needs.
- **GitHub Issues/Projects**: Great for teams already on GitHub.
- **Post-its on a wall**: Works well for co-located teams.

---

## 17. Visual summary

```
SPRINT (1–4 weeks, usually 2)
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Sprint Planning ──► Daily Scrums ──► Sprint Review     │
│       │                                     │           │
│  Sprint Backlog                        Increment        │
│  (stories + tasks)                   (software ready)   │
│                                             │           │
│                                    Sprint Retrospective │
└─────────────────────────────────────────────────────────┘

BACKLOG (always alive)
┌─────────────────────────────────────────────────────────┐
│  Epic A  │  Epic B  │  Epic C  │  Epic D  │  ...       │
│          │          │          │          │             │
│  Story 1 │  Story 4 │  Story 7 │  Spike   │             │
│  Story 2 │  Story 5 │  Story 8 │  Story 9 │             │
│  Story 3 │  Story 6 │  Bug      │          │             │
└─────────────────────────────────────────────────────────┘
          ↑ Priority decreases top to bottom

VERSIONS (delivery milestones to users)
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│  v1.0  │  │  v1.1  │  │  v2.0  │  │  v2.1  │  ...
│ MVP    │  │ Hotfix │  │ Major  │  │ Fixes  │
└────────┘  └────────┘  └────────┘  └────────┘
    ↑            ↑           ↑           ↑
  2 sprints   1 sprint    4 sprints   1 sprint
```

---

*This guide covers Scrum fundamentals and common practice extensions. The official Scrum Guide (scrumguides.org) is the reference for the framework’s core rules.*
