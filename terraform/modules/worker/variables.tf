variable "account_id" {
  description = "Cloudflare Account ID"
  type        = string
}

variable "worker_name" {
  description = "Name of the worker script"
  type        = string
}

variable "content" {
  description = "JavaScript worker code content"
  type        = string
}

variable "kv_binding_name" {
  description = "Variable name bound to KV inside the Worker"
  type        = string
  default     = "TASKS_KV"
}

variable "kv_namespace_id" {
  description = "The ID of the KV namespace to bind"
  type        = string
}

variable "environment" {
  description = "Environment identifier"
  type        = string
  default     = "production"
}
