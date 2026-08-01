# Template de Inspecao do Cloud DLP para identificacao de PII (Nomes e Locais)
resource "google_data_loss_prevention_inspect_template" "dlp_inspect_template" {
  parent       = "projects/${var.project_id}"
  description  = "Template de inspecao de PII para RAG Seguro (DC/Marvel)"
  display_name = "Template Inspecao PII RAG"

  inspect_config {
    info_types {
      name = "PERSON_NAME"
    }
    info_types {
      name = "LOCATION"
    }
    info_types {
      name = "STREET_ADDRESS"
    }

    min_likelihood = "LIKELY"

    limits {
      max_findings_per_request = 100
      max_findings_per_item    = 100
    }
  }
}
