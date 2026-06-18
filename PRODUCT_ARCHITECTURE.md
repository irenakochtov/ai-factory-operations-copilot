# AI Factory Operations Copilot

## Vision

Modern AI Factories generate thousands of alerts every hour from multiple disconnected systems.

Operators must manually correlate information coming from:

- BMS
- DCIM
- GPU telemetry
- Kubernetes
- Slurm
- InfiniBand
- Environmental monitoring
- Network monitoring

This process is slow, error-prone and highly dependent on expert knowledge.

The goal of the AI Factory Operations Copilot is to act as an intelligent operational assistant that correlates signals across systems, identifies root causes, predicts future failures and recommends actions before service disruption occurs.

---

## Problem

Today's monitoring tools answer:

"What happened?"

Operators still need to determine:

- Why it happened
- Which alerts are symptoms
- What the root cause is
- Which systems are affected
- Which team should respond
- What happens next if nothing is done

In large GPU clusters and AI factories, delays in diagnosis can cause:

- Training failures
- Lost GPU utilization
- SLA violations
- Increased operational costs
- Service downtime

---

## Target Users

### Primary Users

- Data Center Operators
- NOC Engineers
- AI Infrastructure Engineers
- SRE Teams
- HPC Operations Teams

### Secondary Users

- Facilities Teams
- Platform Teams
- Network Teams
- Operations Managers

---

## MVP Scope

The MVP focuses on incident correlation and operational decision support.

Input:

- Synthetic BMS events
- Synthetic cooling events
- Synthetic power events
- Synthetic GPU telemetry
- Synthetic network telemetry
- Synthetic workload telemetry

Output:

- Incident classification
- Root cause analysis
- Severity assessment
- Business impact assessment
- Escalation recommendation
- Predicted next failure
- Recommended operational action

---

## What We Are NOT Building

Not in MVP:

- Real-time streaming platform
- Production Kubernetes deployment
- Multi-agent orchestration
- Autonomous remediation
- Full digital twin
- Frontend dashboard

The MVP goal is decision intelligence, not infrastructure engineering.

---

## Architecture

                     +------------------+
                     | Synthetic Events |
                     +--------+---------+
                              |
                              v
                   +----------------------+
                   | Incident Aggregator |
                   +----------+-----------+
                              |
                              v
                   +----------------------+
                   | AI Operations Copilot|
                   |   Qwen3-30B-A3B      |
                   +----------+-----------+
                              |
                              v
                 +--------------------------+
                 | Incident Assessment JSON |
                 +------------+-------------+
                              |
                              v
                 +--------------------------+
                 | Human Readable Report    |
                 +--------------------------+

---

## Incident Workflow

Step 1

Receive incident signals from multiple systems.

Step 2

Correlate related alerts.

Step 3

Identify likely root cause.

Step 4

Estimate business impact.

Step 5

Predict probable next failure.

Step 6

Recommend immediate actions.

Step 7

Recommend workload actions.

Step 8

Recommend escalation team.

---

## Example Input

{
  "rack_temperature_c": 36,
  "gpu_utilization_percent": 98,
  "packet_loss_percent": 2.1,
  "nccl_latency_ms": 240,
  "training_step_ms": 980
}

---

## Example Output

{
  "incident_type": "network_risk",
  "severity": "high",
  "root_cause": "InfiniBand degradation",
  "confidence_score": 95,
  "predicted_failure":
      "Distributed training failure",
  "recommended_action":
      "Inspect InfiniBand switch ports",
  "recommended_workload_action":
      "Move critical workloads to healthy racks",
  "escalation_team": "Network"
}

---

## Success Criteria

The system successfully:

- Correlates signals from multiple domains
- Identifies root cause
- Predicts likely future failures
- Produces actionable recommendations
- Reduces investigation time

---

## Future Roadmap

Phase 2

Historical incident memory

Phase 3

RAG over operational runbooks

Phase 4

Real Prometheus and DCGM ingestion

Phase 5

LangGraph workflow orchestration

Phase 6

Digital Twin integration

Phase 7

Automated remediation recommendations