# 🔐 Ansible Vault for Sensitive Data

> A complete hands-on lab for securing sensitive data using Ansible Vault in automation workflows.

---

# 📚 Objectives

By the end of this lab, students will be able to:

- Understand the importance of securing sensitive data in Ansible automation
- Create and manage encrypted files using Ansible Vault
- Encrypt passwords, API keys, and other sensitive information
- Integrate Ansible Vault into playbooks for secure task execution
- Use different methods to provide vault passwords during playbook execution
- Edit and view encrypted vault files
- Implement best practices for managing sensitive data in Ansible projects

---

# 🛠️ Prerequisites

Before starting this lab, students should have:

- Basic understanding of Linux command line operations
- Familiarity with Ansible fundamentals (playbooks, tasks, variables)
- Knowledge of YAML syntax
- Understanding of file permissions and security concepts
- Completion of previous Ansible labs or equivalent experience

---

# ☁️ Lab Environment

Al Nafi provides pre-configured Linux-based cloud machines for this lab.

### Environment Includes

- CentOS/RHEL 8 or Ubuntu 20.04 LTS
- Ansible 4.0+
- Nano/Vim text editors
- Sample files and directories

---

# 📂 Project Structure

```bash
ansible-vault-lab/
├── inventory/
├── playbooks/
├── templates/
├── vars/
├── group_vars/
│   ├── development/
│   └── production/
├── host_vars/
├── manage_vault.sh
└── .vault_password
```

---

# 🚀 Task 1: Understanding Ansible Vault Basics

## 🔹 Subtask 1.1: Verify Installation & Create Lab Directory

```bash
# 🔧 Check Ansible version
ansible --version

# 📁 Create project directory
mkdir -p ~/ansible-vault-lab
cd ~/ansible-vault-lab

# 📂 Create required folders
mkdir -p {playbooks,vars,inventory}
```

---

## 🔹 Subtask 1.2: Create Sample Sensitive Data

### 📄 Create Database Secrets File

```bash
cat > vars/database_secrets.yml << 'EOF'
---
database_password: "MySecretPassword123!"
database_username: "admin"
database_host: "db.example.com"
database_port: 5432
api_key: "sk-1234567890abcdef"
ssl_certificate_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...
  -----END PRIVATE KEY-----
EOF
```

### 📄 Create User Secrets File

```bash
cat > vars/user_secrets.yml << 'EOF'
---
admin_password: "AdminPass2023!"
service_account_password: "ServiceAccount456"
ldap_bind_password: "LdapSecret789"
encryption_key: "MyEncryptionKey2023"
EOF
```

---

## 🔹 Subtask 1.3: View Unencrypted Files

```bash
# 👀 View database secrets
echo "=== Database Secrets (UNENCRYPTED) ==="
cat vars/database_secrets.yml

# 👀 View user secrets
echo -e "\n=== User Secrets (UNENCRYPTED) ==="
cat vars/user_secrets.yml
```

---

# 🔐 Task 2: Encrypting Files with Ansible Vault

## 🔹 Subtask 2.1: Encrypt Vault Files

```bash
# 🔒 Encrypt database secrets
ansible-vault encrypt vars/database_secrets.yml

# 🔒 Encrypt user secrets
ansible-vault encrypt vars/user_secrets.yml
```

### ✅ Vault Password

```text
VaultPassword123
```

---

## 🔹 Subtask 2.2: Verify Encryption

```bash
# 👀 View encrypted database secrets
echo "=== Encrypted Database Secrets ==="
cat vars/database_secrets.yml

# 👀 View encrypted user secrets
echo -e "\n=== Encrypted User Secrets ==="
cat vars/user_secrets.yml
```

### 🔐 Example Output

```yaml
$ANSIBLE_VAULT;1.1;AES256
663864396537653861613038316639666334646137653861356637313032656562
3438373434353661643266323464663936346435323833310a6636353731396532
...
```

---

## 🔹 Subtask 2.3: Create Encrypted Files Directly

```bash
# 🆕 Create encrypted API secrets file
ansible-vault create vars/api_secrets.yml
```

### 📄 Add Content

```yaml
stripe_api_key: "sk_test_1234567890abcdef"
paypal_client_secret: "PayPalSecret123"
aws_secret_access_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
github_token: "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
```

---

# 🧩 Task 3: Working with Encrypted Vault Files

