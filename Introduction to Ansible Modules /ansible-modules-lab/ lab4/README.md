# Introduction to Ansible Modules

A comprehensive, step-by-step hands-on lab manual for exploring, understanding, and implementing core Ansible modules. This guide covers cross-platform package administration (`yum` and `apt`), state-driven process management via the `service` module, condition-based execution, defensive block handlers, and modular infrastructure orchestration.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Understand the core architecture of idempotent Ansible modules and their purpose in automation.
* Use common Ansible modules including `yum`, `apt`, and `service` to declare target system states.
* Write cross-platform Ansible tasks that abstract underlying operating system differences.
* Create and run complete infrastructure playbooks that automate package installation and service lifetimes.
* Troubleshoot common issues, package locks, and platform conflicts when working with modules.
* Apply operational best practices for module parameters in production environments.

---

## 🧰 Core Modules Reference Guide
The following table outlines the foundational automation modules utilized throughout this lab:


| Module Name | Focus Area | Primary Purpose in this Lab | Common Use Case Example |
| :--- | :--- | :--- | :--- |
| **`yum`** | Red Hat Package Management | Installs, upgrades, or removes packages on RHEL/CentOS systems. | `yum: name=git state=present` |
| **`apt`** | Debian Package Management | Updates repository caches and manages packages on Ubuntu systems. | `apt: update_cache=yes` |
| **`package`** | Abstract Package Manager | Acts as a universal wrapper calling the appropriate platform manager. | `package: name=httpd state=latest` |
| **`service`** | Init System Orchestration | Coordinates systemd or sysvinit services (start, stop, reload, enable). | `service: name=sshd state=started` |
| **`debug`** | Diagnostics Engine | Prints custom variables, evaluation structures, or strings onto stdout. | `debug: msg="{{ service_status }}"` |

---

## 💻 Lab Environment & Prerequisites

### Prerequisites
* Basic understanding of Linux command line operations.
* Familiarity with YAML syntax rules, spacing, and key-value structure.
* Completion of previous Ansible labs covering inventory setup and basic playbook execution.
* Basic knowledge of package managers (`yum`/`dnf` for Red Hat, `apt` for Debian systems).
* General understanding of Linux services and the `systemd` daemon.

### Environment Specs
This architecture lab manual runs across a pre-authenticated multi-distribution network:
* **Control Node:** Dedicated Red Hat/CentOS-based master engine with Ansible pre-installed.
* **Managed Node 1:** Target host platform running a Red Hat/CentOS-based architecture.
* **Managed Node 2:** Target host platform running a Debian/Ubuntu-based architecture.
* **Connectivity:** SSH asymmetric keys are pre-loaded to facilitate zero-prompt terminal execution.

---

## 🚀 Lab Implementation Steps

### Task 1: Understanding Ansible Modules

#### Subtask 1.1: Explore Available Modules
Interrogate your management engine's local documentation definitions to inspect library flags:

```bash
# Verify core application status and version parameters
ansible --version

# Sample the top 20 lines of all locally indexable module utilities
ansible-doc -l | head -20

# Extract interactive manual configurations and code layout schemas
ansible-doc yum
ansible-doc apt
ansible-doc service
```

#### Subtask 1.2: Verify Your Inventory
Audit your target host layouts to confirm the network execution environment is healthy:

```bash
# Read the active system hosts mapping file
cat /etc/ansible/hosts

# Dispatch a baseline ad-hoc ping loop check across all inventory boundaries
ansible all -m ping
```

---

### Task 2: Working with Package Management Modules

#### Subtask 2.1: Using the YUM Module
Isolate enterprise package management loops targeting Red Hat distribution families exclusively:

```bash
# Provision your specialized workspace subfolder structures
mkdir -p ~/ansible-labs/lab4
cd ~/ansible-labs/lab4

# Open a fresh file profile to capture your YUM playbook parameters
nano package-management.yml
```

