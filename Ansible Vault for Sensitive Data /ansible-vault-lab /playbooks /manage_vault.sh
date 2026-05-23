#!/bin/bash

# Vault management script
VAULT_PASSWORD_FILE=".vault_password"

case "$1" in
    "encrypt")
        if [ -z "$2" ]; then
            echo "Usage: $0 encrypt <file>"
            exit 1
        fi
        ansible-vault encrypt "$2" --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;
    "decrypt")
        if [ -z "$2" ]; then
            echo "Usage: $0 decrypt <file>"
            exit 1
        fi
        ansible-vault decrypt "$2" --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;
    "view")
        if [ -z "$2" ]; then
            echo "Usage: $0 view <file>"
            exit 1
        fi
        ansible-vault view "$2" --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;
    "edit")
        if [ -z "$2" ]; then
            echo "Usage: $0 edit <file>"
            exit 1
        fi
        ansible-vault edit "$2" --vault-password-file "$VAULT_PASSWORD_FILE"
        ;;
    "status")
        echo "=== Vault Files Status ==="
        find . -name "*.yml" -type f | while read file; do
            if head -1 "$file" 2>/dev/null | grep -q "ANSIBLE_VAULT"; then
                echo "✓ $file (encrypted)"
            else
                echo "○ $file (plain text)"
            fi
        done
        ;;
    *)
        echo "Usage: $0 {encrypt|decrypt|view|edit|status} [file]"
        echo "Commands:"
        echo "  encrypt <file>  - Encrypt a file"
        echo "  decrypt <file>  - Decrypt a file"
        echo "  view <file>     - View encrypted file content"
        echo "  edit <file>     - Edit encrypted file"
        echo "  status          - Show encryption status of all YAML files"
        exit 1
        ;;
esac
EOF

chmod +x manage_vault.sh

# Test the script./manage_vault.sh status
