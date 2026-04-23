# Semaphore UI Stack

Ansible Semaphore UI deployment with MySQL, remote runner, and HashiCorp Vault integration.

## Prerequisites

- Docker and Docker Compose
- Access to HashiCorp Vault with AppRole authentication
- TLS certificates for Semaphore UI
- Internal CA certificates (if using private PKI)

## Configuration

### 1. Environment File

Create a `.env` file with the following variables:

```bash
# MySQL
MYSQL_PASSWORD=<secure-password>

# Semaphore database password (must match MYSQL_PASSWORD)
SEMAPHORE_DB_PASS=<secure-password>

# Semaphore admin password
SEMAPHORE_ADMIN_PASSWORD=<secure-password>

# Runner registration token (generate from Semaphore UI)
SEMAPHORE_RUNNER_TOKEN=<runner-token>
```

### 2. Vault Secrets

Create the secrets directory and add Vault AppRole credentials:

```bash
mkdir -p secrets
echo "your-role-id" > secrets/role_id
echo "your-secret-id" > secrets/secret_id
chmod 600 secrets/*
```

### 3. Vault Agent Configuration

Create `vault-agent.hcl` with your Vault configuration:

```hcl
auto_auth {
  method "approle" {
    config = {
      role_id_file_path   = "/run/secrets/vault_role_id"
      secret_id_file_path = "/run/secrets/vault_secret_id"
    }
  }

  sink "file" {
    config = {
      path = "/vault/token/vault-token"
    }
  }
}

vault {
  address = "https://vault.company.com"
}
```

### 4. TLS Certificates

Ensure TLS certificates exist at:
- `/etc/ssl/localcerts/semaphore.company.crt`
- `/etc/ssl/localcerts/semaphore.company.key`

## Deployment

```bash
docker compose up -d
```

Check service health:

```bash
docker compose ps
docker compose logs -f
```

## Architecture

```
                    +------------------+
                    |   External:443   |
                    +--------+---------+
                             |
              +--------------v--------------+
              |          semaphore          |
              |        (port 3000)          |
              +---+--------------------+----+
                  |                    |
    +-------------v-------+    +-------v--------------+
    |   semaphore_mysql   |    |   semaphore_runner   |
    +-------------+-------+    +-------+--------------+
                  |                    |
          +-------v-------+    +-------v-------+
          |     mysql     |    |    runner     |
          +---------------+    +-------+-------+
                                       |
                               +-------v-------+
                               |  vault-agent  |
                               +---------------+
```

## Networks

| Network | Purpose |
|---------|---------|
| `semaphore_mysql` | Database connectivity (semaphore <-> mysql) |
| `semaphore_runner` | Runner communication (semaphore <-> runner <-> vault-agent) |

## Volumes

| Volume | Purpose |
|--------|---------|
| `semaphore_data` | Semaphore application data |
| `semaphore_config` | Semaphore configuration |
| `mysql` | MySQL database files |
| `runner_data` | Runner state and keys |
| `vault_token` | Shared Vault token (vault-agent writes, semaphore reads) |

## Accessing the UI

After deployment, access Semaphore at:

```
https://semaphore.company.com
```

Default admin credentials are configured via environment variables:
- Username: `admin`
- Email: `admin@company.com`
- Password: Value of `SEMAPHORE_ADMIN_PASSWORD` from `.env`

## Registering the Runner

1. Log into Semaphore UI as admin
2. Navigate to **Settings > Runners**
3. Click **New Runner** and copy the registration token
4. Add the token to `.env` as `SEMAPHORE_RUNNER_TOKEN`
5. Restart the runner: `docker compose restart runner`
