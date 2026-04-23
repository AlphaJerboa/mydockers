vault {
  address = "https://vault.company.com"
  tls_config {
    ca_cert = "/usr/local/share/ca-certificates/ca.company.com.crt"
  }
}

auto_auth {
  method "approle" {
    config = {
      role_id_file_path   = "/run/secrets/vault_role_id"
      secret_id_file_path = "/run/secrets/vault_secret_id"
      # Docker secrets are read-only, so this must stay false
      remove_secret_id_file_after_reading = false
    }
  }

  # Write the renewed token to a file that Semaphore will read
  sink "file" {
    config = {
      path = "/vault/token/token"
      mode = 0640
    }
  }
}

# Optional: cache tokens locally to reduce Vault load
#cache {
#  use_auto_auth_token = true
#}

# Vault Agent API listener (optional, for debugging)
# listener "tcp" {
#   address     = "127.0.0.1:8007"
#   tls_disable = true
# }