## 🔹 Subtask 3.1: View Encrypted Files

```bash
# 👁️ View database secrets
ansible-vault view vars/database_secrets.yml

# 👁️ View user secrets
ansible-vault view vars/user_secrets.yml

# 👁️ View API secrets
ansible-vault view vars/api_secrets.yml
```

---

## 🔹 Subtask 3.2: Edit Encrypted Files

```bash
# ✏️ Edit encrypted file
ansible-vault edit vars/database_secrets.yml
```

### ➕ Add Variable

```yaml
database_backup_password: "BackupSecret456"
```

---

## 🔹 Subtask 3.3: Change Vault Password

```bash
# 🔄 Rekey encrypted file
ansible-vault rekey vars/database_secrets.yml
```

### 🔑 New Password

```text
NewVaultPassword456
```

---

# ⚙️ Task 4: Integrating Vault into Playbooks

## 🔹 Subtask 4.1: Create Inventory File

```bash
cat > inventory/hosts << 'EOF'
[webservers]
localhost ansible_connection=local

[databases]
localhost ansible_connection=local
EOF
```

---

## 🔹 Subtask 4.2: Create Secure Deployment Playbook

```bash
cat > playbooks/secure_deployment.yml << 'EOF'
---
- name: Secure Application Deployment
  hosts: webservers
  gather_facts: yes

  vars_files:
    - ../vars/database_secrets.yml
    - ../vars/user_secrets.yml
    - ../vars/api_secrets.yml

  tasks:

    - name: 📢 Display server info
      debug:
        msg: "Deploying to {{ ansible_hostname }}"

    - name: 📁 Create configuration directory
      file:
        path: /tmp/app-config
        state: directory
        mode: '0750'
      become: yes

    - name: 📝 Generate database configuration
      template:
        src: ../templates/database.conf.j2
        dest: /tmp/app-config/database.conf
        mode: '0600'
      become: yes

    - name: 📝 Generate API configuration
      template:
        src: ../templates/api.conf.j2
        dest: /tmp/app-config/api.conf
        mode: '0600'
      become: yes

    - name: 👤 Create service user
      user:
        name: appservice
        password: "{{ service_account_password | password_hash('sha512') }}"
        shell: /bin/bash
        create_home: yes
      become: yes

    - name: ✅ Display deployment status
      debug:
        msg: "Configuration completed for {{ database_username }}"
EOF
```

---

## 🔹 Subtask 4.3: Create Template Files

### 📁 Create Templates Directory

```bash
mkdir -p templates
```

### 📝 Database Template

```bash
cat > templates/database.conf.j2 << 'EOF'
# Database Configuration

[database]
host = {{ database_host }}
port = {{ database_port }}
username = {{ database_username }}
password = {{ database_password }}

[backup]
backup_password = {{ database_backup_password | default('DefaultBackup123') }}
EOF
```

### 📝 API Template

```bash
cat > templates/api.conf.j2 << 'EOF'
# API Configuration

[stripe]
api_key = {{ stripe_api_key }}

[paypal]
client_secret = {{ paypal_client_secret }}

[aws]
secret_access_key = {{ aws_secret_access_key }}

[github]
token = {{ github_token }}

[encryption]
key = {{ encryption_key }}
EOF
```

---

## 🔹 Subtask 4.4: Run Playbook with Vault Password

```bash
# 🔄 Rekey file back to original password
ansible-vault rekey vars/database_secrets.yml

# ▶️ Run playbook
ansible-playbook -i inventory/hosts playbooks/secure_deployment.yml --ask-vault-pass
```

---

## 🔹 Subtask 4.5: Use Vault Password File

```bash
# 🔑 Create vault password file
echo "VaultPassword123" > .vault_password

# 🔒 Secure permissions
chmod 600 .vault_password

# ▶️ Run playbook using password file
ansible-playbook -i inventory/hosts playbooks/secure_deployment.yml \
--vault-password-file .vault_password
```

---

## 🔹 Subtask 4.6: Verify Deployment

```bash
# 📄 View database config
sudo cat /tmp/app-config/database.conf

# 📄 View API config
sudo cat /tmp/app-config/api.conf

# 👤 Check service user
id appservice

# 🔒 Verify permissions
ls -la /tmp/app-config/
```

---

# 🧠 Task 5: Advanced Vault Operations

## 🔹 Subtask 5.1: Decrypt Files Permanently

