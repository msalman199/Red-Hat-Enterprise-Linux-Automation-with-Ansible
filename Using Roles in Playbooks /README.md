# Using Roles in Playbooks

This repository contains the complete materials, playbooks, and structural templates for **Lab 9: Using Roles in Playbooks**. This lab guides you through modularizing infrastructure automation configurations by designing, creating, and implementing structured Ansible Roles.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Understand the core structural architecture and organizational benefits of Ansible roles.
* Create a custom role to install and configure an Apache HTTP web server.
* Organize tasks, handlers, and templates systematically into dedicated role directories.
* Include and reference customized roles inside modular playbooks effectively.
* Apply role-based automation paradigms to control multi-system web server configurations.
* Implement production-grade design best practices for role layout, parameters, and organization.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A basic understanding of Linux CLI command navigation and core tool operations.
* Strong familiarity with YAML syntax design, formatting arrays, and list structures.
* Completion of previous Ansible labs covering foundational playbook layouts and execution flows.
* Conceptual knowledge of web routing targets and web server setups (Apache HTTP Server).
* Clear understanding of Linux system file permissions, owners, and directory trees.

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** in your portal to spin up your testing sandbox instantly without configuration overhead.

Your orchestration topology includes:
* **1 Ansible Control Node**: Management node with Ansible preinstalled.
* **2 Managed Target Nodes**: Destination endpoints acting as target web servers.
* **Core Utilities**: Integrated network configurations, SSH access, and core text utilities (`nano`, `vim`).

---

## 🛠️ Lab Tasks

### Task 1: Understanding Ansible Roles Structure

#### Subtask 1.1: Explore the Standard Role Directory Structure
Ansible uses designated folder trees to read properties, default variables, templates, and execution parameters accurately without explicit file mappings.

1. **Navigate to your workspace directory root and initialize the project skeleton:**
   ```bash
   cd ~
   mkdir -p ansible-lab9/roles
   cd ansible-lab9
   ```

2. **Create the explicit standard role subdirectory tree layout for an Apache server role:**
   ```bash
   mkdir -p roles/apache-webserver/{tasks,handlers,templates,files,vars,defaults,meta}
   ```

3. **Verify the initialized configuration paths:**
   ```bash
   tree roles/
   ```
   *Expected Output Structure:*
   ```text
   roles/
   └── apache-webserver
       ├── defaults
       ├── files
       ├── handlers
       ├── meta
       ├── tasks
       ├── templates
       └── vars
   ```

#### Subtask 1.2: Understanding Each Directory Purpose
Create a quick structural reference manual tracking the explicit purpose of each subdirectory layer.

1. **Generate the target manual reference log text file:**
   ```bash
   cat > role-structure-guide.txt << 'EOF'
   Ansible Role Directory Structure:

   tasks/     - Contains the main list of tasks to be executed by the role
   handlers/  - Contains handlers triggered by notify statements
   templates/ - Contains Jinja2 template files
   files/     - Contains files to be copied to managed nodes
   vars/      - Contains variables for the role (higher precedence)
   defaults/  - Contains default variables for the role (lower precedence)
   meta/      - Contains role metadata and dependencies
   EOF
   ```

---

### Task 2: Create a Custom Role for Installing Apache Web Server

#### Subtask 2.1: Create the Main Tasks File
The `tasks/main.yml` block isolates your execution steps into fine-grained tasks optimized for role distribution.

1. **Populate the core execution profile tasks inside the role:**
   ```bash
   cat > roles/apache-webserver/tasks/main.yml << 'EOF'
   ---
   # Main tasks file for apache-webserver role

   - name: Install Apache HTTP Server
     package:
       name: "{{ apache_package_name }}"
       state: present
     become: yes

   - name: Start and enable Apache service
     service:
       name: "{{ apache_service_name }}"
       state: started
       enabled: yes
     become: yes
     notify: restart apache

   - name: Create document root directory
     file:
       path: "{{ document_root }}"
       state: directory
       owner: "{{ apache_user }}"
       group: "{{ apache_group }}"
       mode: '0755'
     become: yes

   - name: Deploy custom index.html from template
     template:
       src: index.html.j2
       dest: "{{ document_root }}/index.html"
       owner: "{{ apache_user }}"
       group: "{{ apache_group }}"
       mode: '0644'
     become: yes
     notify: restart apache

   - name: Configure Apache virtual host
     template:
       src: vhost.conf.j2
       dest: "{{ apache_config_dir }}/{{ site_name }}.conf"
       owner: root
       group: root
       mode: '0644'
     become: yes
     notify: restart apache

   - name: Open firewall for HTTP traffic
     firewalld:
       service: http
       permanent: yes
       state: enabled
       immediate: yes
     become: yes
     ignore_errors: yes
   EOF
   ```

#### Subtask 2.2: Create Default Variables
Default variables serve as safe baseline indicators that hold low precedence values, allowing users to override configurations easily later.

