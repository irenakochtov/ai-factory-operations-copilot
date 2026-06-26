# AI Factory Operations Copilot

## AI-Powered Operational Intelligence for AI Factories

AI Factory Operations Copilot is an AI-powered operations copilot designed for modern AI factories, GPU clusters, and mission-critical data center environments.

The platform transforms raw infrastructure alerts into actionable operational intelligence by combining deterministic classification, AI-powered reasoning, failure prediction, risk assessment, and multi-incident correlation.

Instead of reacting to hundreds of disconnected alerts, operators receive a single operational assessment with root cause analysis, risk scoring, failure forecasting, and recommended actions.

Built entirely on Nebius AI and Serverless infrastructure.

---

# Why AI Factories?

AI factories are fundamentally different from traditional data centers.

Large GPU clusters depend on tightly coupled cooling systems, power infrastructure, network fabrics, and storage platforms.

A single cooling issue can rapidly impact:

- GPU utilization
- AI training jobs
- Inference workloads
- Service availability
- Business outcomes

Traditional monitoring platforms generate alerts.

Operations teams still need to answer:

- What is actually happening?
- Which alerts are related?
- What is the root cause?
- Who should respond?
- What will fail next?
- What is the overall site risk?

AI Factory Operations Copilot was built to answer those questions automatically.

---

# The Problem

Modern AI infrastructure generates alerts from multiple operational domains:

- Building Management Systems (BMS)
- Data Center Infrastructure Management (DCIM)
- NVIDIA DCGM
- Prometheus
- Network Monitoring
- Storage Monitoring

These alerts often arrive independently, making incident investigation slow and reactive.

Operations teams spend valuable time correlating signals manually before they can begin remediation.

---

# The Solution

AI Factory Operations Copilot converts infrastructure alerts into operational intelligence.

The platform automatically:

- Correlates operational events
- Classifies incidents
- Identifies probable root causes
- Recommends corrective actions
- Forecasts future failures
- Simulates failure propagation
- Calculates site-wide risk
- Detects related incident clusters

The result is faster incident response, improved operational awareness, and reduced mean time to resolution (MTTR).

---

# Example Scenario

## Input Alert

GPU-07 temperature reaches 92°C.

## AI Factory Operations Copilot

The platform automatically:

- Identifies a cooling risk
- Correlates rack-level signals
- Determines the likely root cause
- Predicts GPU throttling within 15 minutes
- Predicts GPU shutdown within 30 minutes
- Calculates site-wide risk impact
- Recommends workload migration
- Escalates the incident to Facilities

Instead of a raw alert, operators receive an actionable operational assessment.

---

# Architecture

## Data Sources

- Prometheus Alerts
- BMS
- DCIM
- NVIDIA DCGM
- Network Telemetry
- Storage Telemetry

## Processing Pipeline

1. Alert Ingestion
2. Incident Normalization
3. Correlation Engine
4. Deterministic Classification Engine
5. LLM Analysis
6. Validation Layer
7. Failure Forecast Engine
8. Failure Cascade Simulation
9. Risk Summary Engine
10. Incident Clustering Engine

## Outputs

- Root Cause Analysis
- Severity Classification
- Escalation Team Recommendation
- Operational Recommendations
- Business Impact Assessment
- Failure Forecast Timeline
- Failure Cascade Simulation
- Site Risk Score
- Incident Clusters

---

# Built on Nebius

This project uses multiple Nebius services to provide scalable AI-powered operational intelligence.

## Nebius Token Factory

Provides secure access to foundation models hosted on Nebius AI infrastructure.

Used for:

- Root Cause Analysis
- Executive Incident Summaries
- Business Impact Assessment
- Operational Recommendations
- Failure Prediction

## Nebius Serverless Endpoint

Hosts the production FastAPI inference service.

Provides:

- Serverless API deployment
- Automatic scaling
- Managed inference infrastructure

## Nebius Serverless Job

