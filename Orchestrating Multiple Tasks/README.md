# 🚀 Orchestrating Multiple Tasks with Ansible

## 📘 Lab Overview

This lab demonstrates how to orchestrate multiple systems and services using **Ansible**.  
You will automate deployment of a complete multi-tier infrastructure stack including:

- 🗄️ Database Server
- 🌐 Web Application Servers
- ⚖️ Load Balancer
- 📊 Monitoring System

---

# 🎯 Objectives

By the end of this lab, students will be able to:

✅ Create and organize multiple Ansible playbooks  
✅ Implement task dependencies and execution order  
✅ Use includes and orchestration workflows  
✅ Handle rollback and failure scenarios  
✅ Share variables between hosts and playbooks  
✅ Validate deployments automatically  

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

- ✅ Basic Ansible knowledge
- ✅ Familiarity with YAML syntax
- ✅ Linux command-line experience
- ✅ SSH key authentication setup
- ✅ Basic system administration skills

---

# 🖥️ Lab Environment Setup

## ☁️ Environment Includes

| Component | Description |
|---|---|
| 🧠 Control Node | CentOS/RHEL 8 with Ansible |
| 🌐 Web Servers | 2 Managed Nodes |
| 🗄️ Database Server | MariaDB Server |
| ⚖️ Load Balancer | HAProxy Server |
| 🔐 Authentication | Passwordless SSH |
| 📁 Templates | Preconfigured sample files |

---

# 📁 Step 1 — Create Project Structure

## 🛠️ Create Main Directory

```bash
mkdir -p ~/ansible-orchestration
cd ~/ansible-orchestration
```

## 🛠️ Create Required Folders

```bash
mkdir -p {playbooks,roles,group_vars,host_vars,inventory,templates}
```

---

# 📂 Final Project Structure

```text
ansible-orchestration/
│
├── inventory/
│   └── hosts
│
├── group_vars/
│   └── all.yml
│
├── playbooks/
│   ├── site.yml
│   ├── database.yml
│   ├── webservers.yml
│   ├── loadbalancer.yml
│   ├── monitoring.yml
│   ├── dependency_check.yml
│   └── rollback.yml
│
├── templates/
│   ├── app_config.php.j2
│   ├── webapp.conf.j2
│   └── haproxy.cfg.j2
│
└── roles/
```

---

# ⚙️ Step 2 — Create Master Orchestration Playbook

## 📄 File: `playbooks/site.yml`

```yaml
---
- name: "Complete Application Stack Deployment"
  hosts: localhost
  gather_facts: false

  vars:
    deployment_timestamp: "{{ ansible_date_time.epoch }}"
    deployment_id: "deploy-{{ deployment_timestamp }}"

  tasks:

    - name: "Display deployment information"
      debug:
        msg: |
          Starting deployment
          Deployment ID: {{ deployment_id }}

    - name: "Deploy Database"
      import_playbook: database.yml
      tags:
        - database

    - name: "Deploy Web Servers"
      import_playbook: webservers.yml
      tags:
        - webservers

    - name: "Deploy Load Balancer"
      import_playbook: loadbalancer.yml
      tags:
        - loadbalancer

    - name: "Setup Monitoring"
      import_playbook: monitoring.yml
      tags:
        - monitoring
```

---

# 🗄️ Step 3 — Create Database Playbook

## 📄 File: `playbooks/database.yml`

