terraform {
  required_providers {
    # Kita menggunakan provider "kreuzwerker/docker" untuk berinteraksi dengan Docker lokal.
    # Ini memenuhi persyaratan "Infrastructure as Code" tanpa AWS.
    docker = {
      # Alamat sumber yang benar di Terraform Registry.
      source  = "kreuzwerker/docker"
      # Menggunakan versi yang stabil.
      version = "~> 3.0"
    }
  }
}

# Blok provider "docker" yang sebenarnya.
# Karena kita menggunakan Docker lokal di mesin host, tidak ada konfigurasi tambahan 
# (seperti region, access key, atau secret key) yang diperlukan di sini.
provider "docker" {}