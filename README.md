# 99Group Voting App - Role Challenge 

Aplikasi terdiri dari 5 service utama:

1. Vote: Web berbasis Flask (Python) untuk memberi suara
2. Result: Web berbasis Node.js untuk menampilkan hasil
3. Worker: Berbasis .NET yang memproses suara
4. Redis: Menyimpan antrian vote sementara (in-memory queue)
5. PostgreSQL: Database untuk penyimpanan permanen hasil vote

---

How to do it

- Docker & Docker Compose terinstal
- Git

Menjalankan secara lokal

```bash
git clone https://github.com/sblrm/example-voting-app.git
cd example-voting-app
docker-compose up --build
```

## Akses Aplikasi

Setelah semua container berjalan, akses aplikasi di browser:

Vote App: [http://localhost:5000](http://localhost:5000) - Untuk memberikan suara
Result App: [http://localhost:5001](http://localhost:5001) - Untuk melihat hasil voting
Grafana: [http://localhost:3000](http://localhost:3000) - Dashboard monitoring (admin/admin)
Prometheus: [http://localhost:9090](http://localhost:9090) - Metrics explorer

---

## Monitoring & Logging

Aplikasi dilengkapi dengan Grafana Stack:
1. Prometheus: Metrics collection dari Worker service
2. Grafana: Dashboard visualisasi (login: admin/admin)
3. Loki + Promtail: Centralized logging dari Docker containers

Worker service diimplementasikan dengan metrics:
1. `worker_votes_processed_total`: Total votes processed
2. `worker_redis_connected`: Redis connection status
3. `worker_db_connected`: Database connection status

---

## CI/CD Pipeline

Menggunakan GitHub Actions untuk otomatisasi:

1. Menjalankan pipeline setiap push/PR ke branch `main`
2. Menjalankan unit test untuk service `vote` dan `result`
3. Build image Docker untuk memvalidasi

Keuntungan: otomatisasi testing dan build sehingga mempermudah collaborate dan deployment

---

## Praktik Docker yang Diterapkan

1. Multi-Stage Build: mengurangi ukuran image hingga 70%
2. Non-root User: meningkatkan keamanan container
3. Base Image Minimal (Alpine): mempercepat deployment
4. Health Checks: memantau status container
5. .dockerignore: menghindari agar file tidak penting masuk ke image

---

## Infrastruktur sebagai Kode (IaC)

Menggunakan Terraform untuk provisioning resource seperti:

* S3 Bucket untuk penyimpanan artefak
* EC2 Instance sebagai host Docker
* Security Group untuk pengaturan akses jaringan

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

---

## Alasan Desain

1. Multi-stage Build: Image lebih ringan dan aman
2. Docker Compose Networks: Keamanan antar service
3. GitHub Actions CI/CD: Otomatisasi testing dan build
4. Terraform: Infrastruktur reproducible
5. Alpine Image: Deployment lebih cepat dan efisien

---

## Rencana Pengembangan Selanjutnya

- Jangka Pendek (1–2 Minggu)

1. Tambahkan endpoint `/health` dan `/ready` untuk health check
2. Implementasi monitoring sederhana dengan Prometheus + Grafana
3. Penambahan log aggregation dengan Loki

- Jangka Menengah (1–2 Bulan)

1. Helm chart untuk deployment Kubernetes
2. Staging environment dengan docker-compose terpisah
3. Pengelolaan secrets menggunakan AWS Secrets Manager

- Jangka Panjang (3–6 Bulan)

1. Migrasi ke Kubernetes
2. Implementasi service mesh (Istio)
3. Distributed tracing (Jaeger)
4. GitOps workflow (ArgoCD)

---

## Testing

```bash
docker-compose build
docker-compose up -d
curl http://localhost:5000  # Halaman voting
curl http://localhost:5001  # Halaman hasil voting
```

---

## Pemeliharaan & Backup

1. Backup database otomatis ke S3
2. Konfigurasi tersimpan di Git (version control)
3. Secrets dikelola dengan aman di AWS Secrets Manager