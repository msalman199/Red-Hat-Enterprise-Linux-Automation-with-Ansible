# 🎯 Database Configuration with Ansible

## 📋 Objectives

By the end of this lab, you will be able to:

- Install and configure MySQL and PostgreSQL database servers on remote Linux hosts using Ansible
- Create databases and database users through Ansible playbooks
- Implement database security best practices by configuring proper permissions and access controls
- Write reusable Ansible roles for database management tasks
- Understand the fundamentals of Infrastructure as Code (IaC) for database administration
- Troubleshoot common database configuration issues in automated deployments

---

## 💻 Prerequisites

Before starting this lab, you should have:

- Basic understanding of Linux command line operations
- Familiarity with YAML syntax and structure
- Basic knowledge of Ansible concepts (playbooks, tasks, modules)
- Understanding of database concepts (users, permissions, schemas)
- Completion of previous Ansible labs or equivalent experience
- Basic networking knowledge (IP addresses, ports, SSH)

> 💡 **Note:** Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click **Start Lab** to access your pre-configured environment.

---

## 🛠️ Lab Environment Setup

Your lab environment includes:

- **Control Node:** CentOS/RHEL 8 machine with Ansible pre-installed
- **Target Nodes:** Two Ubuntu 20.04 LTS servers for database installation
- All necessary network connectivity and SSH keys pre-configured

---

## 📂 Project Structure

```text
ansible-database-lab/
├── inventory.ini
├── playbooks/
│   ├── mysql-setup.yml
│   └── postgresql-setup.yml
├── templates/
│   └── my.cnf.j2
├── roles/
├── group_vars/
├── host_vars/
├── files/
└── README.md
```

---

## 🚀 Task 1: Environment Preparation and Inventory Setup

### Subtask 1.1: Verify Lab Environment

Connect to your control node via the terminal and check your setup:

```bash
# Check Ansible installation
ansible --version

# Verify target host connectivity
ansible all -m ping
```

---

### Subtask 1.2: Create Project Directory Structure

Initialize your workspace folders and deploy your infrastructure runtime hosts layout map:

```bash
# Create main lab directory workspace
mkdir -p ~/ansible-database-lab && cd ~/ansible-database-lab

# Create structural subdirectories
mkdir -p {playbooks,roles,group_vars,host_vars,files,templates}

# Create inventory definition configuration mapping
cat > inventory.ini << 'EOF'
[mysql_servers]
mysql-server ansible_host=10.0.1.10

[postgresql_servers]
postgres-server ansible_host=10.0.1.11

[database_servers:children]
mysql_servers
postgresql_servers

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/lab_key
EOF
```

---

### Subtask 1.3: Test Inventory Configuration

Verify your targeted infrastructure mapping configuration is active and connected:

```bash
# List complete registered inventory details
ansible-inventory -i inventory.ini --list

# Verify targeted connectivity across discrete host engines
ansible mysql_servers -i inventory.ini -m ping
ansible postgresql_servers -i inventory.ini -m ping
```

---

## 🚀 Task 2: MySQL Installation and Configuration

### Subtask 2.1: Create MySQL Installation Playbook

Build out your package configurations, custom system handlers, and credential logic:

```bash
cat > playbooks/mysql-setup.yml << 'EOF'
---
- name: Install and Configure MySQL Server
  hosts: mysql_servers
  become: yes
  vars:
    mysql_root_password: "SecureRootPass123!"
    mysql_databases:
      - name: webapp_db
        encoding: utf8mb4
        collation: utf8mb4_unicode_ci
      - name: inventory_db
        encoding: utf8mb4
        collation: utf8mb4_unicode_ci
    mysql_users:
      - name: webapp_user
        password: "WebAppPass123!"
        priv: "webapp_db.*:ALL"
        host: "%"
      - name: inventory_user
        password: "InventoryPass123!"
        priv: "inventory_db.*:SELECT,INSERT,UPDATE,DELETE"
        host: "localhost"

  tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install MySQL server and client
      apt:
        name:
          - mysql-server
          - mysql-client
          - python3-pymysql
        state: present

    - name: Start and enable MySQL service
      systemd:
        name: mysql
        state: started
        enabled: yes

    - name: Set MySQL root password
      mysql_user:
        name: root
        password: "{{ mysql_root_password }}"
        login_unix_socket: /var/run/mysqld/mysqld.sock
        state: present

    - name: Create MySQL configuration file for root
      template:
        src: my.cnf.j2
        dest: /root/.my.cnf
        owner: root
        group: root
        mode: '0600'

    - name: Remove anonymous MySQL users
      mysql_user:
        name: ""
        host_all: yes
        state: absent
        login_user: root
        login_password: "{{ mysql_root_password }}"

    - name: Remove MySQL test database
      mysql_db:
        name: test
        state: absent
        login_user: root
        login_password: "{{ mysql_root_password }}"

    - name: Create MySQL databases
      mysql_db:
        name: "{{ item.name }}"
        encoding: "{{ item.encoding }}"
        collation: "{{ item.collation }}"
        state: present
        login_user: root
        login_password: "{{ mysql_root_password }}"
      loop: "{{ mysql_databases }}"

    - name: Create MySQL users
      mysql_user:
        name: "{{ item.name }}"
        password: "{{ item.password }}"
        priv: "{{ item.priv }}"
        host: "{{ item.host }}"
        state: present
        login_user: root
        login_password: "{{ mysql_root_password }}"
      loop: "{{ mysql_users }}"

    - name: Configure MySQL for remote connections
      lineinfile:
        path: /etc/mysql/mysql.conf.d/mysqld.cnf
        regexp: '^bind-address'
        line: 'bind-address = 0.0.0.0'
        backup: yes
      notify: restart mysql

    - name: Open MySQL port in firewall
      ufw:
        rule: allow
        port: '3306'
        proto: tcp

  handlers:
    - name: restart mysql
      systemd:
        name: mysql
        state: restarted
EOF
```

