terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project               = var.project_id
  region                = var.region
  user_project_override = true
  billing_project       = var.project_id
}

locals {
  common_labels = {
    cost_center = var.cost_center
    environment = var.environment
    owner       = var.owner
    managed_by  = "terraform"
    project     = "rag-seguro-gcp"
  }
}

# Bucket de Storage para ingestao de documentos com labels FinOps
resource "google_storage_bucket" "bucket_fichas_raw" {
  name                        = "${var.project_id}-fichas-raw"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  labels = local.common_labels
}
