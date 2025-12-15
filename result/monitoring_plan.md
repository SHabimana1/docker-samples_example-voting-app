# Monitoring Plan - for Example Voting App

Tools
- Prometheus for collecting metrics
- Grafana for visualization and dashboards
- Alertmanager for alert notifications
- Docker metrics via cAdvisor

Metrics to Monitor
- CPU and memory usage per container
- Container uptime and restart count
- HTTP request rate and response time
- Error rate (4xx or 5xx)
- Redis and PostgreSQL availability

Alerting Strategy
- Alert if CPU usage > 80% for more than 5 minutes
- Alert if any container is down
- Alert if application endpoints are not reachable
- Alert if error rate exceeds defined threshold

Example Prometheus Configuration (in Pseudocode):
- alert: HighCPUUsage
  expr: cpu_usage > 80
  for: 5m
  labels:
    severity: warning
  annotations:
    description: CPU usage is above 80%