resource "cloudflare_workers_kv_namespace" "student_tasks" {
  account_id = var.account_id
  title      = var.kv_namespace_name
}

resource "cloudflare_workers_script" "task_manager" {
  account_id = var.account_id
  name       = var.worker_name
  content    = file("${path.module}/../application/worker.js")
  module     = true

  kv_namespace_binding {
    name         = "TASKS_KV"
    namespace_id = cloudflare_workers_kv_namespace.student_tasks.id
  }

  plain_text_binding {
    name = "ENVIRONMENT"
    text = var.environment
  }
}
