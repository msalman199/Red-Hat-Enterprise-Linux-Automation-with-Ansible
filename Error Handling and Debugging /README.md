# 🛠️ Error Handling and Debugging in Ansible

## 📌 Overview
This lab demonstrates how to implement debugging and error handling techniques in Ansible automation workflows. You will learn how to troubleshoot playbooks, perform dry runs, handle failures gracefully, and apply best practices for resilient automation.

---

# 🎯 Objectives

By the end of this lab, you will be able to:

- ✅ Use the `debug` module for troubleshooting
- ✅ Perform dry runs using `--check`
- ✅ Use `ignore_errors` effectively
- ✅ Implement `block`, `rescue`, and `always`
- ✅ Troubleshoot common Ansible errors
- ✅ Apply debugging best practices

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

- 🧠 Basic YAML knowledge
- 🧠 Understanding of Ansible playbooks
- 🧠 Familiarity with Linux command line
- 🧠 Experience running Ansible commands

---

# 🖥️ Lab Environment

The lab environment includes:

- 🛠️ Ansible Control Node
- 🖥️ Two Managed Nodes
- 🔐 Preconfigured SSH Access
- 📂 Inventory Files Ready

---

# 📁 Task 1: Using Debug Module

---

## 🔹 Subtask 1.1: Create Basic Debug Playbook

### 🛠️ Step 1: Create Lab Directory

```bash
mkdir -p ~/lab19-error-handling
cd ~/lab19-error-handling
```

---

### 🛠️ Step 2: Create Inventory File

```bash
cat > inventory << EOF
[webservers]
node1 ansible_host=192.168.1.10
node2 ansible_host=192.168.1.11

[all:vars]
ansible_user=ansible
ansible_ssh_private_key_file=~/.ssh/id_rsa
EOF
```

---

### 🛠️ Step 3: Create Debug Playbook

```yaml
cat > debug-variables.yml << 'EOF'
---
- name: Debug Module Demonstration
  hosts: webservers
  gather_facts: yes

  vars:
    app_name: "MyWebApp"
    app_version: "2.1.0"
    environment: "production"

  tasks:

    - name: Debug simple variable
      debug:
        msg: "Application Name: {{ app_name }}"

    - name: Debug formatted output
      debug:
        msg: "Running {{ app_name }} version {{ app_version }}"

    - name: Display OS information
      debug:
        msg: "{{ ansible_distribution }} {{ ansible_distribution_version }}"
EOF
```

---

### 🛠️ Step 4: Run Playbook

```bash
ansible-playbook -i inventory debug-variables.yml
```

---

# 🚀 Subtask 1.2: Advanced Debugging

---

### 🛠️ Step 1: Create Advanced Debug Playbook

```yaml
cat > advanced-debug.yml << 'EOF'
---
- name: Advanced Debugging
  hosts: webservers
  gather_facts: yes

  vars:
    users:
      - name: alice
        role: admin
      - name: bob
        role: developer

  tasks:

    - name: Debug loop output
      debug:
        msg: "User {{ item.name }} has role {{ item.role }}"
      loop: "{{ users }}"

    - name: Show variable type
      debug:
        msg: "Variable type: {{ users | type_debug }}"

    - name: Verbosity example
      debug:
        msg: "Visible only with -v"
        verbosity: 1
EOF
```

---

### 🛠️ Step 2: Run Playbook Normally

```bash
ansible-playbook -i inventory advanced-debug.yml
```

---

### 🛠️ Step 3: Run with Verbose Output

```bash
ansible-playbook -i inventory advanced-debug.yml -v
```

---

# 🧪 Task 2: Using Check Mode

---

## 🔹 Subtask 2.1: Create Check Mode Playbook

### 🛠️ Step 1: Create System Changes Playbook

```yaml
cat > system-changes.yml << 'EOF'
---
- name: System Changes
  hosts: webservers
  become: yes

  tasks:

    - name: Install packages
      yum:
        name:
          - htop
          - curl
        state: present

    - name: Create application directory
      file:
        path: /opt/myapp
        state: directory
        mode: '0755'

    - name: Create config file
      copy:
        content: "Application Configurations"
        dest: /opt/myapp/config.conf
EOF
```

---

## 🔹 Subtask 2.2: Run in Check Mode

### 🛠️ Step 1: Dry Run Playbook

```bash
ansible-playbook -i inventory system-changes.yml --check
```

---

### 🛠️ Step 2: Run with Diff

```bash
ansible-playbook -i inventory system-changes.yml --check --diff
```

---

# 🛡️ Task 3: Error Handling

---

## 🔹 Subtask 3.1: Using ignore_errors

### 🛠️ Step 1: Create Error Handling Playbook

```yaml
cat > basic-error-handling.yml << 'EOF'
---
- name: Basic Error Handling
  hosts: webservers
  become: yes

  tasks:

    - name: Command that fails
      command: /bin/false
      ignore_errors: yes
      register: failed_result

    - name: Show failure result
      debug:
        msg: "Return code: {{ failed_result.rc }}"

    - name: Continue execution
      debug:
        msg: "Playbook continued successfully"
EOF
```

