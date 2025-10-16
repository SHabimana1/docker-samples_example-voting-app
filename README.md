# Voting App - 99Group DevOps Challenge

Halo tim 99Group, perkenalkan nama saya **[MUHAMMAD ROBBY KUSUMAH]**.

Selamat datang di submission saya untuk tantangan DevOps Internship. Di sini, saya tidak hanya sekadar menjalankan aplikasi, tetapi juga membangun fondasi DevOps yang baik: automasi, containerization, dan perencanaan untuk production.

### 🚀 **Link Video Walkthrough**
[]

---

## ⚙️ Cara Menjalankan Proyek Ini (Getting Started)

Saya sudah merancang agar proyek ini bisa berjalan di komputer mana pun hanya dengan beberapa perintah.

**Prasyarat:**
* Git
* Docker & Docker Compose

**Langkah-langkah:**
1.  **Clone repositori** ini ke komputer Anda.
2.  **Masuk ke direktori proyek** melalui terminal.
3.  Jalankan `docker-compose up --build`. Perintah ini akan secara otomatis membangun *image* untuk setiap service dari `Dockerfile` yang sudah saya siapkan dan menjalankannya.
4.  Selesai! Buka browser Anda dan akses:
    * **Aplikasi Voting**: `http://localhost:5000`
    * **Halaman Hasil**: `http://localhost:5001`
5.  Untuk mematikan semua service, kembali ke terminal, tekan `Ctrl + C`, lalu jalankan `docker-compose down`.

---

## 💡 Pendekatan dan Keputusan Desain Saya

Berikut adalah pemikiran di balik beberapa pilihan teknis yang saya buat:

#### 1. Containerization yang Efisien
Tujuan utama saya adalah agar siapa pun di tim bisa menjalankan aplikasi ini dengan satu perintah. `docker-compose` adalah pilihan yang jelas. Untuk `Dockerfile`-nya, saya tidak hanya membuatnya berjalan, tapi saya optimalkan menggunakan **multi-stage builds**. Hasilnya? *Image* yang jauh lebih kecil, lebih aman, dan proses *build* yang lebih cepat—semua adalah praktik terbaik di industri.

#### 2. CI sebagai Penjaga Gerbang Kualitas
Saya menggunakan **GitHub Actions** untuk membuat pipeline CI sederhana. Tujuannya adalah sebagai 'penjaga gerbang' kualitas. Setiap kali ada kode baru yang akan digabung ke *branch* `main`, pipeline ini akan otomatis berjalan untuk memastikan dependensi ter-install dengan benar dan tidak ada yang rusak. Ini adalah langkah pertama menuju automasi yang lebih canggih.

#### 3. Infrastructure as Code (IaC) sebagai Fondasi
Meskipun ini bonus, saya percaya IaC adalah fondasi DevOps. Saya menyertakan file `main.tf` (Terraform) sederhana untuk mendefinisikan S3 bucket. Ini menunjukkan bagaimana kita bisa mulai mengelola infrastruktur cloud kita menggunakan kode—yang membuatnya bisa di-*version control*, di-*review*, dan diterapkan ulang dengan konsisten.

---

## 📈 Apa yang Akan Saya Lakukan Selanjutnya?

DevOps adalah tentang perbaikan berkelanjutan. Jika saya punya lebih banyak waktu, ini adalah hal-hal yang akan saya kerjakan berikutnya:

1.  **Pengujian yang Serius (Robust Testing):** Menambahkan *unit test* dan *integration test* yang sesungguhnya, lalu menjalankannya secara otomatis di pipeline CI untuk benar-benar memastikan kualitas kode.
2.  **Keamanan Terintegrasi (Shift-Left Security):** Mengintegrasikan pemindai keamanan seperti **Trivy** langsung di pipeline CI. Ini akan memindai *vulnerability* pada *image* Docker sebelum mereka sampai ke produksi.
3.  **Pipeline Deployment Otomatis (CD):** Membangun *workflow* lanjutan di GitHub Actions untuk secara otomatis mem-push *image* yang sudah lolos uji ke *container registry* (seperti Docker Hub atau AWS ECR), lalu men-deploy-nya ke lingkungan *staging* atau bahkan produksi.

Terima kasih telah meluangkan waktu untuk meninjau pekerjaan saya!