Add the following declarative package properties to the file:
```yaml
---
- name: Package Management with YUM Module
  hosts: centos_nodes
  become: yes
  tasks:
    - name: Install git package
      yum:
        name: git
        state: present
    
    - name: Install multiple packages
      yum:
        name:
          - wget
          - curl
          - vim
        state: present
    
    - name: Update all packages
      yum:
        name: "*"
        state: latest
        update_cache: yes
    
    - name: Remove a specific package
      yum:
        name: telnet
        state: absent
```

```bash
# Run the playbook to execute package management tasks
ansible-playbook package-management.yml
```

#### Subtask 2.2: Using the APT Module
Construct a parallel configuration script focused on managing Debian-family dependencies:

```bash
# Open an independent deployment structure container
nano apt-management.yml
```

Add the following custom APT tasks into your configuration layout:
```yaml
---
- name: Package Management with APT Module
  hosts: ubuntu_nodes
  become: yes
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install git package
      apt:
        name: git
        state: present
    
    - name: Install multiple packages
      apt:
        name:
          - wget
          - curl
          - vim
          - htop
        state: present
    
    - name: Upgrade all packages
      apt:
        upgrade: dist
        update_cache: yes
    
    - name: Remove unnecessary packages
      apt:
        autoremove: yes
    
    - name: Remove a specific package
      apt:
        name: nano
        state: absent
        purge: yes
```

```bash
# Execute the APT playbook
ansible-playbook apt-management.yml
```

#### Subtask 2.3: Cross-Platform Package Management
Leverage environmental context indicators (`ansible_os_family`) to construct a single, cross-platform deployment codebase:

```bash
# Initialize a universal configuration layout sheet
nano universal-packages.yml
```

Add the cross-platform conditional processing rules below:
```yaml
---
- name: Universal Package Management
  hosts: all
  become: yes
  tasks:
    - name: Install git on Red Hat family
      yum:
        name: git
        state: present
      when: ansible_os_family == "RedHat"
    
    - name: Install git on Debian family
      apt:
        name: git
        state: present
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: Install development tools on Red Hat family
      yum:
        name:
          - gcc
          - make
          - kernel-devel
        state: present
      when: ansible_os_family == "RedHat"
    
    - name: Install development tools on Debian family
      apt:
        name:
          - build-essential
          - linux-headers-generic
        state: present
      when: ansible_os_family == "Debian"
```

```bash
# Run the universal playbook across all network nodes
ansible-playbook universal-packages.yml
```

---

### Task 3: Managing Services with the Service Module

#### Subtask 3.1: Basic Service Management
Combine dynamic inline Jinja2 evaluations to orchestrate service daemons across different distributions:

```bash
# Open a service tracking configuration file
nano service-management.yml
```

Add the following basic service management tasks to the layout:
```yaml
---
- name: Service Management with Service Module
  hosts: all
  become: yes
  tasks:
    - name: Install httpd/apache2 based on OS family
      package:
        name: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"
        state: present
    
    - name: Start and enable web service
      service:
        name: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"
        state: started
        enabled: yes
    
    - name: Check if service is running
      service:
        name: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"
        state: started
      register: service_status
    
    - name: Display service status
      debug:
        msg: "Web service is {{ 'running' if service_status.state == 'started' else 'not running' }}"
```

```bash
# Execute the service management playbook
ansible-playbook service-management.yml
```

#### Subtask 3.2: Advanced Service Operations
Group logical service steps within defensive `block` scopes to manage application targets and system firewalls:

```bash
# Open an advanced service administration layout
nano advanced-services.yml
```