1. **Configure baseline standard variables within the defaults space:**
   ```bash
   cat > roles/apache-webserver/defaults/main.yml << 'EOF'
   ---
   # Default variables for apache-webserver role

   # Package and service names (will vary by OS)
   apache_package_name: httpd
   apache_service_name: httpd
   apache_user: apache
   apache_group: apache

   # Paths and directories
   document_root: /var/www/html
   apache_config_dir: /etc/httpd/conf.d

   # Site configuration
   site_name: default-site
   server_name: "{{ ansible_fqdn }}"
   server_admin: admin@example.com

   # Custom variables
   welcome_message: "Welcome to our Apache Web Server!"
   company_name: "Al Nafi Learning Lab"
   EOF
   ```

#### Subtask 2.3: Create Variable Overrides
The `vars/main.yml` file defines high-precedence constants tailored specifically for the role's execution mechanics.

1. **Seed the explicit system overrides tracking block:**
   ```bash
   cat > roles/apache-webserver/vars/main.yml << 'EOF'
   ---
   # Role variables for apache-webserver (higher precedence than defaults)

   # These variables override defaults and are specific to this role
   apache_port: 80
   max_connections: 100
   timeout: 300

   # Security settings
   server_tokens: "Prod"
   server_signature: "Off"
   EOF
   ```

---

### Task 3: Create Handlers for the Role

#### Subtask 3.1: Define Service Handlers
Handlers register explicit actions that run at the conclusion of a play when called via `notify` signals.

1. **Populate the system lifecycle runtime service handlers file:**
   ```bash
   cat > roles/apache-webserver/handlers/main.yml << 'EOF'
   ---
   # Handlers for apache-webserver role

   - name: restart apache
     service:
       name: "{{ apache_service_name }}"
       state: restarted
     become: yes

   - name: reload apache
     service:
       name: "{{ apache_service_name }}"
       state: reloaded
     become: yes

   - name: start apache
     service:
       name: "{{ apache_service_name }}"
       state: started
     become: yes

   - name: stop apache
     service:
       name: "{{ apache_service_name }}"
       state: stopped
     become: yes
   EOF
   ```

---

### Task 4: Create Templates for Configuration Files

#### Subtask 4.1: Create HTML Template
Use dynamic Jinja2 syntax to automatically interpolate server environment data into static system documents.

1. **Build the automated index web home asset template:**
   ```bash
   cat > roles/apache-webserver/templates/index.html.j2 << 'EOF'
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>{{ company_name }} - Web Server</title>
       <style>
           body {
               font-family: Arial, sans-serif;
               margin: 0;
               padding: 20px;
               background-color: #f4f4f4;
           }
           .container {
               max-width: 800px;
               margin: 0 auto;
               background-color: white;
               padding: 30px;
               border-radius: 10px;
               box-shadow: 0 0 10px rgba(0,0,0,0.1);
           }
           h1 {
               color: #333;
               text-align: center;
           }
           .info {
               background-color: #e7f3ff;
               padding: 15px;
               border-left: 4px solid #2196F3;
               margin: 20px 0;
           }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>{{ welcome_message }}</h1>
           <div class="info">
               <h3>Server Information:</h3>
               <p><strong>Hostname:</strong> {{ ansible_hostname }}</p>
               <p><strong>IP Address:</strong> {{ ansible_default_ipv4.address }}</p>
               <p><strong>Operating System:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}</p>
               <p><strong>Server Admin:</strong> {{ server_admin }}</p>
               <p><strong>Deployed by:</strong> Ansible Role</p>
           </div>
           <p>This web server was configured automatically using Ansible roles!</p>
           <p><em>Powered by {{ company_name }}</em></p>
       </div>
   </body>
   </html>
   EOF
   ```

#### Subtask 4.2: Create Apache Virtual Host Template
Dynamic templates evaluate configurations on the fly based on variable definitions and specific node requirements.

1. **Build the targeted Virtual Host routing configuration engine template:**
   ```bash
   cat > roles/apache-webserver/templates/vhost.conf.j2 << 'EOF'
   # Virtual Host Configuration for {{ site_name }}
   # Generated by Ansible Role: apache-webserver

   <VirtualHost *:#{ apache_port }}>
       ServerName {{ server_name }}
       ServerAdmin {{ server_admin }}
       DocumentRoot {{ document_root }}
       
       # Security settings
       ServerTokens {{ server_tokens }}
       ServerSignature {{ server_signature }}
       
       # Performance settings
       Timeout {{ timeout }}
       MaxRequestWorkers {{ max_connections }}
       
       # Logging
       ErrorLog logs/{{ site_name }}_error.log
       CustomLog logs/{{ site_name }}_access.log combined
       
       # Directory permissions
       <Directory "{{ document_root }}">
           Options Indexes FollowSymLinks
           AllowOverride None
           Require all granted
       </Directory>
   </VirtualHost>
   EOF
   ```
*(Note: Replace `#` with `{{` in the VirtualHost opening tag line if required to match specific Jinja template constraints).*

---

### 📁 File Structure
At the conclusion of these architecture modules, your working directory framework will match this file map hierarchy exactly:

```text
~/ansible-lab9/
├── role-structure-guide.txt
└── roles/
    └── apache-webserver/
        ├── defaults/
        │   └── main.yml
        ├── files/
        ├── handlers/
        │   └── main.yml
        ├── meta/
        ├── tasks/
        │   └── main.yml
        ├── templates/
        │   ├── index.html.j2
        │   └── vhost.conf.j2
        └── vars/
            └── main.yml
```
