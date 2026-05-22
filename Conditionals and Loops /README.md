# Lab 6: Conditionals and Loops in Ansible

This repository contains the complete materials and playbooks for **Lab 6: Conditionals and Loops in Ansible**. This lab guides you through automating infrastructure dynamic tasks using conditional state validation and iterative loops.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Implement conditional logic using `when` statements in Ansible playbooks.
* Create and execute loops to handle repetitive tasks efficiently.
* Apply conditionals to control task execution based on system facts and variables.
* Use various loop constructs to install multiple packages and manage configurations.
* Combine conditionals and loops to create dynamic and flexible automation scripts.
* Troubleshoot common issues with conditional statements and loop structures.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* Basic understanding of YAML syntax and structure.
* Familiarity with Ansible playbook fundamentals from previous labs.
* Knowledge of Ansible facts and variables.
* Understanding of basic Linux commands and package management.
* Completion of Labs 1-5 in this series.

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provided by Al Nafi for this lab. Simply click **Start Lab** to access your pre-configured environment.

Your lab environment includes:
* **Control node**: Central machine with Ansible pre-installed.
* **Managed nodes**: Two target servers.
* **Credentials & Configurations**: All necessary SSH keys and inventory files configured automatically.

---

## 🛠️ Lab Tasks

### Task 1: Understanding and Implementing Conditional Logic

#### Subtask 1.1: Basic Conditional Statements
Conditionals in Ansible allow you to control when tasks should run based on specific conditions. The `when` statement is the primary method for implementing conditional logic.

1. **Create a new directory for this lab and navigate to it:**
   ```bash
   mkdir ~/lab6-conditionals-loops
   cd ~/lab6-conditionals-loops
   ```

2. **Create your first conditional playbook:**
   ```bash
   nano basic-conditionals.yml
   ```

3. **Add the following content to demonstrate basic conditional logic:**
   ```yaml
   ---
   - name: Basic Conditionals Demo
     hosts: all
     gather_facts: yes
     vars:
       install_web_server: true
       environment_type: "production"
       
     tasks:
       - name: Install Apache web server (only if variable is true)
         yum:
           name: httpd
           state: present
         when: install_web_server == true
         
       - name: Start Apache service (only on production)
         service:
           name: httpd
           state: started
           enabled: yes
         when: environment_type == "production"
         
       - name: Display message for development environment
         debug:
           msg: "This is a development environment - web server not started"
         when: environment_type == "development"
         
       - name: Install development tools (only on CentOS/RHEL)
         yum:
           name:
             - git
             - vim
             - curl
           state: present
         when: ansible_os_family == "RedHat"
         
       - name: Install development tools (only on Ubuntu/Debian)
         apt:
           name:
             - git
             - vim
             - curl
           state: present
         when: ansible_os_family == "Debian"
   ```

4. **Run the playbook to see conditional logic in action:**
   ```bash
   ansible-playbook -i inventory basic-conditionals.yml
   ```

#### Subtask 1.2: Advanced Conditional Logic

1. **Create a more complex conditional playbook:**
   ```bash
   nano advanced-conditionals.yml
   ```

2. **Add advanced conditional examples:**
   ```yaml
   ---
   - name: Advanced Conditionals Demo
     hosts: all
     gather_facts: yes
     vars:
       required_memory_gb: 2
       required_disk_space_gb: 10
       
     tasks:
       - name: Check if system meets memory requirements
         debug:
           msg: "System has {{ ansible_memtotal_mb // 1024 }}GB RAM - meets requirements"
         when: (ansible_memtotal_mb // 1024) >= required_memory_gb
         
       - name: Warning for insufficient memory
         debug:
           msg: "WARNING: System has only {{ ansible_memtotal_mb // 1024 }}GB RAM"
         when: (ansible_memtotal_mb // 1024) < required_memory_gb
         
       - name: Install monitoring tools on servers with sufficient resources
         yum:
           name:
             - htop
             - iotop
             - nethogs
           state: present
         when: 
           - (ansible_memtotal_mb // 1024) >= required_memory_gb
           - ansible_os_family == "RedHat"
           
       - name: Configure firewall (only if firewalld is installed)
         firewalld:
           service: http
           permanent: yes
           state: enabled
           immediate: yes
         when: ansible_facts['packages']['firewalld'] is defined
         ignore_errors: yes
         
       - name: Create backup directory (only on weekends)
         file:
           path: /opt/weekend-backup
           state: directory
           mode: '0755'
         when: ansible_date_time.weekday in ['5', '6']  # Saturday=5, Sunday=6
   ```

