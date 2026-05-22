# Managing Files with Ansible

This repository contains the complete materials, playbooks, and template frameworks for **Lab 10: Managing Files with Ansible**. This lab guides you through the technical foundations of configuration automation by separating static assets from adaptive, dynamically rendered environments.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Understand the core architectural differences between static and dynamic file management in Ansible.
* Use the `copy` module to transfer immutable files securely from the control node to managed hosts.
* Implement the `template` module to deploy responsive configuration files via Jinja2 parsing.
* Harness Ansible system facts and variables to customize file text dynamically across multiple targets.
* Force structural enforcement of file system permissions, owners, and secure directory traits during flight.
* Track down, debug, and troubleshoot syntax block issues or broken validation runs in file playbooks.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A foundational understanding of Linux directory layouts, security masks, and path flags.
* Strong familiarity with YAML indent spacing, list arrays, and dictionary maps.
* Completion of preceding Ansible labs covering inventories and basic tasks (Labs 1–9).
* General knowledge of variables, system parameters, and text evaluation structures.
* Familiarity with command-line editors like `nano` or `vim`.

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** inside your workspace interface to launch your pre-seeded lab architecture instantly.

Your sandbox perimeter contains:
* **Control Node**: A centralized machine running CentOS/RHEL 8 with Ansible pre-installed.
* **Managed Hosts**: Two targeted target nodes (`web1` and `web2`) ready for immediate execution.
* **Network & Access**: All target hosts are connected with authorized internal networks and pre-authenticated SSH keys.

---

## 🛠️ Lab Tasks

### Task 1: Using the Copy Module for Static Files

#### Subtask 1.1: Create a Static Configuration File
Static files are best used for immutable configuration segments that must remain completely identical across every server node in your target pool.

1. **Connect to your control node and move into your workspace:**
   ```bash
   cd /home/student/ansible-labs
   mkdir -p lab10-file-management/static-files
   cd lab10-file-management
   ```

2. **Create the static security hardening profile configuration file:**
   ```bash
   nano static-files/apache-security.conf
   ```

3. **Paste the following rigid parameters directly into the file:**
   ```apache
   # Security Configuration for Apache Web Server
   ServerTokens Prod
   ServerSignature Off

   # Hide Apache version information
   Header always unset "X-Powered-By"
   Header unset "X-Powered-By"

   # Prevent access to .htaccess files
   <Files ".ht*">
       Require all denied
   </Files>

   # Disable server-status and server-info
   <Location "/server-status">
       Require all denied
   </Location>

   <Location "/server-info">
       Require all denied
   </Location>
   ```

#### Subtask 1.2: Create a Playbook Using the Copy Module
The `copy` module transfers assets directly from your control node local storage while ensuring runtime validation passes before committing configurations.

1. **Generate the copy playbook configuration wrapper file:**
   ```bash
   nano copy-static-files.yml
   ```

2. **Incorporate the following multi-task payload architecture:**
   ```yaml
   ---
   - name: Copy Static Files to Web Servers
     hosts: webservers
     become: yes
     vars:
       apache_config_dir: /etc/httpd/conf.d
       backup_dir: /backup/configs
     
     tasks:
       - name: Ensure backup directory exists
         file:
           path: "{{ backup_dir }}"
           state: directory
           mode: '0755'
           owner: root
           group: root

       - name: Copy Apache security configuration
         copy:
           src: static-files/apache-security.conf
           dest: "{{ apache_config_dir }}/security.conf"
           owner: root
           group: root
           mode: '0644'
           backup: yes
           validate: 'httpd -t -f %s'
         notify: restart apache

       - name: Copy custom index.html file
         copy:
           content: |
             <!DOCTYPE html>
             <html>
             <head>
                 <title>Welcome to {{ inventory_hostname }}</title>
             </head>
             <body>
                 <h1>Static Content Deployed Successfully!</h1>
                 <p>This server is: {{ inventory_hostname }}</p>
                 <p>Deployed on: {{ ansible_date_time.date }}</p>
             </body>
             </html>
           dest: /var/www/html/index.html
           owner: apache
           group: apache
           mode: '0644'

       - name: Copy binary file (favicon)
         copy:
           src: static-files/favicon.ico
           dest: /var/www/html/favicon.ico
           owner: apache
           group: apache
           mode: '0644'
         ignore_errors: yes

     handlers:
       - name: restart apache
         service:
           name: httpd
           state: restarted
   ```

#### Subtask 1.3: Create Additional Static Files
Seed the secondary binary placeholders and establish localized group scopes before kicking off execution routines.

1. **Construct a simple text-based asset placeholder representing the binary target:**
   ```bash
   echo "FAVICON" > static-files/favicon.ico
   ```

2. **Establish your local environmental tracking endpoints:**
   ```bash
   nano inventory.ini
   ```

3. **Incorporate the network targeting map configuration parameters:**
   ```ini
   [webservers]
   web1 ansible_host=192.168.1.10
   web2 ansible_host=192.168.1.11

   [all:vars]
   ansible_user=student
   ansible_ssh_private_key_file=~/.ssh/id_rsa
   ```

#### Subtask 1.4: Execute the Copy Playbook
Trigger the playbook initialization routines and run immediate shell verification commands to prove structural fidelity.

1. **Deploy your static configurations using your inventory routing map:**
   ```bash
   ansible-playbook -i inventory.ini copy-static-files.yml
   ```

