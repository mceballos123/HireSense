resource "google_container_cluster" "hiresense_cluster"{
    name = "hiresense-cluster"
    location = "us-west2-a"
    initial_node_count = 3

    node_config{
        machine_type = "e2-small"
        disk_size_gb = 12
    }
}