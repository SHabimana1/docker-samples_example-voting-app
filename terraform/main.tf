# Resource: docker_image
# Resource ini membuat image "redis:latest" di Docker host lokal.
resource "docker_image" "redis_image" {
  # Nama image yang akan ditarik dari Docker Hub
  name         = "redis:latest"
  # Menyimpan image di lokal setelah dibuat
  keep_locally = true 
}

# Resource: docker_container
# Resource ini membuat dan menjalankan container Redis.
resource "docker_container" "redis_container" {
  # Nama container unik yang akan terlihat di 'docker ps'
  name  = "voting-app-redis-tf" 
  image = docker_image.redis_image.name 
  # Konfigurasi port agar Redis dapat diakses dari luar container
  ports {
    internal = 6379 # Port Redis di dalam container
    external = 6379 # Port yang diekspos ke host lokal (port 6379 di mesin Anda)
  }
}

# Output
# Output ini akan menampilkan ID container sebagai bukti deployment berhasil.
output "redis_container_id" {
  description = "ID unik dari container Redis yang dibuat."
  value       = docker_container.redis_container.id
}