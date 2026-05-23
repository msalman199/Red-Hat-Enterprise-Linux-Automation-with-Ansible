# Optimizing Playbooks and Performance with Ansible

## 📌 Objectives

By the end of this lab, students will be able to:

- Understand playbook optimization principles and best practices for Ansible automation
- Split large playbooks into modular roles to improve maintainability and reusability
- Implement asynchronous execution and delegation to enhance task performance
- Test and measure playbook efficiency in simulated large-scale environments
- Apply performance tuning techniques to optimize Ansible playbook execution
- Troubleshoot common performance bottlenecks in Ansible automation

---

# 📋 Prerequisites

Before starting this lab, students should have:

- Basic understanding of Ansible fundamentals
- Familiarity with YAML syntax and playbook structure
- Knowledge of Linux command line operations
- Understanding SSH connectivity and remote management
- Previous Ansible lab experience
- Basic system administration knowledge

---

# ☁️ Lab Environment Setup

Al Nafi provides pre-configured Linux-based cloud machines for this lab.

## Environment Includes

- Control Node: CentOS/RHEL 8 with Ansible installed
- Managed Nodes: 3 target systems
- Pre-configured SSH keys
- Sample applications and services

---

# 🛠️ Task 1: Split Large Playbooks into Roles for Modularity

---

# 🔧 Subtask 1.1: Analyze a Monolithic Playbook

## ▶️ Step 1: Navigate to Lab Directory

```bash
cd /home/ansible/lab20
ls -la
```

## ▶️ Step 2: Examine Existing Playbook

```bash
cat large-playbook.yml
```

## 📌 Functional Areas Identified

- Web Server Configuration
- Database Setup
- Application Deployment
- Monitoring and Logging
- Security Hardening

---

# 🔧 Subtask 1.2: Create Role Structure

## ▶️ Step 1: Create Roles Directory

```bash
mkdir -p roles/{webserver,database,application,monitoring,security}/{tasks,handlers,templates,files,vars,defaults,meta}
```

## ▶️ Step 2: Verify Structure

```bash
tree roles/
```

---

# 🔧 Subtask 1.3: Extract Web Server Role

## ▶️ Step 1: Create Webserver Tasks

```bash
cat > roles/webserver/tasks/main.yml << 'EOF'
---
- name: Install web server packages
  package:
    name: "{{ webserver_packages }}"
    state: present
  notify: restart webserver

- name: Configure web server
  template:
    src: "{{ webserver_config_template }}"
    dest: "{{ webserver_config_path }}"
    backup: yes
  notify: restart webserver

- name: Start and enable web server
  service:
    name: "{{ webserver_service }}"
    state: started
    enabled: yes

- name: Configure firewall for web server
  firewalld:
    service: "{{ item }}"
    permanent: yes
    state: enabled
    immediate: yes
  loop: "{{ webserver_firewall_services }}"
  when: ansible_facts['os_family'] == "RedHat"
EOF
```

## ▶️ Step 2: Create Defaults File

```bash
cat > roles/webserver/defaults/main.yml << 'EOF'
---
webserver_packages:
  - httpd
  - mod_ssl

webserver_service: httpd
webserver_config_template: httpd.conf.j2
webserver_config_path: /etc/httpd/conf/httpd.conf

webserver_firewall_services:
  - http
  - https
EOF
```

## ▶️ Step 3: Create Handlers

```bash
cat > roles/webserver/handlers/main.yml << 'EOF'
---
- name: restart webserver
  service:
    name: "{{ webserver_service }}"
    state: restarted
EOF
```

## ▶️ Step 4: Create Configuration Template

```bash
cat > roles/webserver/templates/httpd.conf.j2 << 'EOF'
ServerRoot /etc/httpd
Listen 80
Listen 443 ssl

User apache
Group apache

ServerAdmin admin@{{ ansible_fqdn }}
ServerName {{ ansible_fqdn }}

DocumentRoot /var/www/html

<Directory "/var/www/html">
    AllowOverride None
    Require all granted
</Directory>

ErrorLog logs/error_log
CustomLog logs/access_log combined

LoadModule ssl_module modules/mod_ssl.so
Include conf.d/*.conf
EOF
```

---

# 🔧 Subtask 1.4: Extract Database Role

## ▶️ Step 1: Create Database Tasks

```bash
cat > roles/database/tasks/main.yml << 'EOF'
---
- name: Install database packages
  package:
    name: "{{ database_packages }}"
    state: present

- name: Start and enable database service
  service:
    name: "{{ database_service }}"
    state: started
    enabled: yes

- name: Configure database
  template:
    src: "{{ database_config_template }}"
    dest: "{{ database_config_path }}"
    backup: yes
  notify: restart database

- name: Create application database
  mysql_db:
    name: "{{ app_database_name }}"
    state: present
  when: database_type == "mysql"

- name: Create database user
  mysql_user:
    name: "{{ app_database_user }}"
    password: "{{ app_database_password }}"
    priv: "{{ app_database_name }}.*:ALL"
    state: present
  when: database_type == "mysql"
EOF
```