---

### Subtask 2.2: Create MySQL Configuration Template

Deploy a client fallback validation schema for system root logins:

```bash
mkdir -p templates

cat > templates/my.cnf.j2 << 'EOF'
[client]
user=root
password={{ mysql_root_password }}
socket=/var/run/mysqld/mysqld.sock

[mysql]
user=root
password={{ mysql_root_password }}
socket=/var/run/mysqld/mysqld.sock
EOF
```

---

### Subtask 2.3: Execute MySQL Installation

Run and verify your live data platform cluster deployment engines:

```bash
# Execute your MySQL orchestration deployment pipeline
ansible-playbook -i inventory.ini playbooks/mysql-setup.yml

# Verify target service engine daemon health state status indicators
ansible mysql_servers -i inventory.ini -m shell -a "systemctl status mysql" --become

# Assert cluster delivery authentication schema permissions access structures
ansible mysql_servers -i inventory.ini -m shell -a "mysql -u root -p'SecureRootPass123!' -e 'SHOW DATABASES;'" --become
```

---

## 🚀 Task 3: PostgreSQL Installation and Configuration

### Subtask 3.1: Create PostgreSQL Installation Playbook

Deploy configuration engines targeting structured enterprise relational backends:

```bash
cat > playbooks/postgresql-setup.yml << 'EOF'
---
- name: Install and Configure PostgreSQL Server
  hosts: postgresql_servers
  become: yes
  vars:
    postgresql_version: "12"
    postgresql_databases:
      - name: ecommerce_db
        owner: ecommerce_user
        encoding: UTF8
        locale: en_US.UTF-8
      - name: analytics_db
        owner: analytics_user
        encoding: UTF8
        locale: en_US.UTF-8
    postgresql_users:
      - name: ecommerce_user
        password: "EcommercePass123!"
        role_attr_flags: CREATEDB,NOSUPERUSER
      - name: analytics_user
        password: "AnalyticsPass123!"
        role_attr_flags: NOCREATEDB,NOSUPERUSER
      - name: readonly_user
        password: "ReadOnlyPass123!"
        role_attr_flags: NOCREATEDB,NOSUPERUSER

  tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install PostgreSQL and dependencies
      apt:
        name:
          - "postgresql-{{ postgresql_version }}"
          - "postgresql-contrib-{{ postgresql_version }}"
          - python3-psycopg2
          - acl
        state: present

    - name: Start and enable PostgreSQL service
      systemd:
        name: postgresql
        state: started
        enabled: yes

    - name: Create PostgreSQL users
      postgresql_user:
        name: "{{ item.name }}"
        password: "{{ item.password }}"
        role_attr_flags: "{{ item.role_attr_flags }}"
        state: present
      become_user: postgres
      loop: "{{ postgresql_users }}"

    - name: Create PostgreSQL databases
      postgresql_db:
        name: "{{ item.name }}"
        owner: "{{ item.owner }}"
        encoding: "{{ item.encoding }}"
        lc_collate: "{{ item.locale }}"
        lc_ctype: "{{ item.locale }}"
        state: present
      become_user: postgres
      loop: "{{ postgresql_databases }}"

    - name: Configure PostgreSQL remote connections path
      lineinfile:
        path: "/etc/postgresql/{{ postgresql_version }}/main/postgresql.conf"
        regexp: "^#?listen_addresses"
        line: "listen_addresses = '*'"
        backup: yes
      notify: restart postgresql

    - name: Configure client authentication schema methods
      lineinfile:
