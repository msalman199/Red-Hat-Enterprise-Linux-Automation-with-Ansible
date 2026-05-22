# Automating Software Packages

This repository contains the complete materials, playbooks, and structural templates for **Lab 11: Automating Software Packages**. This lab guides you through using Ansible to efficiently orchestrate multi-tier application dependency deployments across mixed Linux environments.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Create Ansible playbooks to automate software package installation across multiple target systems.
* Use cross-platform package management modules (`yum`/`dnf` and `apt`) to seamlessly install, update, and remove packages.
* Manage complex external package repositories and downstream dependencies.
* Implement conditional blocks to target specific operating system distributions.
* Configure precise package rules using targeted version constraints and desired state boundaries.
* Troubleshoot and fix common package execution errors, caching failures, or locking issues.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A basic understanding of Linux CLI structures and system administration tasks.
* Familiarity with package managers (`yum`/`dnf` for RHEL ecosystems, `apt` for Debian-based nodes).
* Completion of previous Ansible labs covering inventory workflows and basic playbook construction (Labs 1–10).
* Sound understanding of YAML syntax, indentation rules, and core variable nesting.
* Knowledge of SSH configuration parameters and shared key validation behaviors.

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** inside your lab interface to spawn your active testing sandbox environment automatically.

Your infrastructure perimeter includes:
* **1 Ansible Control Node**: Management node running CentOS/RHEL 8 or Ubuntu 20.04 (Ansible pre-configured).
* **3 Managed Target Nodes**: Two CentOS/RHEL nodes and one Ubuntu server instance.
* **Network & Access**: Active internal connectivity with pre-authorized user SSH mappings.

---

## 🛠️ Lab Tasks

### Task 1: Creating Basic Package Installation Playbooks

#### Subtask 1.1: Setting Up the Lab Directory Structure
Establishing organized workspaces allows you to handle cross-platform workflows without mixing configurations.

1. **Connect to your control node and build the project core:**
   ```bash
   mkdir -p ~/ansible-lab11/playbooks
   mkdir -p ~/ansible-lab11/inventory
   cd ~/ansible-lab11
   ```

2. **Generate the multi-tier platform targeting inventory definitions map:**
   ```bash
   cat > inventory/hosts << EOF
   [rhel_servers]
   node1 ansible_host=10.0.1.10
   node2 ansible_host=10.0.1.11

   [ubuntu_servers]
   node3 ansible_host=10.0.1.12

   [all_servers:children]
   rhel_servers
   ubuntu_servers

   [all_servers:vars]
   ansible_user=ansible
   ansible_ssh_private_key_file=~/.ssh/id_rsa
   EOF
   ```

3. **Verify infrastructure routing and connectivity flags:**
   ```bash
   ansible all -i inventory/hosts -m ping
   ```

#### Subtask 1.2: Creating Your First Package Installation Playbook
Use distribution checks to guide installations to the proper platform module.

1. **Build a core package checklist implementation blueprint playbook:**
   ```bash
   cat > playbooks/install-basic-packages.yml << 'EOF'
   ---
   - name: Install Basic Software Packages
     hosts: all_servers
     become: yes
     vars:
       common_packages:
         - git
         - curl
         - wget
         - vim
         - htop
     
     tasks:
       - name: Install packages on Red Hat-based systems
         yum:
           name: "{{ common_packages }}"
           state: present
         when: ansible_os_family == "RedHat"
       
       - name: Install packages on Debian-based systems
         apt:
           name: "{{ common_packages }}"
           state: present
           update_cache: yes
         when: ansible_os_family == "Debian"
       
       - name: Verify git installation
         command: git --version
         register: git_version
         changed_when: false
       
       - name: Display git version
         debug:
           msg: "Git version installed: {{ git_version.stdout }}"
   EOF
   ```

2. **Run your baseline installation playbook across all targeted hosts:**
   ```bash
   ansible-playbook -i inventory/hosts playbooks/install-basic-packages.yml
   ```

3. **Validate correct destination paths on remote targets:**
   ```bash
   ansible all -i inventory/hosts -m command -a "which git" --become
   ```

#### Subtask 1.3: Advanced Package Management with Specific Versions
Learn to declare distinct system properties and cleanly remove unneeded applications.

