# Variables and Facts

A comprehensive, step-by-step hands-on lab manual for understanding, implementing, and organizing user-defined variables and system-discovered facts within Ansible automation architectures. This guide covers local data formatting types, external group variables files, custom system facts creation, and dynamic conditional playbooks.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Define and use variables in Ansible playbooks across multiple data types.
* Gather critical remote host system information using Ansible facts.
* Create conditional tasks based on gathered facts such as OS type, distribution, and version.
* Implement variable substitution cleanly in playbook tasks using Jinja2 syntax.
* Understand the core differences between user-defined variables and system facts.
* Apply operational best practices for variable naming and usage in automation scenarios.

---

## 🧰 Core Engines & Directives Matrix
The following table outlines the foundational system utilities, directives, and testing components utilized throughout this lab:


| Component Name | Type | Primary Purpose in this Lab | Common Use Case Example |
| :--- | :--- | :--- | :--- |
| `ansible-playbook` | Engine CLI | Executes declarative automation blueprints against chosen inventory groups. | `ansible-playbook -i ...` |
| `gather_facts` | Play Directive | Controls the initialization loop that harvests hardware and OS data on targets. | `gather_facts: yes` |
| `debug` | Ansible Module | Interrogates active variables, evaluated structures, or strings onto stdout. | `debug: var=ansible_facts` |
| `setup` | Ansible Module | Manually triggers the execution loop that gathers system parameters and reloads facts. | `setup:` |
| `loop` | Task Directive | Iterates a single execution module block over sequential lists or dictionary keys. | `loop: "{{ required_packages }}"` |
| `when` | Task Directive | Enforces conditional gate parameters that limit execution to specific matches. | `when: ansible_os_family == "RedHat"` |

---

## 💻 Lab Environment & Prerequisites

### Prerequisites
* Basic understanding of YAML syntax, indentation conventions, and spacing rules.
* Familiarity with Linux command line operations and basic text editors (`nano`, `vim`).
* Completion of previous Ansible labs (Lab 1-4) or equivalent foundational automation knowledge.
* Understanding of basic Ansible playbook structure and execution loops.
* Functional knowledge of SSH key-based authentication for server access.

### Environment Specs
This architecture lab manual runs across a pre-authenticated multi-distribution staging layout:
* **Control Node:** Dedicated management host running CentOS/RHEL 8 with Ansible pre-installed.
* **Managed Nodes:** Multiple target systems running CentOS and Ubuntu distributions for multi-platform testing.
* **Connectivity:** Pre-configured SSH keys for seamless, zero-prompt terminal connectivity between nodes.

---

## 🚀 Lab Implementation Steps

### Task 1: Understanding and Defining Variables in Playbooks

#### Subtask 1.1: Create a Basic Playbook with Variables
Variables in Ansible allow you to store and reuse values throughout your playbooks, making them flexible and maintainable.

```bash
# Step 1: Connect to your control node and create a new directory for this lab
mkdir ~/lab5-variables-facts
cd ~/lab5-variables-facts

# Step 2: Open your first playbook file context container
nano variables-demo.yml
```

Step 3: Add the following content to demonstrate different ways to define variable data types (strings, integers, booleans, lists, and dictionaries):
```yaml
---
- name: Variables and Facts Demonstration
  hosts: all
  vars:
    # Simple string variable
    application_name: "WebServer"
    
    # Numeric variable
    port_number: 8080
    
    # Boolean variable
    enable_ssl: true
    
    # List variable
    required_packages:
      - httpd
      - firewalld
      - vim
    
    # Dictionary variable
    database_config:
      host: "localhost"
      port: 3306
      name: "webapp_db"
      user: "webapp_user"
  
  tasks:
    - name: Display application information
      debug:
        msg: "Setting up {{ application_name }} on port {{ port_number }}"
    
    - name: Show SSL status
      debug:
        msg: "SSL is {{ 'enabled' if enable_ssl else 'disabled' }}"
    
    - name: Display required packages
      debug:
        msg: "Installing package: {{ item }}"
      loop: "{{ required_packages }}"
    
    - name: Show database configuration
      debug:
        msg: "Database: {{ database_config.name }} on {{ database_config.host }}:{{ database_config.port }}"
```

```bash
# Step 4: Run the playbook to see the variables evaluate in your terminal
ansible-playbook -i inventory variables-demo.yml
```

