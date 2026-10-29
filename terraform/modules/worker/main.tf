resource "cloudflare_workers_script" "this" {
  account_id = var.account_id
  name       = var.worker_name
  content    = var.content
  module     = true

  kv_namespace_binding {
    name         = var.kv_binding_name
    namespace_id = var.kv_namespace_id
  }

  plain_text_binding {
    name = "ENVIRONMENT"
    text = var.environment
  }
}
