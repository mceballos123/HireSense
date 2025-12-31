terraform {
    backend "gcs"{
        bucket = "hiresense-bucket"
        prefix = "terraform/state"
    }
}