```yaml
---
- name: "Deploy Database Server"
  hosts: database_servers
  become: yes

  vars:
    db_name: "webapp_db"
    db_user: "webapp_user"
    db_password: "SecurePassword123!"

  tasks:

    - name: "Install MariaDB Packages"
      yum:
        name:
          - mariadb-server
          - mariadb
          - python3-PyMySQL
        state: present

    - name: "Start MariaDB"
      systemd:
        name: mariadb
        state: started
        enabled: yes

    - name: "Create Database"
      mysql_db:
        name: "{{ db_name }}"
        state: present
        login_unix_socket: /var/lib/mysql/mysql.sock

    - name: "Create Database User"
      mysql_user:
        name: "{{ db_user }}"
        password: "{{ db_password }}"
        priv: "{{ db_name }}.*:ALL"
        host: "%"
        state: present
        login_unix_socket: /var/lib/mysql/mysql.sock

    - name: "Allow MySQL Firewall"
      firewalld:
        service: mysql
        permanent: yes
        state: enabled
        immediate: yes
```

---

# 🌐 Step 4 — Create Web Server Playbook

## 📄 File: `playbooks/webservers.yml`

```yaml
---
- name: "Deploy Web Servers"
  hosts: web_servers
  become: yes

  vars:
    app_name: "webapp"

  tasks:

    - name: "Install Apache and PHP"
      yum:
        name:
          - httpd
          - php
          - php-mysql
        state: present

    - name: "Create Web Directory"
      file:
        path: "/var/www/html/{{ app_name }}"
        state: directory
        owner: apache
        group: apache
        mode: '0755'

    - name: "Deploy Application"
      copy:
        content: |
          <h1>Welcome to {{ inventory_hostname }}</h1>
        dest: "/var/www/html/{{ app_name }}/index.html"

    - name: "Start Apache"
      systemd:
        name: httpd
        state: started
        enabled: yes

    - name: "Allow HTTP Firewall"
      firewalld:
        service: http
        permanent: yes
        state: enabled
        immediate: yes
```

---

# ⚖️ Step 5 — Create Load Balancer Playbook

## 📄 File: `playbooks/loadbalancer.yml`

```yaml
---
- name: "Deploy Load Balancer"
  hosts: load_balancer
  become: yes

  tasks:

    - name: "Install HAProxy"
      yum:
        name: haproxy
        state: present

    - name: "Deploy HAProxy Config"
      template:
        src: haproxy.cfg.j2
        dest: /etc/haproxy/haproxy.cfg

    - name: "Start HAProxy"
      systemd:
        name: haproxy
        state: started
        enabled: yes
```

---

# 📊 Step 6 — Create Monitoring Playbook

## 📄 File: `playbooks/monitoring.yml`

```yaml
---
- name: "Setup Monitoring"
  hosts: all
  become: yes

  tasks:

    - name: "Install Monitoring Tools"
      yum:
        name:
          - htop
          - iotop
        state: present

    - name: "Create Monitoring Script"
      copy:
        content: |
          #!/bin/bash
          uptime
          free -h
          df -h
        dest: /usr/local/bin/system-status.sh
        mode: '0755'
```

---

# 🔍 Step 7 — Dependency Validation

## 📄 File: `playbooks/dependency_check.yml`

```yaml
---
- name: "Validate Dependencies"
  hosts: all
  gather_facts: yes

  tasks:

    - name: "Check Connectivity"
      ping:

    - name: "Check Disk Space"
      assert:
        that:
          - ansible_mounts | selectattr('mount', 'equalto', '/') | map(attribute='size_available') | first > 1073741824
```

---

# 🧩 Step 8 — Create Templates

---

## 📄 File: `templates/app_config.php.j2`

```php
<?php
define('APP_NAME', '{{ app_name }}');
?>
```

---

## 📄 File: `templates/webapp.conf.j2`

```apache
<VirtualHost *:80>

    DocumentRoot /var/www/html/{{ app_name }}

    <Directory /var/www/html/{{ app_name }}>
        AllowOverride All
        Require all granted
    </Directory>

</VirtualHost>
```

---

## 📄 File: `templates/haproxy.cfg.j2`

```cfg
frontend webapp_frontend
    bind *:80
    default_backend webapp_servers

backend webapp_servers
    balance roundrobin

{% for server in groups['web_servers'] %}
    server {{ server }} {{ hostvars[server]['ansible_default_ipv4']['address'] }}:80 check
{% endfor %}
```

