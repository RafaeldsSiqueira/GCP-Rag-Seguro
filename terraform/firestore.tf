# Banco de Dados Firestore Native para Vector Search
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# Service Account com permissao de acesso ao Cloud DLP, Firestore e Secret Manager
resource "google_service_account" "sa_rag_app" {
  account_id   = "sa-rag-seguro-app"
  display_name = "SA RAG Seguro App"
  description  = "Service Account para a API Cloud Run do RAG Seguro"
}

resource "google_project_iam_member" "sa_dlp_user" {
  project = var.project_id
  role    = "roles/dlp.user"
  member  = "serviceAccount:${google_service_account.sa_rag_app.email}"
}

resource "google_project_iam_member" "sa_datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.sa_rag_app.email}"
}

resource "google_project_iam_member" "sa_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.sa_rag_app.email}"
}
