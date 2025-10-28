# Monitoring & Logging Setup

## Stack yang Digunakan
1. **Prometheus**: Mengumpulkan dan menyimpan metrik
2. **Grafana**: Visualisasi dashboard
3. **Loki**: Agregasi log
4. **Promtail**: Mengumpulkan log dari Docker containers

## Quick Start

```bash
# Start semua services
docker compose up --build -d

# Akses aplikasi
Vote:       http://localhost:5000
Result:     http://localhost:5001
Grafana:    http://localhost:3000  (admin/admin)
Prometheus: http://localhost:9090
```

## Konfigurasi Prometheus

File: `prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'worker'
    static_configs:
      - targets: ['worker:8080']
```

**Targets**:
- Prometheus self-monitoring
- Worker service metrics (port 8080)

## Konfigurasi Promtail

File: `promtail-config.yml`

**Fitur**:
- Auto-discovery Docker containers
- Filtering by container name (voting-app)
- Service name extraction otomatis
- Push logs ke Loki

## Grafana Dashboard

File: `grafana/provisioning/dashboards/voting-app-dashboard.json`

**Panels (7 total)**:

**Metrics (4 panels)**:
1. Vote Processing Rate - Grafik rate processing
2. Redis Status - Indikator koneksi (green/red)
3. Database Status - Indikator koneksi (green/red)
4. Total Votes - Gauge counter

**Logs (3 panels)**:
5. All Application Logs - Semua service
6. Worker Logs - Worker service saja
7. Vote Logs - Vote service saja

**Auto-provisioning**:
- Datasources (Prometheus + Loki) otomatis terkonfigurasi
- Dashboard otomatis muncul tanpa manual import

## Metrics yang Tersedia

**Worker Service**:
- `worker_votes_processed_total`: Total votes diproses
- `worker_votes_errors_total`: Total error
- `worker_redis_connected`: Status Redis (1=connected, 0=disconnected)
- `worker_db_connected`: Status Database (1=connected, 0=disconnected)

## Testing

```bash
# Cast votes
curl -X POST http://localhost:5000 -d "vote=a"

# Check metrics
curl http://localhost:8080/metrics | grep worker_

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets
```

## Troubleshooting

**Dashboard tidak muncul**:
```bash
# Restart Grafana
docker compose restart grafana
```

**Metrics tidak muncul**:
```bash
# Check Prometheus targets
http://localhost:9090/targets
# Semua harus status "UP"
```

**Logs tidak muncul**:
```bash
# Check Promtail logs
docker logs promtail
```
