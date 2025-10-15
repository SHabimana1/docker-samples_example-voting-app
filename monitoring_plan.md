# Rencana Monitoring Aplikasi Voting

## 1. Alat yang Akan Digunakan

Untuk memastikan *observability* (kemampuan memantau dan memahami kondisi sistem), saya akan menggunakan tumpukan teknologi standar industri yang sering disebut "Stak PLG":

* **Prometheus**: Untuk mengumpulkan dan menyimpan metrik (data numerik) dari setiap layanan. Misalnya, penggunaan CPU, jumlah *request*, atau jumlah vote yang masuk
* **Loki**: Untuk mengumpulkan dan menganalisis log (catatan teks) dari semua container. Ini sangat berguna untuk *debugging* dan melacak *error*
* **Grafana**: Untuk membuat *dashboard* visual yang interaktif dari data metrik (Prometheus) dan log (Loki) agar mudah dibaca
* [cite_start]**Alertmanager**: Terintegrasi dengan Prometheus untuk mengirim notifikasi (misalnya ke email atau Slack) jika ada metrik yang melewati ambang batas tertentu

---
## 2. Metrik Kunci yang Akan Dipantau

Saya akan fokus pada tiga kategori metrik utama:

* **Metrik Sistem (Dasar)**:
* Penggunaan CPU dan Memori per container
* Ketersediaan (Uptime) setiap layanan
* Penggunaan disk pada volume database (`db-data`)

* **Metrik Aplikasi (Bisnis)**:
* **`http_requests_total`**: Jumlah total *request* HTTP yang diterima oleh layanan `vote` dan `result`.
* **`http_request_duration_seconds`**: Latensi atau waktu respons dari setiap *request*.
* Jumlah vote per detik yang masuk melalui layanan `vote`.
* Jumlah antrian di Redis untuk memastikan *worker* tidak kewalahan.

* **Metrik Database**:
* Jumlah koneksi aktif ke PostgreSQL
* Tingkat *query* per detik

---
## 3. Contoh Konfigurasi Prometheus

contoh dasar bagaimana file `prometheus.yml` akan dikonfigurasi untuk mengambil data metrik dari layanan yang berjalan. Ini mengasumsikan setiap layanan tersebut telah memiliki *endpoint* `/metrics`. [cite: 36]

```yaml
# prometheus.yml

scrape_configs:
  - job_name: 'voting-app'
    # Konfigurasi untuk menemukan target secara dinamis
    # dari layanan yang didefinisikan di Docker Compose
    static_configs:
      - targets: ['vote:80', 'result:80', 'worker:80']
        labels:
          group: 'production'