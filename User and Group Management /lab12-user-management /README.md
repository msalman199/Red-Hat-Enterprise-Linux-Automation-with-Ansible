# User and Group Management in Ansible

This repository contains the complete materials, playbooks, and structural configurations for **Lab 12: User and Group Management**. This lab guides you through using Ansible modules to safely automate multi-tier Linux system user onboarding, privilege escalation layers, and identity configurations.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Create and manage user accounts safely using the Ansible `user` module.
* Create and manage Linux system access groups using the Ansible `group` module.
* Modify fine-grained user properties including specific execution shells, secondary groups, and home directories.
* Master the explicit relationship between security users and system groups in Linux enterprise environments.
* Write reusable Ansible playbooks for zero-touch automated user provisioning.
* Implement identity and access management (IAM) best practices for multi-node deployments.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A basic understanding of Linux CLI navigation and account operations.
* Familiarity with YAML formatting patterns and indent syntax.
* Core knowledge of foundational Ansible playbook building from previous labs (Labs 1–11).
* Understanding of Linux file system permissions, asset ownership, and security masking masks.
* Access to a standard terminal text editor (`nano`, `vim`, or similar).

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** in your portal to launch your pre-configured virtualization environment instantly.

Your testing architecture contains:
* **Control Node**: A CentOS/RHEL-based instance with Ansible pre-installed.
* **Privilege Level**: Full `root` administrative access pre-seeded for target executions.
* **Pre-baked Toolsets**: All necessary verification utilities and configuration files are ready to use.

---

## 🛠️ Lab Tasks

### Task 1: Create Users and Groups Using Ansible Modules

#### Subtask 1.1: Create a Basic Inventory File
Isolating host connections in an inventory file establishes the routing blueprint for local administrative actions.

1. **Create your project workspace directory and enter it:**
   ```bash
   mkdir ~/lab12-user-management
   cd ~/lab12-user-management
   ```

2. **Generate the network targeting map configuration file:**
   ```bash
   nano inventory.ini
   ```

3. **Incorporate the local connection mapping configurations:**
   ```ini
   [local]
   localhost ansible_connection=local

   [webservers]
   localhost ansible_connection=local
   ```

#### Subtask 1.2: Create Groups Using the Group Module
Groups must be provisioned with designated GIDs before deploying users to ensure valid identity mapping links.

1. **Open a new group provisioning playbook wrapper file:**
   ```bash
   nano create-groups.yml
   ```

2. **Add the structural group parameters directly into the playbook:**
   ```yaml
   ---
   - name: Create Groups for User Management
     hosts: local
     become: yes
     tasks:
       - name: Create developers group
         group:
           name: developers
           state: present
           gid: 3001

       - name: Create testers group
         group:
           name: testers
           state: present
           gid: 3002

       - name: Create managers group
         group:
           name: managers
           state: present
           gid: 3003

       - name: Create contractors group
         group:
           name: contractors
           state: present
           gid: 3004

       - name: Display created groups
         shell: getent group | grep -E "(developers|testers|managers|contractors)"
         register: group_info

       - name: Show group information
         debug:
           msg: "{{ group_info.stdout_lines }}"
   ```

3. **Execute the group orchestration script:**
   ```bash
   ansible-playbook -i inventory.ini create-groups.yml
   ```

4. **Verify that the security entries exist within the system log file:**
   ```bash
   getent group | grep -E "(developers|testers|managers|contractors)"
   ```

#### Subtask 1.3: Create Users Using the User Module
Define specific user parameters like home paths, shell definitions, and unique UIDs to standardize identity layouts.

1. **Open your primary user identity blueprint configuration playbook:**
   ```bash
   nano create-users.yml
   ```

2. **Incorporate the explicit configuration settings mapping:**
   ```yaml
   ---
   - name: Create Users with Different Configurations
     hosts: local
     become: yes
     tasks:
       - name: Create developer user - alice
         user:
           name: alice
           comment: "Alice Johnson - Senior Developer"
           uid: 2001
           group: developers
           groups: developers
           shell: /bin/bash
           home: /home/alice
           create_home: yes
           state: present

       - name: Create developer user - bob
         user:
           name: bob
           comment: "Bob Smith - Junior Developer"
           uid: 2002
           group: developers
           groups: developers
           shell: /bin/bash
           home: /home/bob
           create_home: yes
           state: present

       - name: Create tester user - carol
         user:
           name: carol
           comment: "Carol Davis - QA Tester"
           uid: 2003
           group: testers
           groups: testers
           shell: /bin/bash
           home: /home/carol
           create_home: yes
           state: present

       - name: Create manager user - david
         user:
           name: david
           comment: "David Wilson - Project Manager"
           uid: 2004
           group: managers
           groups: managers,developers,testers
           shell: /bin/bash
           home: /home/david
           create_home: yes
           state: present

       - name: Create contractor user - eve
         user:
           name: eve
           comment: "Eve Brown - External Contractor"
           uid: 2005
           group: contractors
           groups: contractors
           shell: /bin/sh
           home: /home/eve
           create_home: yes
           state: present

       - name: Display created users
         shell: getent passwd | grep -E "(alice|bob|carol|david|eve)"
         register: user_info

       - name: Show user information
         debug:
           msg: "{{ user_info.stdout_lines }}"
   ```