## ▶️ Step 2: Create Database Defaults

```bash
cat > roles/database/defaults/main.yml << 'EOF'
---
database_type: mysql

database_packages:
  - mariadb-server
  - mariadb
  - python3-PyMySQL

database_service: mariadb
database_config_template: my.cnf.j2
database_config_path: /etc/my.cnf.d/server.cnf

app_database_name: webapp
app_database_user: webuser
app_database_password: changeme
EOF
```

## ▶️ Step 3: Create Database Handlers

```bash
cat > roles/database/handlers/main.yml << 'EOF'
---
- name: restart database
  service:
    name: "{{ database_service }}"
    state: restarted
EOF
```

---

# 🔧 Subtask 1.5: Create Application Role

## ▶️ Step 1: Create Application Tasks

```bash
cat > roles/application/tasks/main.yml << 'EOF'
---
- name: Create application directory
  file:
    path: "{{ app_directory }}"
    state: directory
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: '0755'

- name: Deploy application files
  copy:
    src: "{{ item }}"
    dest: "{{ app_directory }}/"
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: '0644'
  loop: "{{ app_files }}"
  notify: restart webserver

- name: Configure application
  template:
    src: app-config.php.j2
    dest: "{{ app_directory }}/config.php"
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: '0640'
  notify: restart webserver
EOF
```

## ▶️ Step 2: Create Application Defaults

```bash
cat > roles/application/defaults/main.yml << 'EOF'
---
app_directory: /var/www/html
app_user: apache
app_group: apache

app_files:
  - index.php
  - style.css
EOF
```

---

# 🔧 Subtask 1.6: Create Optimized Main Playbook

## ▶️ Step 1: Create Optimized Playbook

```bash
cat > optimized-playbook.yml << 'EOF'
---
- name: Deploy Web Application Infrastructure
  hosts: webservers
  become: yes
  gather_facts: yes

  roles:
    - role: security
      tags: security

    - role: database
      tags: database

    - role: webserver
      tags: webserver

    - role: application
      tags: application

    - role: monitoring
      tags: monitoring

  post_tasks:
    - name: Verify web service is accessible
      uri:
        url: "http://{{ ansible_fqdn }}"
        method: GET
        status_code: 200
      delegate_to: localhost
      tags: verification
EOF
```

## ▶️ Step 2: Create Site Playbook

```bash
cat > site.yml << 'EOF'
---
- import_playbook: optimized-playbook.yml

- name: Post-deployment tasks
  hosts: webservers
  become: yes

  tasks:
    - name: Display deployment summary
      debug:
        msg: |
          Deployment completed successfully!
          Web server: {{ ansible_fqdn }}
          Database: {{ database_type }}
          Application directory: {{ app_directory }}
EOF
```

---

# 🚀 Task 2: Use Asynchronous Execution and Delegation

---

# 🔧 Subtask 2.1: Implement Asynchronous Execution

## ▶️ Step 1: Create Async Optimization Playbook

```bash
cat > async-optimization.yml << 'EOF'
---
- name: Demonstrate Asynchronous Task Execution
  hosts: all
  become: yes
  gather_facts: yes

  tasks:
    - name: Start long-running package updates
      yum:
        name: '*'
        state: latest
      async: 300
      poll: 0
      register: package_update_job

    - name: Perform other tasks while updates run
      debug:
        msg: "Running async operations"

    - name: Wait for package updates
      async_status:
        jid: "{{ package_update_job.ansible_job_id }}"
      register: package_result
      until: package_result.finished
      retries: 30
      delay: 10
EOF
```

---

# 🔧 Subtask 2.2: Implement Task Delegation

## ▶️ Step 1: Create Delegation Optimization Playbook

```bash
cat > delegation-optimization.yml << 'EOF'
---
- name: Demonstrate Task Delegation
  hosts: webservers
  become: yes

  tasks:
    - name: Generate SSL certificate on control node
      command: openssl version
      delegate_to: localhost

    - name: Verify connectivity
      wait_for:
        host: "{{ ansible_fqdn }}"
        port: 80
        timeout: 30
      delegate_to: localhost
EOF
```

---

# 🔧 Subtask 2.3: Optimize with Parallel Execution

## ▶️ Step 1: Create Parallel Optimization Playbook

