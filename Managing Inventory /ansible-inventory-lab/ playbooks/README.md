# Managing Inventory

A comprehensive, step-by-step hands-on lab manual for creating, configuring, and testing static and dynamic Ansible inventory environments. This guide covers INI formats, YAML formatting syntax, dynamic asset mapping via Python abstraction layers, and host-variable segmentation rules.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Create and configure static inventory files for multi-tiered infrastructure automation.
* Mastery over structural design differences between basic INI configurations and YAML inventory parameters.
* Programmatically implement dynamic data injection scripts to discover cloud assets.
* Audit and validate network topologies using dedicated management commands.
* Segment massive multi-region host maps into organized nested infrastructure groupings.
* Inject variable scopes across systems to drive fine-grained target system behaviors.

---

## 🧰 Tools & Commands Matrix
The following table outlines the foundational system engines and troubleshooting commands used throughout this lab:




| Tool / Command | Type | Primary Purpose in this Lab | Common Use Case Example |
| :--- | :--- | :--- | :--- |
| `ansible-inventory` | Engine Utility | Parses, checks, and graphs structural configurations of target inventories. | `ansible-inventory -i ... --list` |
| `ansible` | Engine CLI | Dispatches ad-hoc connection runs or checks to explicit system boundaries. | `ansible -i ... managed_nodes -m ping` |
| `chmod` | System Binary | Alters standard operating system permission bitmasks on files. | `chmod +x dynamic-inventory.py` |
| `python3` | Runtime | Executes custom dynamic inventory discovery scripts. | `./dynamic-inventory.py --list` |

---

## 💻 Lab Environment & Prerequisites

### Prerequisites
* Basic competency over core Linux terminal command execution paths.
* Familiarity with text editors like `nano`, `vim`, or similar.
* Completion of preceding configuration guides covering basic playbooks.
* Basic understanding of structural YAML markup layouts and key-value blocks.
* Functional knowledge of SSH public key-based server access.

### Environment Specs
This architecture lab manual runs across a pre-authenticated cloud workspace network:
* **Control Node:** Dedicated management host computer (`ansible-control`).
* **Managed Nodes:** Multi-tiered production server environments (`web1`, `web2`, `db1`).
* **Connectivity:** Shared public keys are pre-loaded to facilitate zero-prompt terminal connections.

---

## 🚀 Lab Implementation Steps

### Task 1: Create a Static Inventory File

#### Subtask 1.1: Understanding Inventory Basics
Establish a safe storage directory workspace, then construct your first fundamental INI mapping schema:

```bash
# Step 1: Connect directly to your master control engine target
ssh student@ansible-control

# Step 2: Establish a dedicated subfolder workspace tracking environment rules
cd /home/student/ansible-labs
mkdir lab3-inventory
cd lab3-inventory

# Step 3: Open an initial empty initialization configuration file
nano inventory.ini
```

Step 4: Append the following group structures, child definitions, and variable parameters:
```ini
# Basic Static Inventory File
# Web Servers Group
[webservers]
web1 ansible_host=192.168.1.10 ansible_user=student
web2 ansible_host=192.168.1.11 ansible_user=student

# Database Servers Group
[databases]
db1 ansible_host=192.168.1.20 ansible_user=student

# All servers group (automatically created)
[production:children]
webservers
databases

# Group variables
[webservers:vars]
http_port=80
max_clients=200

[databases:vars]
mysql_port=3306
max_connections=100
```
*Step 5: Save configurations and drop back into shell loops (`Ctrl+X` -> `Y` -> `Enter`).*

#### Subtask 1.2: Creating an Advanced Static Inventory
Build a real-world enterprise infrastructure layout featuring tiering, locations, and global variable injections:

```bash
# Step 1: Open an advanced static configuration document shell
nano advanced-inventory.ini
```

Step 2: Input the multi-region structural configuration layer details shown below:
```ini
# Advanced Static Inventory Configuration

# Web Server Tier
[webservers]
web1 ansible_host=192.168.1.10 ansible_user=student server_role=frontend
web2 ansible_host=192.168.1.11 ansible_user=student server_role=frontend

# Database Tier
[databases]
db1 ansible_host=192.168.1.20 ansible_user=student server_role=backend

# Load Balancers
[loadbalancers]
lb1 ansible_host=192.168.1.30 ansible_user=student server_role=loadbalancer

# Environment Groups
[production:children]
webservers
databases
loadbalancers

[staging]
staging-web ansible_host=192.168.1.40 ansible_user=student
staging-db ansible_host=192.168.1.41 ansible_user=student

# Regional Groups
[east-coast]
web1
db1

[west-coast]
web2
lb1

# Global Variables
[all:vars]
ansible_ssh_private_key_file=/home/student/.ssh/id_rsa
ansible_ssh_common_args='-o StrictHostKeyChecking=no'

# Group-specific Variables
[webservers:vars]
http_port=80
https_port=443
document_root=/var/www/html
max_clients=200

[databases:vars]
mysql_port=3306
mysql_datadir=/var/lib/mysql
max_connections=100
innodb_buffer_pool_size=256M

[loadbalancers:vars]
balance_method=roundrobin
health_check_interval=30
```

#### Subtask 1.3: Creating YAML Format Inventory
Translate your parameters into human-readable nested structural layouts using standard object keys:

```bash
# Step 1: Open an updated declarative layout file context container
nano inventory.yml
```

Step 2: Input the matching declarative structure rules strictly validating correct alignment tabs:
```yaml
# YAML Static Inventory File
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.10
          ansible_user: student
          server_role: frontend
          http_port: 80
        web2:
          ansible_host: 192.168.1.11
          ansible_user: student
          server_role: frontend
          http_port: 80
      vars:
        max_clients: 200
        document_root: /var/www/html
    
    databases:
      hosts:
        db1:
          ansible_host: 192.168.1.20
          ansible_user: student
          server_role: backend
          mysql_port: 3306
      vars:
        max_connections: 100
        mysql_datadir: /var/lib/mysql
    
    production:
      children:
        webservers:
        databases:
      vars:
        environment: production
        backup_schedule: "0 2 * * *"
```

---

### Task 2: Use Dynamic Inventory for Cloud-Based Systems

#### Subtask 2.1: Understanding Dynamic Inventory
Construct an executive orchestration runtime script layer designed to simulate query executions against backend API cloud targets:

```bash
# Step 1: Open a fresh automation script document interface
nano dynamic-inventory.py
```

Step 2: Inject the complete JSON serialization handling pipeline code structure block shown below:
```python
#!/usr/bin/env python3
"""
Simple Dynamic Inventory Script for Ansible
This script demonstrates how to create dynamic inventory
"""

import json
import sys

def get_inventory():
    """Generate dynamic inventory"""
    inventory = {
        'webservers': {
            'hosts': ['web1', 'web2'],
            'vars': {
                'http_port': 80,
                'max_clients': 200
            }
        },
        'databases': {
            'hosts': ['db1'],
            'vars': {
                'mysql_port': 3306,
                'max_connections': 100
            }
        },
        'production': {
            'children': ['webservers', 'databases'],
            'vars': {
                'environment': 'production'
            }
        },
        '_meta': {
            'hostvars': {
                'web1': {
                    'ansible_host': '192.168.1.10',
                    'ansible_user': 'student',
                    'server_role': 'frontend'
                },
                'web2': {
                    'ansible_host': '192.168.1.11',
                    'ansible_user': 'student',
                    'server_role': 'frontend'
                },
                'db1': {
                    'ansible_host': '192.168.1.20',
                    'ansible_user': 'student',
                    'server_role': 'backend'
                }
            }
        }
    }
    return inventory

def get_host_vars(host):
    """Get variables for a specific host"""
    inventory = get_inventory()
    return inventory.get('_meta', {}).get('hostvars', {}).get(host, {})

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print(json.dumps(get_inventory(), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        print(json.dumps(get_host_vars(sys.argv[2]), indent=2))
    else:
        print("Usage: {} --list or {} --host <hostname>".format(sys.argv[0], sys.argv[0]))
        sys.exit(1)

if __name__ == '__main__':
    main()
```

```bash
# Step 3: Enforce operational file system execute flags on the scripting layout
chmod +x dynamic-inventory.py
```

#### Subtask 2.2: Creating an Advanced Dynamic Inventory Script
Prepare an advanced multi-provider tracking framework layer template:

```bash
# Step 1: Open your secondary dynamic environment mapping container
nano cloud-inventory.py
```

Step 2: Inject the initial contextual engine foundation block logic:
```python
#!/usr/bin/env python3
"""
Advanced Dynamic Inventory Script
Simulates cloud provider integration
"""

import json
import sys
import os

class CloudInventory:
    def __init__(self):
        self.inventory = {}
        self.read_environment()
        
    def read_environment(self):
        """Read configuration from environment variables"""
        self.cloud_provider = os.environ.get('CLOUD_PROVIDER', 'aws')
        self.region = os.environ.get('CLOUD_REGION', 'us-east-1')
        self.environment = os.environ.get('ENVIRONMENT', 'production')
        
    def discover_instances(self):
        """Simulate cloud instance discovery"""
        # Placeholder for dynamic cloud provider instance API ingestion
        pass
```
*Note: In real production systems, this placeholder block triggers API client calls (e.g., using `boto3` for AWS or `google-auth` for GCP) to parse raw metadata values directly into the required JSON mapping syntax.*

---

## 🔍 Verification & Troubleshooting Checklist
Run the validation commands below to verify your settings match compliance bounds before finishing up:

* [ ] **INI Structure Audit:** Verify static files structure cleanly on screen using `ansible-inventory -i inventory.ini --list`.
* [ ] **YAML Structural Verification:** Ensure your nested indentations align with syntax guidelines by running `ansible-inventory -i inventory.yml --graph`.
* [ ] **Dynamic Processing Check:** Execute your Python discovery pipeline directly to confirm it renders valid JSON tracking structures: `./dynamic-inventory.py --list`.
* [ ] **End-to-End Pipeline Check:** Validate ad-hoc routing connectivity over all managed targets by running `ansible -i inventory.ini all -m ping`.

### Troubleshooting Matrix
* **Anomalous State: `ERROR! The inventory file was not parseable as a script`**
  * *Root Cause:* Your script lacks the mandatory shell parser identifier line (`#!/usr/bin/env python3`), or you forgot to mark it as executable.
  * *Remediation:* Verify that the script starts with the correct path definition and update the file permissions by running `chmod +x dynamic-inventory.py`.
* **Anomalous State: `Host matched multiple group variables`**
  * *Root Cause:* Overlapping child groups conflict when attempting to set the same variable string targets.
  * *Remediation:* Keep your tracking variable parameters separated cleanly, or move global attributes down into the master configuration sections inside `[all:vars]`.

---

## 🏁 Conclusion
By completing this practical lab guide, you have transitioned from basic host tracking to designing scalable, multi-format environment inventories.

### Key Architectural Takeaways:
* **Alternative Serialization Formats:** Transforming flat INI layouts into clear, tree-mapped YAML files helps reduce configuration duplication in complex systems.
* **Dynamic Cloud Integration:** Implementing JSON automation pipelines allows you to replace brittle manual lists with automated host tracking that scales across fluid cloud environments.
* **Hierarchical Variables Scoping:** Assigning variables logically to individual hosts, specific tiers, or broad regions helps keep configuration codes clean, reusable, and maintainable.

---

## 📁 Repository Directory File Structure
To organize your playbook files and scripts, align your repository directories to match the folder structure shown below:

```text
📁 ansible-inventory-lab/
└── 📁 playbooks/
    └── 📁 lab3-inventory/
        ├── 📄 advanced-inventory.ini     # Enterprise tier mapping setup featuring region overrides
        ├── 📄 cloud-inventory.py         # Advanced template class structure managing cloud provider queries
        ├── 📄 dynamic-inventory.py       # Runnable script that auto-generates JSON target mapping schemas
        ├── 📄 inventory.ini              # Baseline initial INI grouping setup file
        └── 📄 inventory.yml              # Nested YAML environment definitions file
```