3. **Deploy the user profiles onto your target nodes:**
   ```bash
   ansible-playbook -i inventory.ini create-users.yml
   ```

4. **Run a targeted status inspection on the generated profiles:**
   ```bash
   getent passwd | grep -E "(alice|bob|carol|david|eve)"
   ```

---

### Task 2: Modify Users' Shell, Groups, and Home Directories

#### Subtask 2.1: Modify User Shells
Use task logic to update runtime environments and shell properties for individual user groups.

1. **Open the system shell modifications workbook file:**
   ```bash
   nano modify-shells.yml
   ```

2. **Add the installation and fallback task steps into the playbook configuration:**
   ```yaml
   ---
   - name: Modify User Shells
     hosts: local
     become: yes
     tasks:
       - name: Change alice's shell to zsh (if available)
         user:
           name: alice
           shell: /bin/zsh
         ignore_errors: yes

       - name: Fallback - Change alice's shell to bash if zsh not available
         user:
           name: alice
           shell: /bin/bash
         when: ansible_failed_result is defined

       - name: Change eve's shell to restricted shell
         user:
           name: eve
           shell: /bin/sh

       - name: Change bob's shell to bash (confirm it's bash)
         user:
           name: bob
           shell: /bin/bash

       - name: Install zsh if not present
         package:
           name: zsh
           state: present
         ignore_errors: yes

       - name: Change alice's shell to zsh after installation
         user:
           name: alice
           shell: /bin/zsh

       - name: Display current shell information for all users
         shell: getent passwd | grep -E "(alice|bob|carol|david|eve)" | cut -d: -f1,7
         register: shell_info

       - name: Show shell information
         debug:
           msg: "User shells: {{ shell_info.stdout_lines }}"
   ```

3. **Run your shell configuration playbook updates:**
   ```bash
   ansible-playbook -i inventory.ini modify-shells.yml
   ```

#### Subtask 2.2: Modify User Group Memberships
Update user memberships to reflect role changes using the `append` parameter flag to prevent overwriting existing permissions.

1. **Open the primary group assignment adjustments playbook file:**
   ```bash
   nano modify-groups.yml
   ```

2. **Add the cross-functional group tracking configurations into the playbook:**
   ```yaml
   ---
   - name: Modify User Group Memberships
     hosts: local
     become: yes
     tasks:
       - name: Add alice to testers group (cross-functional role)
         user:
           name: alice
           groups: developers,testers
           append: yes

       - name: Add bob to a temporary project group
         group:
           name: project-alpha
           state: present
           gid: 3005

       - name: Add bob to project-alpha group
         user:
           name: bob
           groups: developers,project-alpha
           append: yes

       - name: Remove eve from contractors and add to developers (conversion)
         user:
           name: eve
           groups: developers
           append: no

       - name: Create a special admin group
         group:
           name: sysadmins
           state: present
           gid: 3006

       - name: Add david to sysadmins group
         user:
           name: david
           groups: managers,developers,testers,sysadmins
           append: no

       - name: Display group memberships
         shell: |
           for user in alice bob carol david eve; do
             echo "User $user groups: \$(groups \$user)"
          done
         register: group_memberships

       - name: Show group membership information
         debug:
           msg: "{{ group_memberships.stdout_lines }}"
   ```

3. **Run the group tracking configuration changes live:**
   ```bash
   ansible-playbook -i inventory.ini modify-groups.yml
   ```

---

### 📁 File Structure
At the conclusion of this lab, your user management directory tree layout will match this hierarchy:

```text
~/lab12-user-management/
├── create-groups.yml           # Playbook for system group declarations and GID maps
├── create-users.yml            # Playbook managing complete core user profile creation
├── inventory.ini               # Local staging host tracking inventory environment mapping
├── modify-groups.yml           # Playbook managing membership changes and append validations
└── modify-shells.yml           # Playbook handling custom system tool overrides and shells
```

---

## 🏁 Conclusion
In this lab, you successfully built out a complete corporate identity framework. By completing these tasks, you have mastered:
* **Role Separation**: Creating targeted groups and unique GID ranges to enforce crisp access boundaries across teams.
* **Dynamic Adjustments**: Managing multi-group changes safely by configuring the `append` keyword properly to protect secondary system privileges.
* **Environment Configuration**: Tailoring individual user runtime states by handling conditional shells and verifying installations smoothly.