---

### 🛠️ Step 2: Run Playbook

```bash
ansible-playbook -i inventory basic-error-handling.yml
```

---

# 🧱 Subtask 3.2: Block, Rescue, Always

---

### 🛠️ Step 1: Create Advanced Error Handling Playbook

```yaml
cat > advanced-error-handling.yml << 'EOF'
---
- name: Advanced Error Handling
  hosts: webservers
  become: yes

  tasks:

    - name: Web Server Deployment
      block:

        - name: Install Apache
          yum:
            name: httpd
            state: present

        - name: Start Apache
          systemd:
            name: httpd
            state: started

      rescue:

        - name: Rescue Message
          debug:
            msg: "Apache setup failed"

      always:

        - name: Always Run
          debug:
            msg: "This task always executes"
EOF
```

---

### 🛠️ Step 2: Run Playbook

```bash
ansible-playbook -i inventory advanced-error-handling.yml
```

---

# 🔄 Subtask 3.3: Best Practices

---

## ✅ Recommended Practices

| 🛠️ Technique | 📌 Purpose |
|---|---|
| `debug` | Troubleshooting |
| `--check` | Dry Run Validation |
| `ignore_errors` | Continue After Failure |
| `block/rescue` | Structured Error Handling |
| `always` | Cleanup Tasks |
| `register` | Store Command Results |
| `retries` | Retry Failed Tasks |

---

# 🧾 Verification Playbook

---

### 🛠️ Step 1: Create Verification File

```yaml
cat > verify-lab-completion.yml << 'EOF'
---
- name: Verify Lab 19
  hosts: webservers

  tasks:

    - name: Debug verification
      debug:
        msg: "Debug module works"

    - name: Check mode verification
      debug:
        msg: "Check mode: {{ ansible_check_mode }}"

    - name: Error handling verification
      block:

        - name: Successful task
          debug:
            msg: "Task successful"

      rescue:

        - name: Rescue task
          debug:
            msg: "Error handled"

      always:

        - name: Always task
          debug:
            msg: "Always executed"

    - name: Completion message
      debug:
        msg: "Lab 19 Completed Successfully"
EOF
```

---

### 🛠️ Step 2: Run Verification

```bash
ansible-playbook -i inventory verify-lab-completion.yml
```

---

# 🐞 Troubleshooting Common Issues

---

## ❌ Debug Module Issues

### 🔹 Problem
Debug values not showing correctly

### ✅ Solution
Check variable scope and spelling.

---

## ❌ Check Mode Issues

### 🔹 Problem
Tasks fail in check mode

### ✅ Solution

```yaml
when: not ansible_check_mode
```

---

## ❌ Error Handling Issues

### 🔹 Problem
`ignore_errors` not working

### ✅ Solution
Verify YAML indentation.

---

# 🎓 Conclusion

In this lab, you successfully learned:

- ✅ Debugging techniques in Ansible
- ✅ Dry runs with `--check`
- ✅ Error handling using `ignore_errors`
- ✅ Structured handling using `block`, `rescue`, and `always`
- ✅ Best practices for resilient automation

These skills are essential for:

- 🚀 Infrastructure Automation
- 🛡️ Reliable Deployments
- ⚙️ Production Automation
- 🎯 RHCE & Ansible Certification Preparation

---

# 📚 Next Steps

Continue practicing by:

- 🔹 Creating custom error handling workflows
- 🔹 Exploring callback plugins
- 🔹 Implementing logging systems
- 🔹 Automating production deployments

---

# 📁 Project File Structure

```bash
lab19-error-handling/
│
├── inventory
│
├── debug-variables.yml
├── advanced-debug.yml
├── system-changes.yml
├── check-mode-aware.yml
├── basic-error-handling.yml
├── advanced-error-handling.yml
├── error-handling-best-practices.yml
├── error-handling-template.yml
├── verify-lab-completion.yml
│
└── README.md
```

---

# 📄 File Descriptions

| 📁 File Name | 📝 Purpose |
|---|---|
| `inventory` | Defines managed nodes and SSH configuration |
| `debug-variables.yml` | Demonstrates basic debug module usage |
| `advanced-debug.yml` | Shows advanced debugging techniques |
| `system-changes.yml` | Used for testing `--check` mode |
| `check-mode-aware.yml` | Demonstrates check-mode-safe playbooks |
| `basic-error-handling.yml` | Implements `ignore_errors` handling |
| `advanced-error-handling.yml` | Uses `block`, `rescue`, and `always` |
| `error-handling-best-practices.yml` | Demonstrates retry logic and robust automation |
| `error-handling-template.yml` | Reusable production-ready error handling template |
| `verify-lab-completion.yml` | Verifies successful lab completion |
| `README.md` | Documentation for the entire lab |

---

# 👨‍💻 Author

**Hafiz Muhammad Salman**  
Cloud & DevOps Engineer

---
