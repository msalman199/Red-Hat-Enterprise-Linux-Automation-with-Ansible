# 🎯 Configuring Web Servers with Ansible

## 📋 Objectives

By the end of this lab, you will be able to:

- Understand the fundamentals of Ansible automation for web server configuration
- Write and execute Ansible playbooks to install and configure Apache web server
- Ensure web services are properly enabled and running using Ansible
- Deploy custom HTML content to web servers using automation
- Implement best practices for infrastructure as code using Ansible
- Troubleshoot common issues in Ansible playbook execution

---

## 💻 Prerequisites

Before starting this lab, you should have:

- Basic understanding of Linux command line operations
- Familiarity with YAML syntax and structure
- Basic knowledge of web servers and HTTP protocol
- Understanding of SSH key-based authentication
- Access to a text editor (nano, vim, or similar)

> 💡 **Note:** Al Nafi provides ready-to-use Linux-based cloud machines for this lab.

---

## 🛠️ Lab Environment Setup

Your lab environment includes:

- **Control Node:** CentOS/RHEL 8 machine with Ansible pre-installed
- **Managed Nodes:** Two CentOS/RHEL 8 machines
- SSH connectivity pre-configured
- Sudo privileges on all systems

---

## 📂 Project Structure

```text
ansible-webserver-lab/
├── inventory/
│   └── hosts.ini
├── playbooks/
│   ├── install-apache.yml
│   ├── deploy-website.yml
│   └── complete-webserver-setup.yml
├── templates/
│   └── index.html.j2
└── files/
    └── style.css
```

---

## 🚀 Task 1: Setting Up Ansible Inventory and Basic Configuration

### Verify Ansible Installation

```bash
ansible --version
ansible-config view
```

---

### Create Project Directory

```bash
mkdir ~/ansible-webserver-lab
cd ~/ansible-webserver-lab

mkdir playbooks
mkdir inventory
mkdir templates
mkdir files
```

---

### Configure Inventory

Create inventory file:

```bash
nano inventory/hosts.ini
```

Add:

```ini
[webservers]
web1 ansible_host=192.168.1.10 ansible_user=ec2-user
web2 ansible_host=192.168.1.11 ansible_user=ec2-user

[webservers:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

---

### Test Connectivity

```bash
ansible -i inventory/hosts.ini all -m ping
ansible -i inventory/hosts.ini webservers -m ping
```

---

## 🚀 Task 2: Install and Configure Apache

Create playbook:

```bash
nano playbooks/install-apache.yml
```

Add:

```yaml
---
- name: Install and Configure Apache Web Server
  hosts: webservers
  become: yes

  vars:
    apache_package: httpd
    apache_service: httpd
    document_root: /var/www/html

  tasks:

    - name: Update packages
      yum:
        name: '*'
        state: latest
        update_cache: yes

    - name: Install Apache
      yum:
        name: "{{ apache_package }}"
        state: present

    - name: Install additional packages
      yum:
        name:
          - wget
          - curl
          - vim
        state: present

    - name: Configure Apache
      copy:
        content: |
          ServerRoot /etc/httpd
          Listen 80
          DocumentRoot {{ document_root }}
        dest: /etc/httpd/conf/httpd.conf
        backup: yes
      notify: restart apache

    - name: Set permissions
      file:
        path: "{{ document_root }}"
        state: directory
        owner: apache
        group: apache
        mode: '0755'

    - name: Configure firewall
      firewalld:
        service: http
        permanent: yes
        state: enabled
        immediate: yes

    - name: Start and enable Apache
      systemd:
        name: "{{ apache_service }}"
        state: started
        enabled: yes

    - name: Verify Apache
      systemd:
        name: "{{ apache_service }}"
        state: started
      register: apache_status

    - name: Display status
      debug:
        msg: "Apache service is {{ apache_status.status.ActiveState }}"

    - name: Check port 80
      wait_for:
        port: 80
        host: "{{ ansible_default_ipv4.address }}"
        timeout: 30

  handlers:

    - name: restart apache
      systemd:
        name: "{{ apache_service }}"
        state: restarted
        enabled: yes