1. **Build the advanced installation configuration playbook file:**
   ```bash
   cat > playbooks/advanced-package-management.yml << 'EOF'
   ---
   - name: Advanced Package Management
     hosts: all_servers
     become: yes
     vars:
       development_packages:
         rhel:
           - name: python3
             state: present
           - name: python3-pip
             state: present
           - name: nodejs
             state: present
           - name: npm
             state: present
         ubuntu:
           - name: python3
             state: present
           - name: python3-pip
             state: present
           - name: nodejs
             state: present
           - name: npm
             state: present
       
       packages_to_remove:
         - telnet
         - rsh
     
     tasks:
       - name: Install development packages on Red Hat systems
         yum:
           name: "{{ item.name }}"
           state: "{{ item.state }}"
         loop: "{{ development_packages.rhel }}"
         when: ansible_os_family == "RedHat"
       
       - name: Install development packages on Ubuntu systems
         apt:
           name: "{{ item.name }}"
           state: "{{ item.state }}"
           update_cache: yes
         loop: "{{ development_packages.ubuntu }}"
         when: ansible_os_family == "Debian"
       
       - name: Remove insecure packages from Red Hat systems
         yum:
           name: "{{ packages_to_remove }}"
           state: absent
         when: ansible_os_family == "RedHat"
       
       - name: Remove insecure packages from Ubuntu systems
         apt:
           name: "{{ packages_to_remove }}"
           state: absent
         when: ansible_os_family == "Debian"
       
       - name: Check Python version
         command: python3 --version
         register: python_version
         changed_when: false
       
       - name: Display Python version
         debug:
           msg: "Python version: {{ python_version.stdout }}"
   EOF
   ```

2. **Run your advanced package deployment playbook:**
   ```bash
   ansible-playbook -i inventory/hosts playbooks/advanced-package-management.yml
   ```

---

### Task 2: Using yum/apt to Manage Packages on Multiple Remote Hosts

#### Subtask 2.1: Creating OS-Specific Package Management Playbooks
Isolating complex workflows into dedicated files prevents execution clutter when configuring platform-specific options like EPEL repositories or custom mirror definitions.

1. **Build the Red Hat system administration deployment configuration playbook:**
   ```bash
   cat > playbooks/rhel-package-management.yml << 'EOF'
   ---
   - name: Red Hat Package Management
     hosts: rhel_servers
     become: yes
     vars:
       rhel_packages:
         - epel-release
         - yum-utils
         - device-mapper-persistent-data
         - lvm2
         - tree
         - net-tools
         - bind-utils
     
     tasks:
       - name: Update all packages to latest version
         yum:
           name: '*'
           state: latest
           update_cache: yes
         tags: update
       
       - name: Install EPEL repository
         yum:
           name: epel-release
           state: present
       
       - name: Install system administration packages
         yum:
           name: "{{ rhel_packages }}"
           state: present
       
       - name: Install packages from EPEL repository
         yum:
           name:
             - htop
             - ncdu
             - iotop
           state: present
       
       - name: Check if Docker repository exists
         stat:
           path: /etc/yum.repos.d/docker-ce.repo
         register: docker_repo
       
       - name: Add Docker CE repository
         yum_repository:
           name: docker-ce-stable
           description: Docker CE Stable - $basearch
           baseurl: https://download.docker.com/linux/centos/8/$basearch/stable
           gpgcheck: yes
           gpgkey: https://download.docker.com/linux/centos/gpg
           enabled: yes
         when: not docker_repo.stat.exists
       
       - name: Install Docker CE
         yum:
           name:
             - docker-ce
             - docker-ce-cli
             - containerd.io
           state: present
       
       - name: Start and enable Docker service
         systemd:
           name: docker
           state: started
           enabled: yes
       
       - name: Verify installed packages
         command: rpm -qa | grep -E "(docker|epel|htop)"
         register: installed_packages
         changed_when: false
       
       - name: Display installed packages
         debug:
           msg: "Installed packages: {{ installed_packages.stdout_lines }}"
   EOF
   ```

2. **Build the corresponding Debian/Ubuntu deployment configuration playbook:**
   ```bash
   cat > playbooks/ubuntu-package-management.yml << 'EOF'
   ---
   - name: Ubuntu Package Management
     hosts: ubuntu_servers
     become: yes
     vars:
       ubuntu_packages:
         - software-properties-common
         - apt-transport-https
         - ca-certificates
         - gnupg
         - lsb-release
         - tree
   
     tasks:
       - name: Update apt cache and upgrade system packages
         apt:
           upgrade: dist
           update_cache: yes
         tags: update

       - name: Install supporting administration packages
         apt:
           name: "{{ ubuntu_packages }}"
           state: present
   EOF
   ```

---

### 📁 File Structure
At the conclusion of this lab, your repository layout should match this directory mapping:

```text
~/ansible-lab11/
├── inventory/
│   └── hosts                           # Environment endpoint topology mappings file
└── playbooks/
    ├── advanced-package-management.yml # Playbook for specific versions and removal tasks
    ├── install-basic-packages.yml      # Multi-platform basic package setup playbook
    ├── rhel-package-management.yml     # Custom repository and Docker setup on Red Hat
    └── ubuntu-package-management.yml   # APT cache and dist upgrades on Ubuntu systems
```
