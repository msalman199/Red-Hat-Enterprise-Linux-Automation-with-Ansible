# Apache Web Server Role

This Ansible role installs and configures Apache HTTP Server on RHEL/CentOS systems.

## Requirements

- Ansible 2.9 or higher
- Target systems running RHEL/CentOS 7, 8, or 9

## Role Variables

### Default Variables (defaults/main.yml)
- `apache_package_name`: Package name for Apache (default: httpd)
- `apache_service_name`: Service name for Apache (default: httpd)
- `document_root`: Web document root (default: /var/www/html)
- `welcome_message`: Welcome message for index page
- `company_name`: Company name displayed on web page

### Role Variables (vars/main.yml)
- `apache_port`: Port number for Apache (default: 80)
- `max_connections`: Maximum connections (default: 100)
- `timeout`: Connection timeout (default: 300)

## Dependencies

None

## Example Playbook

```yaml
- hosts: web_servers
  roles:
    - apache-webserver