2. **Verify target paths across your web instances via direct verification checks:**
   ```bash
   ansible webservers -i inventory.ini -m shell -a "ls -la /etc/httpd/conf.d/security.conf"
   ansible webservers -i inventory.ini -m shell -a "ls -la /var/www/html/"
   ```

---

### Task 2: Using the Template Module for Dynamic Configuration Files

#### Subtask 2.1: Create Jinja2 Templates
Dynamic file management relies on Jinja2 parsing rules to construct system configurations based on targeted system parameters and inventory metrics.

1. **Initialize the template holding directory structure:**
   ```bash
   mkdir templates
   ```

2. **Open your target Virtual Host dynamic routing template file:**
   ```bash
   nano templates/vhost.conf.j2
   ```

3. **Add the dynamic loop parsing logic variables into `vhost.conf.j2`:**
   ```ini
   # Virtual Host Configuration for {{ server_name }}
   # Generated automatically by Ansible

   <VirtualHost *:{{ http_port | default(80) }}>
       ServerName {{ server_name }}
       {% if server_aliases is defined %}
       {% for alias in server_aliases %}
       ServerAlias {{ alias }}
       {% endfor %}
       {% endif %}
       
       DocumentRoot {{ document_root | default('/var/www/html') }}
       
       # Logging Configuration
       ErrorLog {{ log_dir }}/{{ server_name }}_error.log
       CustomLog {{ log_dir }}/{{ server_name }}_access.log combined
       
       # Security Headers
       {% if enable_security_headers | default(true) %}
       Header always set X-Content-Type-Options nosniff
       Header always set X-Frame-Options DENY
       Header always set X-XSS-Protection "1; mode=block"
       {% endif %}
       
       # Environment-specific settings
       {% if ansible_hostname == 'web1' %}
       # Primary server configuration
       SetEnv SERVER_ROLE "primary"
       {% else %}
       # Secondary server configuration
       SetEnv SERVER_ROLE "secondary"
       {% endif %}
       
       <Directory "{{ document_root }}">
           Options {{ directory_options | default('Indexes FollowSymLinks') }}
           AllowOverride {{ allow_override | default('None') }}
           Require all granted
       </Directory>
       
       {% if ssl_enabled | default(false) %}
       # SSL Configuration
       SSLEngine on
       SSLCertificateFile {{ ssl_cert_path }}
       SSLCertificateKeyFile {{ ssl_key_path }}
       {% endif %}
   </VirtualHost>
   ```

4. **Open a system mapping metrics reporting template file:**
   ```bash
   nano templates/system-info.conf.j2
   ```

5. **Populate the runtime facts extraction parameters inside `system-info.conf.j2`:**
   ```ini
   # System Information Configuration
   # Generated on {{ ansible_date_time.date }} at {{ ansible_date_time.time }}

   # Server Details
   HOSTNAME={{ inventory_hostname }}
   SERVER_IP={{ ansible_default_ipv4.address }}
   TOTAL_MEMORY={{ ansible_memtotal_mb }}MB
   CPU_CORES={{ ansible_processor_vcpus }}
   OS_FAMILY={{ ansible_os_family }}
   OS_VERSION={{ ansible_distribution_version }}

   # Environment Configuration
   ENVIRONMENT={{ environment | default('production') }}
   APPLICATION_PORT={{ app_port | default(8080) }}
   MAX_CONNECTIONS={{ max_connections | default(100) }}

   # Feature Flags
   {% for feature, enabled in feature_flags.items() %}
   {{ feature | upper }}_ENABLED={{ enabled | lower }}
   {% endfor %}

   # Custom Variables
   {% if custom_vars is defined %}
   {% for key, value in custom_vars.items() %}
   {{ key | upper }}={{ value }}
   {% endfor %}
   {% endif %}
   ```

#### Subtask 2.2: Create Variables for Templates
Decouple structural file designs from system variable parameters by using group files to drive values safely.

1. **Establish the localized group variable repository tree configuration:**
   ```bash
   mkdir -p group_vars
   nano group_vars/webservers.yml
   ```

2. **Add the structural tracking variables inside `webservers.yml`:**
   ```yaml
   ---
   # Apache Configuration Variables
   http_port: 80
   log_dir: /var/log/httpd
   enable_security_headers: true
   directory_options: "Indexes FollowSymLinks"
   allow_override: "All"

   # SSL Configuration
   ssl_enabled: false
   ssl_cert_path: /etc/ssl/certs/server.crt
   ssl_key_path: /etc/ssl/private/server.key

   # Application Configuration
   environment: production
   app_port: 8080
   max_connections: 150

   # Feature Flags
   feature_flags:
     caching: true
     compression: true
   ```

---

### 📁 File Structure

At the conclusion of this lab, your workspace layout will align with this tree hierarchy:

```text
~/lab10-file-management/
├── copy-static-files.yml       # Playbook managing static asset distribution
├── group_vars/
│   └── webservers.yml          # Dynamic configuration variables for templates
├── inventory.ini               # Production environment infrastructure inventory
├── static-files/
│   ├── apache-security.conf    # Immutable security parameters file
│   └── favicon.ico             # Static asset binary placeholder
└── templates/
    ├── system-info.conf.j2     # Dynamic system facts engine template
    └── vhost.conf.j2           # Dynamic Jinja2 server host routing template
```
