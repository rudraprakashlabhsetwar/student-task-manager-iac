output "worker_name" {
  description = "Name of the provisioned Cloudflare Worker"
  value       = cloudflare_workers_script.task_manager.name
}

output "kv_namespace_id" {
  description = "Unique ID of the provisioned Cloudflare Workers KV Namespace"
  value       = cloudflare_workers_kv_namespace.student_tasks.id
}

output "kv_namespace_title" {
  description = "Title of the Cloudflare Workers KV Namespace"
  value       = cloudflare_workers_kv_namespace.student_tasks.title
}

output "environment" {
  description = "Target deployment environment"
  value       = var.environment
}

output "application_url" {
  description = "Live URL of the deployed Student Task Management Application"
  value       = var.workers_subdomain != "" ? "https://${cloudflare_workers_script.task_manager.name}.${var.workers_subdomain}.workers.dev" : "https://${cloudflare_workers_script.task_manager.name}.workers.dev"
}