---

# 🖧 Step 9 — Create Inventory File

## 📄 File: `inventory/hosts`

```ini
[database_servers]
db1 ansible_host=10.0.1.10

[web_servers]
web1 ansible_host=10.0.1.11
web2 ansible_host=10.0.1.12

[load_balancer]
lb1 ansible_host=10.0.1.13

[all:vars]
ansible_user=centos
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

---

# 🌍 Step 10 — Create Global Variables

## 📄 File: `group_vars/all.yml`

```yaml
---
deployment_environment: production

app_name: webapp

db_name: webapp_db
db_user: webapp_user

vault_db_password: SecurePassword123!
```

---

# ▶️ Step 11 — Execute Deployment

## 🔎 Run Dependency Check

```bash
ansible-playbook -i inventory/hosts playbooks/dependency_check.yml
```

---

## 🚀 Run Complete Deployment

```bash
ansible-playbook -i inventory/hosts playbooks/site.yml
```

---

## 🎯 Run Specific Deployment Tags

### 🗄️ Database

```bash
ansible-playbook -i inventory/hosts playbooks/site.yml --tags database
```

### 🌐 Web Servers

```bash
ansible-playbook -i inventory/hosts playbooks/site.yml --tags webservers
```

### ⚖️ Load Balancer

```bash
ansible-playbook -i inventory/hosts playbooks/site.yml --tags loadbalancer
```

---

# 🔄 Step 12 — Rollback Playbook

## 📄 File: `playbooks/rollback.yml`

```yaml
---
- name: "Rollback Stack"
  hosts: all
  become: yes

  tasks:

    - name: "Stop Services"
      systemd:
        name: "{{ item }}"
        state: stopped
      loop:
        - httpd
        - mariadb
        - haproxy

    - name: "Remove Application Files"
      file:
        path: "/var/www/html/webapp"
        state: absent
```

---

# 🛠️ Troubleshooting Commands

---

## 🔎 Check MariaDB Status

```bash
ansible database_servers -i inventory/hosts -m systemd -a "name=mariadb" --become
```

---

## 🔎 Check Apache Status

```bash
ansible web_servers -i inventory/hosts -m shell -a "systemctl status httpd"
```

---

## 🔎 Check HAProxy Status

```bash
ansible load_balancer -i inventory/hosts -m shell -a "systemctl status haproxy"
```

---

## 🔎 Check Firewall Rules

```bash
ansible all -i inventory/hosts -m shell -a "firewall-cmd --list-all"
```

---

# 🧪 Debugging Commands

## 📌 Verbose Mode

```bash
ansible-playbook -i inventory/hosts playbooks/site.yml -vvv
```

---

## 📌 Gather Facts

```bash
ansible all -i inventory/hosts -m setup
```

---

## 📌 Test Connectivity

```bash
ansible all -i inventory/hosts -m ping
```

---

# ✅ Conclusion

In this lab, you successfully learned how to orchestrate multiple infrastructure components using Ansible.

## 🏆 Skills Developed

- ✅ Multi-playbook orchestration
- ✅ Dependency management
- ✅ Infrastructure automation
- ✅ Template management
- ✅ Monitoring setup
- ✅ Rollback handling
- ✅ Deployment validation

---

# 🌟 Real-World Use Cases

These orchestration skills are essential for:

- 🚀 DevOps Automation
- ☁️ Cloud Infrastructure Management
- 🏢 Enterprise Deployments
- 🔄 CI/CD Pipelines
- 📦 Infrastructure as Code (IaC)

---

# 📚 Next Steps

- Learn Ansible Roles deeply
- Explore AWX / Ansible Tower
- Study Ansible Vault
- Automate Cloud Deployments
- Learn Dynamic Inventories

---

# 👨‍💻 Author

## Hafiz Muhammad Salman  
### Cloud & DevOps Engineer

---