```bash
# 💾 Backup file
cp vars/user_secrets.yml vars/user_secrets.yml.backup

# 🔓 Decrypt file
ansible-vault decrypt vars/user_secrets.yml

# 👀 View decrypted content
cat vars/user_secrets.yml

# 🔒 Re-encrypt file
ansible-vault encrypt vars/user_secrets.yml
```

---

## 🔹 Subtask 5.2: Encrypt Specific Variables

```bash
# 🔐 Encrypt single variable
ansible-vault encrypt_string 'SuperSecretPassword123!' \
--name 'mysql_root_password'
```

---

## 🔹 Subtask 5.3: Create Mixed Variable File

```bash
cat > vars/mixed_secrets.yml << 'EOF'
---
application_name: "MyWebApp"
version: "2.1.0"
debug_mode: false

database_root_password: "PLACEHOLDER"
EOF
```

### 🔒 Encrypt Placeholder Password

```bash
encrypted_password=$(ansible-vault encrypt_string 'RootPassword789!' \
--name 'database_root_password' \
--vault-password-file .vault_password)

sed -i 's/database_root_password: "PLACEHOLDER"/'"$encrypted_password"'/' vars/mixed_secrets.yml
```

---

## 🔹 Subtask 5.4: Multiple Vault IDs

### 🧪 Development Secrets

```bash
ansible-vault create --vault-id dev@prompt vars/dev_secrets.yml
```

```yaml
dev_database_password: "DevPassword123"
dev_api_key: "dev-api-key-123"
```

### 🏭 Production Secrets

```bash
ansible-vault create --vault-id prod@prompt vars/prod_secrets.yml
```

```yaml
prod_database_password: "ProdPassword456"
prod_api_key: "prod-api-key-456"
```

---

# 🏗️ Task 6: Best Practices and Security

## 🔹 Subtask 6.1: Create Secure Structure

```bash
mkdir -p {group_vars,host_vars}
mkdir -p group_vars/{development,production}
```

### 🧪 Development Variables

```bash
cat > group_vars/development/main.yml << 'EOF'
---
environment: development
database_host: dev-db.example.com
api_endpoint: https://api-dev.example.com
debug_enabled: true
EOF
```

### 🔒 Development Vault

```bash
ansible-vault create group_vars/development/vault.yml \
--vault-password-file .vault_password
```

```yaml
vault_database_password: "DevDBPassword123"
vault_api_secret: "dev-secret-key-789"
vault_ssl_key: "dev-ssl-private-key"
```

---

## 🔹 Subtask 6.2: Production Configuration

```bash
cat > group_vars/production/main.yml << 'EOF'
---
environment: production
database_host: prod-db.example.com
api_endpoint: https://api.example.com
debug_enabled: false
EOF
```

### 🔒 Production Vault

```bash
ansible-vault create group_vars/production/vault.yml \
--vault-password-file .vault_password
```

```yaml
vault_database_password: "ProdDBPassword456"
vault_api_secret: "prod-secret-key-abc"
vault_ssl_key: "prod-ssl-private-key"
```

---

## 🔹 Subtask 6.3: Environment Deployment Playbook

```bash
cat > playbooks/environment_deployment.yml << 'EOF'
---
- name: Environment-Specific Deployment
  hosts: "{{ target_environment | default('development') }}"
  gather_facts: yes

  tasks:

    - name: 🌍 Display environment info
      debug:
        msg: |
          Deploying to: {{ environment }}
          Database Host: {{ database_host }}
          API Endpoint: {{ api_endpoint }}

    - name: 📝 Create environment config
      template:
        src: ../templates/app_config.j2
        dest: "/tmp/{{ environment }}_config.conf"
        mode: '0600'
      become: yes

    - name: ✅ Verify sensitive variables
      debug:
        msg: "Database password loaded successfully"
EOF
```

---

## 🔹 Subtask 6.4: Application Template

```bash
cat > templates/app_config.j2 << 'EOF'
# {{ environment | upper }} Environment Configuration

[application]
environment = {{ environment }}

[database]
host = {{ database_host }}
password = {{ vault_database_password }}

[api]
endpoint = {{ api_endpoint }}
secret = {{ vault_api_secret }}

[ssl]
private_key = {{ vault_ssl_key }}
EOF
```

---

## 🔹 Subtask 6.5: Deploy Environments

