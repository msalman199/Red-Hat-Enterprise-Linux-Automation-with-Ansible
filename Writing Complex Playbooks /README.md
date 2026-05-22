# Writing Complex Playbooks in Ansible

This repository contains the complete materials, playbooks, and directory frameworks for **Lab 8: Writing Complex Playbooks in Ansible**. This lab guides you through scaling your automation by decomposing monolithic playbooks into multi-play workflows and highly structured Ansible Roles.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Break down complex automation tasks into multiple organized plays targeting distinct host groups.
* Structure playbooks using native Ansible Roles for enhanced configuration organization and reusability.
* Create comprehensive playbooks that systematically configure multiple web and database tiers.
* Implement architectural best practices for complex multi-tier playbook development.
* Use variables, handlers, and Jinja2 templates effectively across decoupled infrastructure blocks.
* Master the explicit operational execution relationships between plays, tasks, and roles.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A basic understanding of core Ansible concepts (playbooks, tasks, and modules).
* Strong familiarity with YAML data syntax and indentation structures.
* Core knowledge of Linux CLI navigation and text configuration files.
* Conceptual knowledge of web server applications (`Apache`/`Nginx`) and relational databases (`MySQL`/`PostgreSQL`).
* Complete baseline fluency from completing previous Ansible labs (Labs 1–7).
* Core networking alignment concepts (TCP/IP ports, services, and firewall policies).

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** inside your staging portal to spawn your environment without any manual virtualization configuration.

Your infrastructure sandbox contains:
* **1 Ansible Control Node** running CentOS/RHEL 8 (Ansible pre-configured).
* **2 Web Server target nodes** running CentOS/RHEL 8.
* **2 Database Server target nodes** running CentOS/RHEL 8.
* **SSH Infrastructure**: Multi-node key-based authentication is pre-seeded and active.

---

## 🛠️ Lab Tasks

### Task 1: Breaking Down Complex Tasks into Multiple Plays

#### Subtask 1.1: Understanding Multi-Play Structure
A clean production playbook should partition multi-tier architectural operations into distinct plays that execute across localized target host layers.

1. **Establish the standard complex playbook multi-directory tree:**
   ```bash
   mkdir -p ~/complex-playbook/{group_vars,host_vars,roles,templates,files}
   cd ~/complex-playbook
   ```

2. **Create the master operational entry-point playbook:**
   ```bash
   nano site.yml
   ```

3. **Incorporate the multi-play operational configurations inside `site.yml`:**
   ```yaml
   ---
   - name: Configure Database Servers
     hosts: database_servers
     become: yes
     vars:
       mysql_root_password: "SecurePass123!"
       mysql_database: "webapp_db"
       mysql_user: "webapp_user"
       mysql_password: "WebApp123!"
     
     tasks:
       - name: Install MySQL server
         yum:
           name: 
             - mysql-server
             - python3-PyMySQL
           state: present
       
       - name: Start and enable MySQL service
         systemd:
           name: mysqld
           state: started
           enabled: yes
       
       - name: Set MySQL root password
         mysql_user:
           name: root
           password: "{{ mysql_root_password }}"
           login_unix_socket: /var/lib/mysql/mysql.sock
           state: present
       
       - name: Create application database
         mysql_db:
           name: "{{ mysql_database }}"
           login_user: root
           login_password: "{{ mysql_root_password }}"
           state: present
       
       - name: Create application user
         mysql_user:
           name: "{{ mysql_user }}"
           password: "{{ mysql_password }}"
           priv: "{{ mysql_database }}.*:ALL"
           login_user: root
           login_password: "{{ mysql_root_password }}"
           state: present

   - name: Configure Web Servers
     hosts: web_servers
     become: yes
     vars:
       web_user: "webadmin"
       document_root: "/var/www/html"
       
     tasks:
       - name: Install Apache web server
         yum:
           name:
             - httpd
             - php
             - php-mysql
           state: present
       
       - name: Create web user
         user:
           name: "{{ web_user }}"
           system: yes
           shell: /bin/bash
           home: /home/{{ web_user }}
           create_home: yes
       
       - name: Start and enable Apache service
         systemd:
           name: httpd
           state: started
           enabled: yes
       
       - name: Configure firewall for HTTP
         firewalld:
           service: http
           permanent: yes
           state: enabled
           immediate: yes

   - name: Deploy Application
     hosts: web_servers
     become: yes
     vars:
       app_name: "webapp"
       
     tasks:
       - name: Create application directory
         file:
           path: "{{ document_root }}/{{ app_name }}"
           state: directory
           owner: apache
           group: apache
           mode: '0755'
       
       - name: Deploy sample PHP application
         copy:
           content: |
             <?php
             $servername = "{{ groups['database_servers'][0] }}";
             $username = "{{ mysql_user }}";
             $password = "{{ mysql_password }}";
             $dbname = "{{ mysql_database }}";
             
             try {
                 $pdo = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
                 $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                 echo "<h1>Database Connection Successful!</h1>";
                 echo "<p>Connected to database: $dbname</p>";
             } catch(PDOException $e) {
                 echo "<h1>Connection failed: " . $e->getMessage() . "</h1>";
             }
             ?>
           dest: "{{ document_root }}/{{ app_name }}/index.php"
           owner: apache
           group: apache
           mode: '0644'
   ```

