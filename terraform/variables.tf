variable "project_id" {
  type        = string
  description = "ID do projeto GCP"
  default     = "poc-rag-seguro-gcp-042"
}

variable "region" {
  type        = string
  description = "Região principal do GCP"
  default     = "us-central1"
}

variable "cost_center" {
  type        = string
  description = "Centro de Custo FinOps corporativo"
  default     = "cc-ia-genai-042"
}

variable "environment" {
  type        = string
  description = "Ambiente de implantação"
  default     = "poc"
}

variable "owner" {
  type        = string
  description = "Responsável técnico pelo recurso"
  default     = "rafael-siqueira"
}