```

---

### Execute Playbook

```bash
ansible-playbook -i inventory/hosts.ini playbooks/install-apache.yml
```

Dry run:

```bash
ansible-playbook -i inventory/hosts.ini playbooks/install-apache.yml --check
```

---

## 🚀 Task 3: Deploy Website Content

### Create HTML Template

```bash
nano templates/index.html.j2
```

Add:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to {{ inventory_hostname }}</title>

    <link rel="stylesheet" href="style.css">
</head>

<body>

<div class="container">

<h1>Welcome to {{ inventory_hostname }}</h1>

<div class="info">
    <h3>Server Information</h3>

    <p><strong>Hostname:</strong> {{ inventory_hostname }}</p>
    <p><strong>IP Address:</strong> {{ ansible_default_ipv4.address }}</p>
    <p><strong>OS:</strong> {{ ansible_distribution }}</p>
</div>

<p>This server was configured using Ansible automation.</p>

</div>

</body>
</html>
```

---

### Create CSS File

```bash
nano files/style.css
```

Add:

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    padding: 20px;
}

.container {
    background: white;
    padding: 30px;
    border-radius: 10px;
}

h1 {
    color: #2196F3;
}

.info {
    background: #e7f3ff;
    padding: 15px;
}
```

---

### Create Deployment Playbook

```bash
nano playbooks/deploy-website.yml
```

Add:

```yaml
---
- name: Deploy Website Content
  hosts: webservers
  become: yes

  vars:
    document_root: /var/www/html

  tasks:

    - name: Deploy index page
      template:
        src: ../templates/index.html.j2
        dest: "{{ document_root }}/index.html"
        owner: apache
        group: apache
        mode: '0644'

    - name: Deploy CSS
      copy:
        src: ../files/style.css
        dest: "{{ document_root }}/style.css"
        owner: apache
        group: apache
        mode: '0644'

    - name: Create about page
      copy:
        content: |
          <html>
          <head>
              <title>About</title>
          </head>
          <body>

          <h1>About {{ inventory_hostname }}</h1>

          <p>Configured using Ansible</p>

          </body>
          </html>
        dest: "{{ document_root }}/about.html"

    - name: Verify website
      uri:
        url: "http://{{ ansible_default_ipv4.address }}"
        method: GET
        status_code: 200
      register: web_check

    - name: Display result
      debug:
        msg: "Website is accessible. Status: {{ web_check.status }}"

  handlers:

    - name: reload apache
      systemd:
        name: httpd
        state: reloaded
```

---

### Deploy Website

```bash
ansible-playbook -i inventory/hosts.ini playbooks/deploy-website.yml
```

---

## 🚀 Task 4: Complete Deployment Playbook

Create:

```bash
nano playbooks/complete-webserver-setup.yml
```

Add:

```yaml
---
- name: Complete Web Server Setup
  hosts: webservers
  become: yes

  vars:
    apache_package: httpd
    apache_service: httpd
    document_root: /var/www/html

  tasks:

    - name: Install Apache
      yum:
        name:
          - "{{ apache_package }}"
          - firewalld
          - wget
          - curl
        state: present

    - name: Start Apache
      systemd:
        name: "{{ apache_service }}"
        state: started
        enabled: yes

    - name: Start Firewall
      systemd:
        name: firewalld
        state: started
        enabled: yes

    - name: Open HTTP Port
      firewalld:
        service: http
        permanent: yes
        state: enabled
        immediate: yes

    - name: Create document root
      file:
        path: "{{ document_root }}"
        state: directory
        owner: apache
        group: apache
        mode: '0755'

    - name: Deploy HTML page
      template:
        src: ../templates/index.html.j2
        dest: "{{ document_root }}/index.html"
        owner: apache
        group: apache
        mode: '0644'

    - name: Deploy CSS
      copy:
        src: ../files/style.css
        dest: "{{ document_root }}/style.css"
        owner: apache
        group: apache
        mode: '0644'
```

---

## 🏁 Conclusion

By implementing this Infrastructure as Code (IaC) configuration lifecycle, the web infrastructure is fully automated. Handlers drastically reduce unnecessary resource reboots by executing configuration state updates conditionally. Real-time logging assertions and embedded verification methods prevent configuration drift and guarantee multi-node delivery across all environments.
