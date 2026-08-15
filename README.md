# MiniKubeX

A lightweight Kubernetes-inspired container orchestration platform built with Python, FastAPI, Docker, Redis, and PostgreSQL.

MiniKubeX demonstrates core container-orchestration concepts such as desired-state reconciliation, deployment management, self-healing replicas, rolling updates, rollback, service discovery, service registration, and round-robin load balancing.

---

## 🚀 Features

### Deployment Management
- Create and manage container deployments
- Define desired replica counts
- Track deployment status and available replicas
- Maintain deployment versions
- Support deployment updates and rollback

### Self-Healing & Reconciliation
MiniKubeX continuously compares the desired deployment state with the actual Docker state.

If a replica fails or disappears:

```text
Desired State
     ↓
3 replicas
     ↓
Actual State
     ↓
2 healthy replicas
     ↓
Reconciliation
     ↓
Create missing replica
     ↓
3 healthy replicas