Add the comprehensive multi-service management tasks below:
```yaml
---
- name: Advanced Service Management
  hosts: all
  become: yes
  tasks:
    - name: Install and configure SSH service
      block:
        - name: Ensure SSH is installed
          package:
            name: openssh-server
            state: present
        
        - name: Start SSH service
          service:
            name: "{{ 'ssh' if ansible_os_family == 'Debian' else 'sshd' }}"
            state: started
            enabled: yes
        
        - name: Reload SSH service configuration
          service:
            name: "{{ 'ssh' if ansible_os_family == 'Debian' else 'sshd' }}"
            state: reloaded
    
    - name: Manage firewall service
      block:
        - name: Install firewall on Red Hat family
          yum:
            name: firewalld
            state: present
          when: ansible_os_family == "RedHat"
        
        - name: Start firewall service on Red Hat family
          service:
            name: firewalld
            state: started
            enabled: yes
          when: ansible_os_family == "RedHat"
        
        - name: Install UFW on Debian family
          apt:
            name: ufw
            state: present
          when: ansible_os_family == "Debian"
        
        - name: Enable UFW on Debian family
          service:
            name: ufw
            state: started
            enabled: yes
          when: ansible_os_family == "Debian"
```

```bash
# Run the advanced service playbook
ansible-playbook advanced-services.yml
```

---

### Task 4: Creating a Complete Infrastructure Playbook

#### Subtask 4.1: Combine All Modules
Consolidate package setup tasks, state-driven daemons, and condition evaluations into a single master layout:

```bash
# Open the master orchestration file container
nano infrastructure-setup.yml
```
*(Populate this manifest file by merging your package installations, firewall blocks, and service tracking modules into a unified blueprint to establish a standardized baseline across your multi-OS network).*

---

## 🔍 Verification & Troubleshooting Checklist
Run these verification procedures to confirm your settings match compliance bounds before finishing up:

* [ ] **Core Validation:** Verify ad-hoc connectivity across your multi-OS network by running `ansible all -m ping`.
* [ ] **System Compliance Check:** Run `ansible all -m command -a "git --version"` to verify package installation across all platforms.
* [ ] **Process Status Verification:** Confirm web application server status metrics match expectations on target systems:
  * On RHEL nodes: `systemctl status httpd`
  * On Ubuntu nodes: `systemctl status apache2`

### Common Errors Matrix
* **Error Token: `No package matching 'httpd' found` on Ubuntu nodes**
  * *Root Cause:* Attempting to execute RHEL package naming configurations directly on Debian-based distribution branches.
  * *Remediation:* Utilize the universal `package` module wrapper coupled with inline Jinja2 conditional statement selectors.
* **Error Token: `Failed to lock apt for exclusive operation`**
  * *Root Cause:* Background system maintenance engines (like unattended-upgrades) are locking the package manager socket.
  * *Remediation:* Add a `cache_valid_time` parameter or introduce retry logic parameters inside your playbook tasks block.

---

## 🏁 Conclusion
By completing this structural modules lab guide, you have moved from basic configuration scripts to mastering platform-agnostic infrastructure orchestration.

### Key Concepts Mastered:
* **Idempotent Module Logic:** Using declarative state parameters (`present`, `started`, `absent`) instead of raw bash command lines to ensure repeatable target system execution.
* **Abstract System Operations:** Leveraging platform-agnostic tools like the `package` module to automatically map distribution differences under a single command wrapper.
* **Dynamic Fact Ingestion:** Capturing hardware values at runtime (`ansible_os_family`) to guide complex conditional paths smoothly.
* **Structured Failure Containment:** Wrapping system calls inside modular `block` elements to separate configuration tracking from network security layers cleanly.

---

## 📁 Repository Directory File Structure
To organize your playbook files and maintain clean source boundaries, implement the following repository structure inside your workspace folder:

```text
📁 ansible-modules-lab/
└── 📁 ansible-labs/
    └── 📁 lab4/
        ├── 📄 advanced-services.yml     # Service orchestration block handling system firewalls
        ├── 📄 apt-management.yml        # Targeted validation profile tracking Debian package tasks
        ├── 📄 error-handling.yml        # Defensive configuration testing blocks and failure handlers
        ├── 📄 infrastructure-setup.yml  # Comprehensive master production deployment automation sheet
        ├── 📄 package-management.yml    # Targeted deployment file handling YUM repository commands
        ├── 📄 service-management.yml    # State tracking file containing web service checks
        └── 📄 universal-packages.yml    # Platform-agnostic execution script with condition maps
```
