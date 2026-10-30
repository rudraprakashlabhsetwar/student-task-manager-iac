variable "cloudflare_api_token" {
  description = "Cloudflare API Token with Workers Scripts and Workers KV edit permissions"
  type        = string
  sensitive   = true
}

variable "account_id" {
  description = "Cloudflare Account ID"
  type        = string
  default     = "f4984c3282a5a5d31d6bbcee2d638939"
}

variable "worker_name" {
  description = "Name of the Cloudflare Worker script"
  type        = string
  default     = "student-task-manager"
}

variable "kv_namespace_name" {
  description = "Title of the Cloudflare Workers KV Namespace"
  type        = string
  default     = "student_tasks"
}

variable "environment" {
  description = "Deployment environment (e.g., dev, test, production)"
  type        = string
  default     = "production"
}

variable "workers_subdomain" {
  description = "Cloudflare workers.dev account subdomain"
  type        = string
  default     = "rudraprakashlabhasetwar"
}