```bash
cat > parallel-optimization.yml << 'EOF'
---
- name: Parallel Execution Optimization
  hosts: all
  become: yes
  strategy: free

  tasks:
    - name: Update system packages
      package:
        name: '*'
        state: latest
      async: 600
      poll: 0

    - name: Create directories
      file:
        path: "{{ item }}"
        state: directory
      loop:
        - /opt/app1
        - /opt/app2
        - /opt/app3
EOF
```

---

# 📊 Task 3: Test Playbook Efficiency

---

# 🔧 Subtask 3.1: Create Performance Testing Framework

## ▶️ Step 1: Create Performance Test Playbook

```bash
cat > performance-test.yml << 'EOF'
---
- name: Performance Testing Framework
  hosts: localhost
  gather_facts: no

  tasks:
    - name: Run optimized playbook benchmark
      command: ansible-playbook optimized-playbook.yml --check
EOF
```

---

# 🔧 Subtask 3.2: Create Large Inventory

## ▶️ Step 1: Create Inventory File

```bash
cat > large-inventory << 'EOF'
[webservers]
web01 ansible_host=192.168.1.10
web02 ansible_host=192.168.1.11
web03 ansible_host=192.168.1.12

[databases]
db01 ansible_host=192.168.1.20

[all:vars]
ansible_user=ansible
EOF
```

---

# 🔧 Subtask 3.3: Configure ansible.cfg

## ▶️ Step 1: Create ansible.cfg

```bash
cat > ansible.cfg << 'EOF'
[defaults]
inventory = large-inventory
forks = 20
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts_cache
fact_caching_timeout = 3600

[ssh_connection]
pipelining = True
EOF
```

---

# 🔧 Subtask 3.4: Create Benchmark Script

## ▶️ Step 1: Create Benchmark Script

```bash
cat > benchmark-playbooks.sh << 'EOF'
#!/bin/bash

echo "Starting benchmark tests..."

ansible-playbook optimized-playbook.yml --check
ansible-playbook async-optimization.yml --check

echo "Benchmark completed."
EOF
```

## ▶️ Step 2: Make Script Executable

```bash
chmod +x benchmark-playbooks.sh
```

## ▶️ Step 3: Run Benchmark Script

```bash
./benchmark-playbooks.sh
```

---

# 🔧 Subtask 3.5: Analyze Performance Results

## ▶️ Step 1: Create Performance Analysis Playbook

```bash
cat > analyze-performance.yml << 'EOF'
---
- name: Analyze Playbook Performance
  hosts: localhost

  tasks:
    - name: Display optimization recommendations
      debug:
        msg: |
          Optimization Recommendations:
          - Use modular roles
          - Implement async execution
          - Optimize fork values
          - Enable fact caching
EOF
```

## ▶️ Step 2: Run Analysis

```bash
ansible-playbook analyze-performance.yml
```

---

# 🐞 Troubleshooting Common Issues

---

# ⚠️ Issue 1: Async Tasks Not Completing

## ✅ Solution

```bash
ansible all -m async_status -a "jid=<job_id>"
```

Increase timeout values:

```yaml
async: 600
poll: 10
```

---

# ⚠️ Issue 2: Role Dependencies Not Working

## ✅ Solution

```bash
cat > roles/application/meta/main.yml << 'EOF'
dependencies:
  - role: webserver
  - role: database
EOF
```

---

# ⚠️ Issue 3: Performance Degradation with High Fork Count

## ✅ Solution

- Start with 5 × CPU cores
- Monitor CPU and memory usage
- Adjust based on infrastructure capacity

---

# ⚠️ Issue 4: Fact Gathering Taking Too Long

## ✅ Solution

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_timeout = 3600
```

Disable fact gathering when unnecessary:

```yaml
gather_facts: no
```

---

# ✅ Conclusion

In this lab, you successfully implemented advanced Ansible optimization techniques including:

- Role-based modular architecture
- Asynchronous task execution
- Task delegation
- Parallel execution strategies
- Performance benchmarking
- Large-scale inventory testing
- Optimization troubleshooting

These techniques are essential for scalable enterprise automation and efficient infrastructure management.

---

# 📁 File Structure

```bash
lab20/
├── ansible.cfg
├── large-playbook.yml
├── optimized-playbook.yml
├── site.yml
├── async-optimization.yml
├── delegation-optimization.yml
├── parallel-optimization.yml
├── performance-test.yml
├── analyze-performance.yml
├── benchmark-playbooks.sh
├── large-inventory
├── roles/
│   ├── webserver/
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   ├── defaults/main.yml
│   │   └── templates/httpd.conf.j2
│   ├── database/
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   └── defaults/main.yml
│   ├── application/
│   │   ├── tasks/main.yml
│   │   └── defaults/main.yml
│   ├── monitoring/
│   └── security/
└── README.md
```
