# AI Factory Incident Triage Copilot - Dataset V2 Starter

This starter creates a synthetic multi-source incident dataset.

Each incident contains separate event groups:

- bms_events
- dcim_events
- gpu_events
- network_events
- power_events
- storage_events
- workload_events
- security_events
- environmental_events

Project assumption:
The MVP does not solve real-world BMS/DCIM/OT integration.
It assumes the data already flows into JSON, then focuses on incident triage and LLM evaluation.

Run:

```bash
python3 generate_dataset_v2.py
```

Output:

```bash
dataset_v2.json
```
