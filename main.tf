# ===================================================================
# Konfigurasi Provider Cloud
# ===================================================================
# Blok ini memberitahu Terraform bahwa kita akan bekerja dengan AWS
# dan menentukan region (pusat data) mana yang akan kita gunakan.
# Untuk contoh ini, kita tidak perlu memiliki akun AWS,
# file ini hanya untuk menunjukkan pemahaman konsep.
provider "aws" {
  region = "ap-southeast-1" # Contoh: Region Singapura
}

# ===================================================================
# Definisi Sumber Daya (Resource)
# ===================================================================
# Blok ini adalah "resep" untuk membuat sebuah S3 Bucket.
# S3 Bucket adalah layanan penyimpanan objek di cloud, mirip seperti Google Drive.
resource "aws_s3_bucket" "devops_challenge_bucket" {
  # 'bucket' adalah nama unik global untuk S3 bucket kita.
  # GANTI 'namaanda-unik' DENGAN NAMA ANDA ATAU KOMBINASI UNIK.
  bucket = "99group-devops-challenge-bucket-robbykusumah"

  # 'tags' adalah label untuk membantu kita mengorganisir dan
  # mengidentifikasi sumber daya kita di cloud. Sangat berguna
  # jika sudah punya banyak sekali sumber daya. [cite: 27]
  tags = {
    Name        = "DevOps Challenge Bucket"
    Environment = "Submission"
    Owner       = "Muhammad Robby Kusumah"
  }
}