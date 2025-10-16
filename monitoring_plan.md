# Rencana Monitoring Aplikasi Voting

Dokumen ini menjelaskan pendekatan saya untuk memastikan aplikasi ini berjalan dengan sehat di lingkungan produksi dan bagaimana kita bisa tahu jika ada masalah, bahkan sebelum pengguna mengeluh.

## 1. Filosofi dan Peralatan Andalan

Filosofi saya adalah "kita tidak bisa memperbaiki apa yang tidak bisa kita ukur". Oleh karena itu, saya akan menggunakan beberapa alat standar industri yang saling melengkapi:

* **Prometheus sebagai Mata-Mata:** Anggap Prometheus ini seperti agen yang terus-menerus mengumpulkan angka-angka penting (metrik) dari setiap sudut aplikasi kita—seberapa sibuk CPU-nya, berapa banyak memori yang terpakai, dan lain-lain.
* **Grafana sebagai Dasbor Utama:** Semua data angka yang dikumpulkan Prometheus tidak akan berarti jika sulit dibaca. Grafana akan mengubah angka-angka tersebut menjadi grafik dan dasbor visual yang cantik. Dalam 5 detik, kita bisa melihat apakah semua lampu hijau atau ada yang merah.
* **Loki sebagai Buku Catatan Terpusat:** Setiap kontainer menghasilkan log (catatan aktivitas). Jika terjadi error, log adalah tempat pertama kita mencari tahu "apa yang sebenarnya terjadi?". Loki akan mengumpulkan semua log ini di satu tempat, sehingga kita tidak perlu login ke setiap server untuk mencari jejak masalah.
* **Alertmanager sebagai Alarm Darurat:** Jika Prometheus melihat ada angka yang aneh (misalnya, error melonjak tinggi), Alertmanager akan bertindak sebagai alarm yang akan langsung memberi tahu tim melalui Slack atau email, lengkap dengan detail masalahnya.

## 2. Apa Saja yang Perlu Diawasi?

Saya akan fokus memantau tiga area utama:

#### a. Kesehatan Infrastruktur (Apakah Mesinnya Sehat?)
Ini adalah fondasinya. Jika mesinnya bermasalah, aplikasi pasti bermasalah.
* **Penggunaan CPU & Memori:** Apakah ada service yang "rakus" sumber daya? Jika CPU mendekati 100%, aplikasi akan melambat.
* **Kesehatan Kontainer:** Apakah semua kontainer berjalan? Atau ada yang sering mati dan hidup kembali (crash-loop)?

#### b. Pengalaman Pengguna (Apakah Pengguna Senang?)
Ini adalah metrik yang paling penting karena berdampak langsung pada pengguna.
* **Latency (Waktu Respons):** Butuh berapa milidetik bagi aplikasi untuk merespons klik dari pengguna? Jika terlalu lama, pengguna akan frustrasi.
* **Error Rate (Tingkat Kegagalan):** Dari 100 permintaan, berapa banyak yang gagal? Kita harus menargetkan angka ini serendah mungkin (misalnya, di bawah 0.1%).
* **Throughput (Beban Kerja):** Berapa banyak permintaan yang bisa dilayani aplikasi setiap detiknya? Ini membantu kita merencanakan kapasitas server.

#### c. Kesehatan Internal (Apakah di Belakang Layar Lancar?)
Aplikasi ini memiliki antrean data (`queue`) antara `vote` dan `worker`.
* **Kedalaman Antrean (Queue Depth):** Berapa banyak vote yang menunggu untuk diproses oleh `worker` di Redis? Jika angka ini terus bertambah, itu artinya `worker` kita kewalahan dan tidak bisa mengimbangi jumlah vote yang masuk.

## 3. Contoh Skenario Peringatan (Alert)

Teori saja tidak cukup. Berikut adalah contoh skenario nyata:

**Skenario:** Tiba-tiba, banyak pengguna gagal melakukan vote.

1.  **Deteksi:** Prometheus melihat metrik `http_requests_total{status="5xx"}` (jumlah request error) untuk `vote-app` melonjak tajam selama 2 menit.
2.  **Peringatan:** Alertmanager langsung mengirim pesan ke channel Slack tim:
    > **"🚨 Waspada! Tingkat Error Aplikasi Vote Tinggi! 🚨**
    >
    > Tingkat error telah melampaui 5% dalam 2 menit terakhir. Kemungkinan ada masalah di service `vote` atau dependensinya. Mohon segera diperiksa."
3.  **Investigasi:** Tim membuka dasbor Grafana untuk melihat grafik mana yang aneh. Mereka juga membuka Loki untuk mencari log error spesifik yang terjadi saat itu.

Dengan pendekatan ini, kita bisa proaktif menyelesaikan masalah, bukan reaktif setelah pengguna marah-marah.