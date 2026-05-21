# Understanding Playbooks

A comprehensive, step-by-step hands-on lab manual for understanding the architecture, components, and implementation of Ansible playbooks. This guide covers YAML syntax validation, variable scopes, conditional handlers, templates, and execution workflows.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Understand the basic structural organization and components of Ansible playbooks.
* Write operational playbooks to automate package management on managed hosts.
* Define hosts, execute task modules, and implement triggered handlers.
* Execute automated playbooks using the `ansible-playbook` core CLI engine.
* Structure execution workflows via pre-tasks, core tasks, post-tasks, and tags.
* Leverage Jinja2 dynamic templates (`.j2`) to build customized deployment configurations.

---

## 🧰 Tools & Modules Matrix
The following table outlines the foundational system engines and automation modules used throughout this lab:



| Tool / Module Name | Type | Primary Purpose in this Lab | Common Use Case Example |
| :--- | :--- | :--- | :--- |
| `ansible-playbook` | Engine CLI | Executes declarative task lists defined in `.yml` files against targets. | `ansible-playbook -i ...` |
| `yum` | Module | Manages operating system software packages on Red Hat-based targets. | `yum: name=httpd state=present` |
| `service` / `firewalld` | Module | Controls systemd runtime daemons and configures active firewall metrics. | `service: state=started` |
| `copy` / `template` | Module | Transports flat text files or parses dynamic Jinja2 markup configurations. | `template: src=index.html.j2` |
| `uri` | Module | Interrogates HTTP endpoints directly to validate connection headers. | `uri: method=GET status_code=200` |
| `debug` | Module | Prints user-defined diagnostic strings or facts onto the standard output. | `debug: msg="Task complete"` |

---

## 💻 Lab Environment & Prerequisites

### Prerequisites
* Basic understanding of Linux terminal control operations.
* Familiarity with the indentation rule sets of YAML markup formats.
* Completion of basic control node initialization or equivalent knowledge.
* Functional knowledge of SSH key-based authentication paths and package managers.

### Environment Specs
This lab runs within a pre-configured automation network topology:
* **Control Node:** CentOS / RHEL 8 master machine containing Ansible.
* **Managed Nodes:** Multi-tiered target execution host targets (`node1`, `node2`).
* **Connectivity:** SSH asymmetric keys pre-authenticated between nodes.

---

## 🚀 Lab Implementation Steps

### Task 1: Understanding Playbook Structure and Creating Your First Playbook

#### Subtask 1.1: Explore the Playbook Directory Structure
Establish a clean enterprise workspace hierarchy to maintain deployment variables and roles:

```bash
# Step 1: Access the working directory path
cd /home/ansible

# Step 2: Create isolated project directory nodes
mkdir -p playbooks/lab2
cd playbooks/lab2

# Step 3: Build out corporate standard subdirectories for templates and group vars
mkdir -p {group_vars,host_vars,roles,files,templates}
ls -la
```

#### Subtask 1.2: Create Your First Basic Playbook
Draft a baseline deployment blueprint to handle server configurations and static files:

```bash
# Step 1: Open a fresh file context container using nano
nano install-package.yml
```

Step 2: Append the following declarative execution structure to your `install-package.yml` file:
```yaml
---
- name: Install and configure a package on remote hosts
  hosts: managed_nodes
  become: yes
  gather_facts: yes
  
  vars:
    package_name: httpd
    service_name: httpd
    
  tasks:
    - name: Install the specified package
      yum:
        name: "{{ package_name }}"
        state: present
      notify: start and enable service
      
    - name: Ensure the service is running
      service:
        name: "{{ service_name }}"
        state: started
        enabled: yes
        
    - name: Create a simple index.html file
      copy:
        content: |
          <html>
          <head><title>Ansible Lab 2</title></head>
          <body>
          <h1>Welcome to Ansible Playbook Lab!</h1>
          <p>This page was created by an Ansible playbook.</p>
          </body>
          </html>
        dest: /var/www/html/index.html
        owner: apache
        group: apache
        mode: '0644'
      notify: restart web service
        
  handlers:
    - name: start and enable service
      service:
        name: "{{ service_name }}"
        state: started
        enabled: yes
        
    - name: restart web service
      service:
        name: "{{ service_name }}"
        state: restarted
```
*Step 3: Save and exit the editor panel (`Ctrl+X` -> `Y` -> `Enter`).*

#### Subtask 1.3: Understanding Playbook Components
* **Play Definition:** Binds the declarative block steps to specific `hosts` targets and uses `become: yes` to elevate tasks via sudo.
* **Variables Section (`vars`):** Defines reusable parameters referenceable throughout the block via Jinja2 interpolation braces `{{ var }}`.
* **Tasks Section (`tasks`):** Sequential execution steps. If an active step returns a modified state, it triggers a `notify` hook.
* **Handlers Section (`handlers`):** Specialized trigger routines that execute at the end of a play to reload files or restart daemons.

---

### Task 2: Define Hosts and Create Inventory

#### Subtask 2.1: Create a Custom Inventory File
Map out your target architecture using an INI file definition matrix:

```bash
# Step 1: Open a custom inventory file configuration shell
nano inventory.ini
```