#### Subtask 1.2: Creating Inventory File
Map the explicit network designations to align with the inventory groups specified within your multi-play architecture.

1. **Create the static tracking inventory initialization file:**
   ```bash
   nano inventory.ini
   ```

2. **Add the structural target endpoints matrix definition:**
   ```ini
   [web_servers]
   web1 ansible_host=10.0.1.10
   web2 ansible_host=10.0.1.11

   [database_servers]
   db1 ansible_host=10.0.1.20
   db2 ansible_host=10.0.1.21

   [all:vars]
   ansible_user=ec2-user
   ansible_ssh_private_key_file=~/.ssh/id_rsa
   ```

#### Subtask 1.3: Testing the Multi-Play Structure
Always evaluate syntax bindings and check logic routines before making live configuration state changes.

1. **Perform an execution test dry-run using the `--check` parameter flag:**
   ```bash
   ansible-playbook -i inventory.ini site.yml --check
   ```

2. **Deploy the configuration live onto your production nodes:**
   ```bash
   ansible-playbook -i inventory.ini site.yml
   ```

---

### Task 2: Organizing Tasks by Roles

#### Subtask 2.1: Creating Role Structure
Roles provide a structured, modular approach to organizing your automation code by separating tasks, variables, templates, and handlers into dedicated directories.

1. **Initialize the specialized role profiles via standard `ansible-galaxy` scoping templates:**
   ```bash
   ansible-galaxy init roles/mysql
   ansible-galaxy init roles/apache
   ansible-galaxy init roles/webapp
   ```

#### Subtask 2.2: Developing the MySQL Role

1. **Populate the primary modular execution logic mapping for MySQL:**
   ```bash
   nano roles/mysql/tasks/main.yml
   ```
   ```yaml
   ---
   - name: Install MySQL packages
     yum:
       name:
         - mysql-server
         - python3-PyMySQL
       state: present

   - name: Start and enable MySQL service
     systemd:
       name: mysqld
       state: started
       enabled: yes

   - name: Set MySQL root password
     mysql_user:
       name: root
       password: "{{ mysql_root_password }}"
       login_unix_socket: /var/lib/mysql/mysql.sock
       state: present
     notify: restart mysql

   - name: Create MySQL configuration file
     template:
       src: my.cnf.j2
       dest: /etc/my.cnf
       backup: yes
     notify: restart mysql

   - name: Create application database
     mysql_db:
       name: "{{ mysql_database }}"
       login_user: root
       login_password: "{{ mysql_root_password }}"
       state: present

   - name: Create application user
     mysql_user:
       name: "{{ mysql_user }}"
       password: "{{ mysql_password }}"
       priv: "{{ mysql_database }}.*:ALL"
       login_user: root
       login_password: "{{ mysql_root_password }}"
       state: present

   - name: Configure firewall for MySQL
     firewalld:
       port: 3306/tcp
       permanent: yes
       state: enabled
       immediate: yes
   ```

2. **Isolate variable profiles using the role defaults layer:**
   ```bash
   nano roles/mysql/defaults/main.yml
   ```
   ```yaml
   ---
   mysql_root_password: "SecurePass123!"
   mysql_database: "webapp_db"
   mysql_user: "webapp_user"
   mysql_password: "WebApp123!"
   mysql_port: 3306
   mysql_bind_address: "0.0.0.0"
   ```

3. **Establish a modular configuration template using a Jinja2 (`.j2`) format:**
   ```bash
   nano roles/mysql/templates/my.cnf.j2
   ```
   ```ini
   [mysqld]
   bind-address = {{ mysql_bind_address }}
   port = {{ mysql_port }}
   datadir = /var/lib/mysql
   socket = /var/lib/mysql/mysql.sock
   user = mysql
   symbolic-links = 0

   [mysqld_safe]
   log-error = /var/log/mysqld.log
   pid-file = /var/run/mysqld/mysqld.pid
   ```

4. **Define event handlers to track and handle automated state resets cleanly:**
   ```bash
   nano roles/mysql/handlers/main.yml
   ```
   ```yaml
   ---
   - name: restart mysql
     systemd:
       name: mysqld
       state: restarted
   ```

#### Subtask 2.3: Developing the Apache Role

1. **Populate the explicit orchestration configuration tasks for the Apache tier:**
   ```bash
   nano roles/apache/tasks/main.yml
   ```
   ```yaml
   ---
   - name: Install Apache and PHP packages
     yum:
       name:
         - httpd
         - php
         - php-mysql
         - php-json
       state: present

   - name: Create web user
     user:
       name: "{{ web_user }}"
       system: yes
       shell: /bin/bash
       home: /home/{{ web_user }}
       create_home: yes

   - name: Configure Apache virtual host
     template:
       src: vhost.conf.j2
       dest: /etc/httpd/conf.d/vhost.conf
     notify: restart apache
   ```

---

### 📁 File Structure

At the conclusion of this lab, your structural workspace directory layout should match this hierarchy exactly:

```text
~/complex-playbook/
├── files/
├── group_vars/
├── host_vars/
├── inventory.ini
├── site.yml
├── templates/
└── roles/
    ├── apache/
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── handlers/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── vhost.conf.j2
    ├── mysql/
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── handlers/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── my.cnf.j2
    └── webapp/
        ├── defaults/
        │   └── main.yml
        ├── handlers/
        │   └── main.yml
        └── tasks/
            └── main.yml
```