#### Subtask 1.2: Using External Variable Files
Decouple parameters entirely from task logic to organize corporate-scale configuration properties cleanly:

```bash
# Step 1: Create a separate variable subdirectory and definition file
mkdir -p group_vars
nano group_vars/all.yml
```

Step 2: Add global variable parameters to the external configuration file:
```yaml
---
# Application Configuration
app_name: "MyWebApp"
app_version: "2.1.0"
app_port: 9090

# System Configuration
max_connections: 100
timeout_seconds: 30

# Environment Settings
environment: "production"
debug_mode: false

# File paths
log_directory: "/var/log/myapp"
config_directory: "/etc/myapp"
```

```bash
# Step 3: Create a playbook that references these external variable fields
nano external-vars-demo.yml
```

Input the following tasks to pull and display data from your group variables directory:
```yaml
---
- name: Using External Variables
  hosts: all
  
  tasks:
    - name: Display application details
      debug:
        msg: |
          Application: {{ app_name }}
          Version: {{ app_version }}
          Port: {{ app_port }}
          Environment: {{ environment }}
    
    - name: Show configuration paths
      debug:
        msg: |
          Log Directory: {{ log_directory }}
          Config Directory: {{ config_directory }}
          Max Connections: {{ max_connections }}
```

```bash
# Step 4: Execute the external vars validation playbook
ansible-playbook -i inventory external-vars-demo.yml
```

---

### Task 2: Using Ansible Facts to Gather System Information

#### Subtask 2.1: Understanding Ansible Facts
Ansible facts are dynamic system properties automatically discovered by the setup engine when connecting to managed hosts.

```bash
# Step 1: Create a playbook to explore available facts variables
nano facts-exploration.yml
```

Step 2: Add content to gather and filter structural host system properties:
```yaml
---
- name: Exploring Ansible Facts
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: Display all available facts
      debug:
        var: ansible_facts
      when: inventory_hostname == groups['all'][0]  # Only show for first host to reduce spam
    
    - name: Show basic system information
      debug:
        msg: |
          Hostname: {{ ansible_hostname }}
          Operating System: {{ ansible_distribution }} {{ ansible_distribution_version }}
          Architecture: {{ ansible_architecture }}
          Kernel: {{ ansible_kernel }}
          Total Memory: {{ ansible_memtotal_mb }} MB
          CPU Cores: {{ ansible_processor_cores }}
    
    - name: Display network information
      debug:
        msg: |
          IP Address: {{ ansible_default_ipv4.address }}
          Network Interface: {{ ansible_default_ipv4.interface }}
          Gateway: {{ ansible_default_ipv4.gateway }}
    
    - name: Show disk information
      debug:
        msg: |
          Mount Point: {{ item.mount }}
          Device: {{ item.device }}
          Filesystem: {{ item.fstype }}
          Size: {{ item.size_total | human_readable }}
          Available: {{ item.size_available | human_readable }}
      loop: "{{ ansible_mounts }}"
      when: item.mount == "/"
```

```bash
# Step 3: Run the facts exploration playbook
ansible-playbook -i inventory facts-exploration.yml
```

#### Subtask 2.2: Creating Custom Facts
Inject localized configuration maps into managed node directories to track unique operational variables alongside standard system parameters.

```bash
# Step 1: Open a deployment blueprint configuration file
nano setup-custom-facts.yml
```

Step 2: Add playbook tasks to provision local folders and define custom JSON/INI facts:
```yaml
---
- name: Setup Custom Facts
  hosts: all
  become: yes
  
  tasks:
    - name: Create custom facts directory
      file:
        path: /etc/ansible/facts.d
        state: directory
        mode: '0755'
    
    - name: Create custom application facts
      copy:
        content: |
          #!/bin/bash
          echo "{"
          echo "  \"application\": {"
          echo "    \"name\": \"MyCustomApp\","
          echo "    \"version\": \"1.0.0\","
          echo "    \"status\": \"active\","
          echo "    \"last_updated\": \"$(date -I)\""
          echo "  }"
          echo "}"
        dest: /etc/ansible/facts.d/application.fact
        mode: '0755'
    
    - name: Create system health facts
      copy:
        content: |
          [system_health]
          uptime_days={{ ansible_uptime_seconds | int // 86400 }}
          load_average={{ ansible_loadavg['1m'] }}
          disk_usage_root={{ (ansible_mounts | selectattr('mount', 'equalto', '/') | first).size_used / (ansible_mounts | selectattr('mount', 'equalto', '/') | first).size_total * 100 | round(2) }}
        dest: /etc/ansible/facts.d/health.fact
        mode: '0644'
    
    - name: Refresh facts to include custom facts
      setup:
```