Step 2: Append the group topologies and globally inherited variables below:
```ini
[managed_nodes]
node1 ansible_host=192.168.1.10 ansible_user=ansible
node2 ansible_host=192.168.1.11 ansible_user=ansible

[web_servers]
node1

[database_servers]
node2

[all:vars]
ansible_ssh_private_key_file=/home/ansible/.ssh/id_rsa
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

#### Subtask 2.2: Verify Inventory and Connectivity
Audit your newly created network topology before triggering your configurations:

```bash
# Step 1: View the active grouped structure using formatting flags
ansible-inventory -i inventory.ini --list

# Step 2: Validate ad-hoc module connections across your managed nodes
ansible -i inventory.ini managed_nodes -m ping

# Step 3: Run the fact-gathering setup engine to test context processing
ansible -i inventory.ini managed_nodes -m setup --tree /tmp/facts
```

---

### Task 3: Enhance the Playbook with Advanced Tasks and Handlers

#### Subtask 3.1: Create an Enhanced Playbook
Build an advanced orchestration workflow that handles pre-tasks, metadata loops, and integration testing:

```bash
# Step 1: Open a separate deployment script layout profile
nano enhanced-playbook.yml
```

Step 2: Input the multi-tier task architecture shown below into your file:
```yaml
---
- name: Enhanced package installation and configuration
  hosts: managed_nodes
  become: yes
  gather_facts: yes
  
  vars:
    packages:
      - httpd
      - firewalld
      - wget
    web_port: 80
    document_root: /var/www/html
    
  pre_tasks:
    - name: Update package cache
      yum:
        update_cache: yes
      tags: always
      
  tasks:
    - name: Install required packages
      yum:
        name: "{{ packages }}"
        state: present
      notify:
        - start httpd
        - start firewalld
      tags: packages
      
    - name: Configure firewall for web traffic
      firewalld:
        service: http
        permanent: yes
        state: enabled
        immediate: yes
      notify: reload firewall
      tags: firewall
      
    - name: Create custom web content
      template:
        src: index.html.j2
        dest: "{{ document_root }}/index.html"
        owner: apache
        group: apache
        mode: '0644'
      notify: restart httpd
      tags: content
      
    - name: Ensure web service is running and enabled
      service:
        name: httpd
        state: started
        enabled: yes
      tags: services
      
    - name: Verify web service is responding
      uri:
        url: "http://{{ ansible_default_ipv4.address }}:{{ web_port }}"
        method: GET
        status_code: 200
      delegate_to: localhost
      tags: verification
      
  handlers:
    - name: start httpd
      service:
        name: httpd
        state: started
        enabled: yes
        
    - name: restart httpd
      service:
        name: httpd
        state: restarted
        
    - name: start firewalld
      service:
        name: firewalld
        state: started
        enabled: yes
        
    - name: reload firewall
      service:
        name: firewalld
        state: reloaded
        
  post_tasks:
    - name: Display completion message
      debug:
        msg: "Playbook execution completed successfully on {{ inventory_hostname }}"
```

#### Subtask 3.2: Create a Template File
Develop a dynamic HTML template sheet using system metrics variables:

```bash
# Step 1: Create the templates target structural subfolder path
mkdir -p templates

# Step 2: Open your target Jinja2 template file layout interface
nano templates/index.html.j2
```

Step 3: Inject the responsive layout code parameters directly into the template file:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ inventory_hostname }} - Ansible Lab 2</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .info { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Welcome to {{ inventory_hostname }}</h1>
    <div class="info">
        <h2>System Information</h2>
        <p><strong>Hostname:</strong> {{ ansible_hostname }}</p>
        <p><strong>Operating System:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}</p>
        <p><strong>IP Address:</strong> {{ ansible_default_ipv4.address }}</p>
        <p><strong>Architecture:</strong> {{ ansible_architecture }}</p>
        <p><strong>Memory:</strong> {{ ansible_memtotal_mb }} MB</p>
        <p><strong>Processor:</strong> {{ ansible_processor[2] }}</p>
    </div>
    <p><em>This page was generated by Ansible on {{ ansible_date_time.iso8601 }}</em></p>
</body>
</html>
```

---

## 🏁 Conclusion
By executing this orchestration lab guide, you have transitioned from basic commands to developing robust automation workflows via Ansible playbooks.

### Key Concepts Mastered:
* **Structured Directory Mapping:** Aligning configurations with enterprise layout frameworks (`templates/`, `group_vars/`).
* **State Management via Modules:** Using declarative parameters instead of raw terminal command strings to ensure predictable target execution.
* **Conditional Handlers Optimization:** Minimizing processing overhead by triggering service reloads only when underlying files shift configurations.
* **Context-Aware Templating:** Leveraging Jinja2 modules to extract machine details at runtime, turning static configurations into adaptable code assets.

---

## 📁 Repository Directory File Structure
To maintain your development files and keep them organized, ensure your repository mirrors the following file layout model:

```text
📁 ansible-playbook-lab/
└── 📁 playbooks/
    └── 📁 lab2/
        ├── 📄 enhanced-playbook.yml    # Advanced playbook featuring pre/post-tasks and tags
        ├── 📄 install-package.yml       # Baseline package installation playbook file
        ├── 📄 inventory.ini             # Structured INI file mapping server topologies
        ├── 📁 files/                    # Directory for static flat file tracking
        ├── 📁 group_vars/               # Globally shared network parameters block files
        ├── 📁 host_vars/                # Machine-specific unique context parameters
        ├── 📁 roles/                    # Decoupled component playbook tracking structures
        └── 📁 templates/                # Staging folder for dynamic files
            └── 📄 index.html.j2         # Jinja2 environment metrics welcome page template
```
