# AI Factory Operations Copilot

AI-powered incident triage and operational decision support system for AI factories, GPU clusters, and modern data center environments.

---

## Overview

Modern AI factories generate thousands of alerts across multiple operational domains:

- BMS
- DCIM
- GPU telemetry
- InfiniBand networks
- Power systems
- Cooling systems
- Environmental monitoring
- Workload orchestration platforms

Operators often receive alerts from multiple systems without understanding:

- What is the real root cause?
- Which alerts are symptoms?
- Which team should respond?
- What will fail next?
- What action should be taken immediately?

This project demonstrates an AI Operations Copilot capable of analyzing multi-source infrastructure incidents and generating structured operational recommendations.

---

## Project Goals

The goal of this project is to build a working prototype of an AI Factory Operations Copilot.

The system helps NOC and data center operations teams analyze multi-source infrastructure incidents from AI factories and GPU data centers.

The prototype focuses on:

- Correlating alerts from multiple operational domains
- Identifying likely root cause
- Predicting the next possible failure
- Estimating severity and time to critical impact
- Recommending first operational actions
- Routing incidents to the correct escalation team
- Evaluating model predictions against ground truth

The MVP is designed to demonstrate operational intelligence, not full production monitoring.

---

## Target Users

Primary users:

- NOC Engineers
- Data Center Operations Engineers
- Critical Facilities Engineers
- AI Infrastructure Engineers
- SRE Teams
- Platform Operations Teams

---

## MVP Scope

Current MVP capabilities:

✅ Synthetic AI Factory incident dataset

✅ Multi-source incident analysis

✅ AI-powered root cause identification

✅ Severity classification

✅ Escalation team recommendation

✅ Operational action recommendation

✅ Business impact assessment

✅ Predicted next failure

✅ Asset history support

✅ Evaluation framework

✅ FastAPI service

✅ Swagger API documentation

---

## Technology Stack

### AI Layer

- Nebius Token Factory
- Qwen3-30B-A3B-Instruct-2507
- OpenAI Compatible API

### Backend

- Python 3
- FastAPI
- Uvicorn

### Data

- JSON datasets
- Synthetic incident scenarios
- Asset history context

### Evaluation

- Ground truth validation
- Accuracy measurement
- Classification scoring

---

## Architecture

```text
dataset_v2.json
       +
asset_history.json
       |
       v
FastAPI Service
       |
       v
Incident Loader
       |
       v
AI Factory Operations Copilot
       |
       v
Qwen3-30B-A3B
       |
       v
Structured Incident Analysis
       |
       v
Operational Recommendation
```

---

## Project Structure

```text
serverlessv2/

├── api.py
├── copilot.py
├── evaluate.py
├── dataset_v2.json
├── asset_history.json
├── requirements.txt
├── PRODUCT_ARCHITECTURE.md
├── README_dataset_v2.md
├── README.md
├── results/
└── .env
```

---

## API Endpoints

### Health Check

```http
GET /
```

Returns service status.

---

### List Incidents

```http
GET /incidents
```

Returns available incidents from the dataset.

---

### Analyze Incident

```http
POST /analyze/{incident_id}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/analyze/INC-0016
```

---

## Example Output

```json
{
  "incident_type": "network_risk",
  "severity": "high",
  "root_cause": "InfiniBand fabric packet loss causing NCCL communication slowdown",
  "affected_systems": [
    "InfiniBand network fabric",
    "GPU cluster",
    "Distributed AI training workloads"
  ],
  "escalation_team": "Network",
  "recommended_action": "Inspect affected InfiniBand switch ports",
  "priority_score": 80,
  "confidence_score": 95,
  "time_to_critical_minutes": 30
}
```

---

## Evaluation

Run evaluation:

```bash
python3 evaluate.py
```

Current baseline results:

- Severity Accuracy: 80%
- Incident Type Accuracy: 100%
- Escalation Team Accuracy: 100%
- Overall Accuracy: 93.33%

---

## Installation

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Running The API

Start FastAPI:

```bash
python -m uvicorn api:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

## Current Project Status

### Completed

- Dataset generation
- Ground truth labels
- AI Copilot implementation
- FastAPI integration
- Swagger documentation
- Evaluation framework
- Asset history support

### Planned

- Correlation Engine
- Historical context analysis
- Risk scoring engine
- Business impact engine
- Timeline reconstruction
- Prometheus integration
- DCGM integration
- Grafana dashboard
- ServiceNow integration

---

## Disclaimer

This project is a proof-of-concept prototype developed for AI Factory Operations and AI Infrastructure research and demonstration purposes.

It is not intended for direct production deployment without additional validation, security controls, observability, and operational testing.

---

## Author

Irena Kochtov

Nebius Academy – AI Performance Engineering