```bash
# Step 3: Execute the custom facts file setup
ansible-playbook -i inventory setup-custom-facts.yml

# Step 4: Open a verification output playbook to read the custom namespaces
nano display-custom-facts.yml
```

Add the custom metrics printing configurations below:
```yaml
---
- name: Display Custom Facts
  hosts: all
  
  tasks:
    - name: Show custom application facts
      debug:
        msg: |
          App Name: {{ ansible_local.application.application.name }}
          App Version: {{ ansible_local.application.application.version }}
          App Status: {{ ansible_local.application.application.status }}
          Last Updated: {{ ansible_local.application.application.last_updated }}
    
    - name: Show custom health facts
      debug:
        msg: |
          System Uptime: {{ ansible_local.health.system_health.uptime_days }} days
          Load Average: {{ ansible_local.health.system_health.load_average }}
          Root Disk Usage: {{ ansible_local.health.system_health.disk_usage_root }}%
```

```bash
# Step 5: Run the custom facts display playbook to confirm setup
ansible-playbook -i inventory display-custom-facts.yml
```

---

## 🔍 Verification & Troubleshooting Checklist
Run the validation checkpoints below to ensure your variables evaluate correctly before finishing the lab:

* [ ] **Data Formats Validation:** Confirm dictionary paths resolve accurately and loops compile parameter variables cleanly via `variables-demo.yml`.
* [ ] **Decoupled Injection Verification:** Ensure global configuration attributes append cleanly without syntax flaws via `group_vars/all.yml`.
* [ ] **Telemetry Audit:** Validate that memory, network, and architecture metrics register with the setup loop using `facts-exploration.yml`.
* [ ] **Namespace Scope Verification:** Confirm local system extensions load smoothly underneath the explicit `ansible_local` variable registry.

### Common Anomalies Matrix
* **Error Token: `An unquoted string with a character like ':' is invalid`**
  * *Root Cause:* YAML formatting syntax considers unquoted string mappings containing semicolons or brackets as broken block components.
  * *Remediation:* Enclose your text value expressions containing template properties completely within double quotes, for example: `msg: "Setting up {{ application_name }}"`.
* **Error Token: `The variable is undefined` inside `ansible_local` properties**
  * *Root Cause:* The setup directory structure path is missing on the remote host, file permission bits prevent reads, or the target output returns malformed JSON.
  * *Remediation:* Ensure `/etc/ansible/facts.d/` uses `0755` permissions, scripts are executable, and the dynamic output returns perfect syntax schema layouts. Run the ad-hoc command `ansible <host> -m setup -a "filter=ansible_local"` to diagnose.

---

## 🏁 Conclusion
By implementing this data-scoping lab guide, you have moved from static parameters to designing dynamic, context-aware automation workflows.

### Key Concepts Mastered:
* **Decoupled Variable Scoping:** Abstracting configuration profiles into dedicated file sheets (`group_vars/`) to maximize play reusability.
* **Dynamic Telemetry Injection:** Utilizing auto-gathered machine facts to guide complex conditional paths across distributions smoothly.
* **Persistent Local Extensions:** Building enterprise metadata blocks beneath `facts.d/` to store business variables inside standard automation loops.
* **Jinja2 In-line Formatting:** Manipulating raw string elements and computing numeric transformations to output human-readable metric logs.

---

## 📁 Repository Directory File Structure
To maintain your development files and keep them organized, ensure your repository mirrors the following file layout model:

```text
📁 ansible-variables-lab/
└── 📁 lab5-variables-facts/
    ├── 📄 display-custom-facts.yml   # Verification script evaluating unique machine fact properties
    ├── 📄 external-vars-demo.yml     # Application play extracting metadata from external configurations
    ├── 📄 facts-exploration.yml      # Deep inspection playbook scanning remote system telemetry fields
    ├── 📄 inventory                  # Inventory configurations file mapping testing environments
    ├── 📄 setup-custom-facts.yml     # Infrastructure setup blueprint building local fact extension blocks
    ├── 📄 variables-demo.yml         # Evaluation playbook validating primitive configuration data formatting
    └── 📁 group_vars/
        └── 📄 all.yml                # Centralized variables repository file containing global overrides
```