### 📄 Update Inventory

```bash
cat > inventory/hosts << 'EOF'
[development]
localhost ansible_connection=local

[production]
localhost ansible_connection=local

[webservers:children]
development
production
EOF
```

### 🚀 Deploy Development

```bash
ansible-playbook -i inventory/hosts \
playbooks/environment_deployment.yml \
--limit development \
--vault-password-file .vault_password
```

### 🚀 Deploy Production

```bash
ansible-playbook -i inventory/hosts \
playbooks/environment_deployment.yml \
--limit production \
--vault-password-file .vault_password
```

---

## 🔹 Subtask 6.6: Verify Environment Configurations

```bash
# 👀 Development config
sudo cat /tmp/development_config.conf

# 👀 Production config
sudo cat /tmp/production_config.conf
```

---

# 🐞 Task 7: Troubleshooting & Common Issues

## 🔹 Subtask 7.1: Handle Vault Errors

```bash
cat > playbooks/test_vault_errors.yml << 'EOF'
---
- name: Test Vault Error Handling
  hosts: localhost

  vars_files:
    - ../vars/database_secrets.yml

  tasks:
    - name: ❌ Test vault access
      debug:
        msg: "Database user: {{ database_username }}"
EOF
```

### ❌ Run Without Password

```bash
ansible-playbook -i inventory/hosts \
playbooks/test_vault_errors.yml
```

### ✅ Run With Password

```bash
ansible-playbook -i inventory/hosts \
playbooks/test_vault_errors.yml \
--vault-password-file .vault_password
```

---

## 🔹 Subtask 7.2: Validate Vault Files

```bash
echo "=== Vault File Status ==="

for file in vars/*.yml group_vars/*/vault.yml; do
    if [ -f "$file" ]; then
        echo "File: $file"

        if head -1 "$file" | grep -q "ANSIBLE_VAULT"; then
            echo "  Status: Encrypted ✓"
        else
            echo "  Status: Not encrypted ⚠️"
        fi
    fi
done
```

---

## 🔹 Subtask 7.3: Vault Management Script

```bash
cat > manage_vault.sh << 'EOF'
#!/bin/bash

VAULT_PASSWORD_FILE=".vault_password"

case "$1" in

    "encrypt")
        ansible-vault encrypt "$2" \
        --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;

    "decrypt")
        ansible-vault decrypt "$2" \
        --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;

    "view")
        ansible-vault view "$2" \
        --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;

    "edit")
        ansible-vault edit "$2" \
        --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;

    "status")
        echo "=== Vault Files Status ==="

        find . -name "*.yml" -type f | while read file; do
            if head -1 "$file" | grep -q "ANSIBLE_VAULT"; then
                echo "✓ $file (encrypted)"
            else
                echo "○ $file (plain text)"
            fi
        done
        ;;

    *)
        echo "Usage: $0 {encrypt|decrypt|view|edit|status}"
        ;;
esac
EOF
```

### 🔧 Make Script Executable

```bash
chmod +x manage_vault.sh
```

### ▶️ Test Script

```bash
./manage_vault.sh status
```

---

# 🎯 Conclusion

Congratulations! You have successfully completed the **Ansible Vault for Sensitive Data** lab.

## ✅ Skills Learned

- Securing sensitive data using Ansible Vault
- Encrypting files and variables
- Managing vault passwords securely
- Integrating vault secrets into playbooks
- Environment-specific secret management
- Implementing automation security best practices
- Troubleshooting vault-related issues

---

# 🌟 Why Ansible Vault Matters

### 🔐 Production Security
Protects passwords, API keys, SSL certificates, and confidential data.

### 📋 Compliance
Helps organizations meet security and compliance standards like:

- SOX
- HIPAA
- PCI-DSS

### 👥 Team Collaboration
Allows teams to safely share automation code without exposing secrets.

### ⚡ Operational Excellence
Build secure, scalable, and enterprise-ready automation workflows.

---

# 📈 Next Steps

Explore more advanced topics:

- Multiple Vault IDs
- Secret rotation strategies
- HashiCorp Vault integration
- Ansible Tower / AWX
- CI/CD secret management



# 👨‍💻 Author

## Hafiz Muhammad Salman
### Cloud & DevOps Engineer

---

# ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork this project
- 📢 Share with others

---

# 📜 License

This project is for educational and learning purposes.