3. **Execute the advanced conditionals playbook:**
   ```bash
   ansible-playbook -i inventory advanced-conditionals.yml
   ```

---

### Task 2: Implementing Loops for Repetitive Tasks

#### Subtask 2.1: Basic Loop Structures
Loops in Ansible help you avoid repetitive code by iterating over lists, dictionaries, or other data structures.

1. **Create a basic loops demonstration playbook:**
   ```bash
   nano basic-loops.yml
   ```

2. **Add basic loop examples:**
   ```yaml
   ---
   - name: Basic Loops Demo
     hosts: all
     gather_facts: yes
     
     tasks:
       - name: Install multiple packages using loop
         yum:
           name: "{{ item }}"
           state: present
         loop:
           - wget
           - unzip
           - tree
           - nano
           - screen
           
       - name: Create multiple users
         user:
           name: "{{ item }}"
           state: present
           shell: /bin/bash
           create_home: yes
         loop:
           - alice
           - bob
           - charlie
           
       - name: Create multiple directories
         file:
           path: "/opt/{{ item }}"
           state: directory
           mode: '0755'
         loop:
           - app1
           - app2
           - app3
           - logs
           - backups
           
       - name: Display information about each user
         debug:
           msg: "Processing user: {{ item }}"
         loop:
           - alice
           - bob
           - charlie
   ```

3. **Run the basic loops playbook:**
   ```bash
   ansible-playbook -i inventory basic-loops.yml
   ```

#### Subtask 2.2: Advanced Loop Techniques

1. **Create an advanced loops playbook:**
   ```bash
   nano advanced-loops.yml
   ```

2. **Add advanced loop examples with dictionaries and complex data:**
   ```yaml
   ---
   - name: Advanced Loops Demo
     hosts: all
     gather_facts: yes
     vars:
       web_applications:
         - name: "webapp1"
           port: 8080
           user: "webapp1user"
           directory: "/opt/webapp1"
         - name: "webapp2"
           port: 8081
           user: "webapp2user"
           directory: "/opt/webapp2"
         - name: "webapp3"
           port: 8082
           user: "webapp3user"
           directory: "/opt/webapp3"
           
       database_configs:
         mysql:
           port: 3306
           config_file: "/etc/mysql/my.cnf"
           service: "mysqld"
         postgresql:
           port: 5432
           config_file: "/etc/postgresql/postgresql.conf"
           service: "postgresql"
           
     tasks:
       - name: Create users for web applications
         user:
           name: "{{ item.user }}"
           state: present
           shell: /bin/bash
           create_home: yes
         loop: "{{ web_applications }}"
         
       - name: Create directories for web applications
         file:
           path: "{{ item.directory }}"
           state: directory
           owner: "{{ item.user }}"
           group: "{{ item.user }}"
           mode: '0755'
         loop: "{{ web_applications }}"
         
       - name: Display web application configurations
         debug:
           msg: "App: {{ item.name }}, Port: {{ item.port }}, User: {{ item.user }}"
         loop: "{{ web_applications }}"
         
       - name: Process database configurations
         debug:
           msg: "Database: {{ item.key }}, Port: {{ item.value.port }}, Service: {{ item.value.service }}"
         loop: "{{ database_configs | dict2items }}"
         
       - name: Install packages with version control
         yum:
           name: "{{ item.name }}"
           state: "{{ item.state | default('present') }}"
         loop:
           - { name: "httpd", state: "present" }
           - { name: "php", state: "present" }
           - { name: "php-mysql", state: "present" }
           - { name: "mariadb-server", state: "present" }
   ```

3. **Execute the advanced loops playbook:**
   ```bash
   ansible-playbook -i inventory advanced-loops.yml
   ```

---

## 🏁 Conclusion
In this lab, you successfully transitioned from static configuration files to flexible, intelligent automation scripts. By completing these tasks, you have mastered:
* **Task Optimization**: Replacing repetitive block definitions with modular `loop` expressions, vastly cleaner codebases, and faster implementation timelines.
* **Intelligent Configurations**: Utilizing `when` filters alongside gathered facts to seamlessly scale operations across varying distributions (`RedHat` vs `Debian`) and dynamic resource tiers.
* **Complex Data Management**: Harnessing structures like lists of dictionaries and transformation utilities like `dict2items` to navigate nested setups smoothly.

These combined mechanisms provide the baseline required to construct enterprise-grade, OS-agnostic infrastructure deployments.