Runs automated evaluation and validation workflows.

Used for:

- Model evaluation
- Accuracy testing
- Validation reporting

## Nebius Container Registry

Stores and distributes production container images.

Used for:

- Docker image storage
- Versioned deployments
- Serverless endpoint updates

---

# Core Features

## Incident Intelligence

Transforms infrastructure alerts into structured operational incidents.

---

## Root Cause Analysis

Identifies the most likely cause of operational failures and infrastructure degradation.

Example:

```text
Cooling failure detected in Rack D11.

Root Cause:
Low coolant flow in CDU BMS-08 causing rack thermal imbalance and GPU overheating.
```

---

## Failure Forecast

Predicts likely operational impact over:

- 15 Minutes
- 30 Minutes
- 60 Minutes

Example:

```text
15 Minutes:
GPU thermal throttling may begin

30 Minutes:
Affected GPU nodes may reach shutdown threshold

60 Minutes:
Rack-level workload disruption may occur
```

---

## Failure Cascade Simulation

Predicts how incidents may propagate through AI infrastructure.

Example:

```text
GPU Overheating
      ↓
GPU Throttling
      ↓
GPU Shutdown
      ↓
Training Failure
      ↓
SLA Violation
```

---

## Risk Summary

Provides site-wide operational visibility.

Example:

```text
Risk Score: 96
Critical Incidents: 5
Top Risk Domain: Network
```

---

## Incident Clustering

Groups related incidents and identifies probable common causes.

Example:

```text
Cooling Risk

INC-0003
INC-0008
INC-0010

Confidence: 85%
```

---

# API Endpoints

## Incident Analysis

```http
POST /analyze_alert

POST /analyze/{incident_id}
```

Analyzes incidents and generates operational intelligence.

---

## Correlation

```http
GET /correlation/{incident_id}
```

Returns correlated operational context for an incident.

---

## Risk Assessment

```http
GET /risk_summary
```

Provides site-wide operational risk visibility.

---

## Incident Clustering

```http
GET /incident_clusters
```

Groups related incidents and identifies common causes.

---

## Dataset Exploration

```http
GET /incidents
```

Lists available demo incidents.

---

# Evaluation Results

The platform includes an automated evaluation framework.

## Evaluation Metrics

- Severity Accuracy
- Incident Type Accuracy
- Escalation Team Accuracy

## Current Evaluation

```text
Total Incidents: 10

Severity Accuracy: 100%
Incident Type Accuracy: 100%
Escalation Team Accuracy: 100%

Overall Accuracy: 100%
```

Evaluation reports are automatically generated and stored during validation runs.

---

# Results

The platform successfully demonstrates:

- Incident Correlation
- Root Cause Analysis
- Failure Forecasting
- Failure Cascade Simulation
- Site-Wide Risk Scoring
- Incident Clustering
- Operational Recommendations
- Production API Deployment on Nebius Serverless

---

# Repository Structure

```text
api.py
pipeline.py
classification_engine.py
correlation_engine.py
forecast_engine.py
cascade_engine.py
risk_engine.py
cluster_engine.py
validation_engine.py
evaluate.py
dataset_v2.json
```

---

# Running Locally

## Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start API

```bash
python api.py
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# Docker Deployment

## Build Image

```bash
docker build -t ai-factory-copilot .
```

## Run Container

```bash
docker run -p 8000:8000 ai-factory-copilot
```

---

# Future Enhancements

- Real-Time Prometheus Integration
- Historical Incident Learning
- Automated Remediation Workflows
- Multi-Site Correlation
- Live Operations Dashboard
- Agent-Based Incident Investigation
- Predictive Capacity Planning

---

# Built For

**Nebius Serverless AI Builders Challenge 2026**

AI-powered operational intelligence for the next generation of AI factories.

---

## Author

Irena Kochtov

Infrastructure • Data Center Operations • Cloud • AI Infrastructure

AWS Solutions Architect | Nebius AI Performance Engineering