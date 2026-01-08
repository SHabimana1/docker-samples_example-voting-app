resource "docker_network" "voting" {
  name = "voting-network"
}

resource "docker_volume" "db_data" {
  name = "voting-db-data"
}
