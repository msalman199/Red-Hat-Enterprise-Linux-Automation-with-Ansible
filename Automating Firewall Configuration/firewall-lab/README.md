# Automating Firewall Configuration

This repository contains the complete materials, playbooks, and inventory structures for **Lab 14: Automating Firewall Configuration**. This lab guides you through using Ansible to implement network security policies, control traffic zones, and deploy advanced rule profiles across enterprise host topologies.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Configure persistent security rules using the Ansible `firewalld` module.
* Manage firewall zones and services dynamically through declarative automation scripts.
* Establish uniform firewall policies simultaneously across multiple managed nodes.
* Understand the core relationship between `firewalld` zones, services, and structural rules.
* Implement security hardening patterns using infrastructure-as-code firewall management.
* Troubleshoot common firewall state errors, runtime mismatches, and execution locking issues.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A basic understanding of Linux command-line interaction and system services.
* Familiarity with standard Ansible configurations (playbooks, inventory structures, modules).
* Core networking knowledge including common port layers, transport protocols (`TCP`/`UDP`), and services.
* General comprehension of security baselines, access boundaries, and network protection models.
* Completion of preceding labs or equivalent playbook development experience.

---

## 💻 Lab Environment
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** inside your staging panel to spin up your virtualization lab environment instantly.

Your testing sandbox boundary contains:
* **Control Node**: A central machine running CentOS/RHEL 8 with Ansible pre-installed.
* **Managed Nodes**: Two target systems waiting for explicit firewall policies.
* **Network & Privileges**: Open intra-node routing and full `sudo` administrative rights on all machines.

---

## 🛠️ Lab Tasks

### Task 1: Configure Firewall Rules Using the firewalld Module

#### Subtask 1.1: Verify Lab Environment and Firewalld Status
Inspecting service runtimes before editing rules prevents unreachable node scenarios or communication failures.

1. **Connect to your central orchestration control node and check the engine environment:**
   ```bash
   ansible --version
   ```

2. **Verify target server communication matrices via a rapid ping sweep run:**
   ```bash
   ansible all -m ping
   ```

3. **Ensure that the `firewalld` service is running and configured to launch during boot cycles:**
   ```bash
   ansible all -m systemd -a "name=firewalld state=started enabled=yes" --become
   ```

4. **Verify the active structural state of the remote system firewalls:**
   ```bash
   ansible all -m command -a "firewall-cmd --state" --become
   ```

#### Subtask 1.2: Create Basic Firewall Configuration Playbook
Build a playbook to open standard corporate access ports (`SSH`, `HTTP`, `HTTPS`) using permanent flags to ensure survival over system resets.

1. **Establish your firewall project tracking workspace:**
   ```bash
   mkdir ~/firewall-lab
   cd ~/firewall-lab
   ```

2. **Generate your local infrastructure targeting endpoints configuration file:**
   ```bash
   cat > inventory << EOF
   [webservers]
   node1 ansible_host=192.168.1.10
   node2 ansible_host=192.168.1.11

   [all:vars]
   ansible_user=student
   ansible_become=yes
   EOF
   ```

3. **Open and write your primary baseline rules playbook engine blueprint:**
   ```bash
   cat > basic-firewall.yml << 'EOF'
   ---
   - name: Configure Basic Firewall Rules
     hosts: all
     become: yes
     tasks:
       - name: Ensure firewalld is installed
         package:
           name: firewalld
           state: present

       - name: Start and enable firewalld service
         systemd:
           name: firewalld
           state: started
           enabled: yes

       - name: Allow SSH service
         firewalld:
           service: ssh
           permanent: yes
           state: enabled
           immediate: yes

       - name: Allow HTTP service
         firewalld:
           service: http
           permanent: yes
           state: enabled
           immediate: yes

       - name: Allow HTTPS service
         firewalld:
           service: https
           permanent: yes
           state: enabled
           immediate: yes

       - name: Display current firewall rules
         command: firewall-cmd --list-all
         register: firewall_rules

       - name: Show firewall configuration
         debug:
           var: firewall_rules.stdout_lines
   EOF
   ```

4. **Deploy your basic rule map configurations live across all targeted machines:**
   ```bash
   ansible-playbook -i inventory basic-firewall.yml
   ```

#### Subtask 1.3: Configure Custom Port Rules
Use variable array iterations to configure custom tracking ports, port ranges, and specific source validations.

1. **Generate your multi-tier custom configuration playbook asset module:**
   ```bash
   cat > advanced-firewall.yml << 'EOF'
   ---
   - name: Configure Advanced Firewall Rules
     hosts: webservers
     become: yes
     vars:
       custom_ports:
         - port: 8080
           protocol: tcp
           description: "Custom web application"
         - port: 3306
           protocol: tcp
           description: "MySQL database"
         - port: 5432
           protocol: tcp
           description: "PostgreSQL database"

   tasks:
     - name: Open custom TCP ports
       firewalld:
         port: "{{ item.port }}/{{ item.protocol }}"
         permanent: yes
         state: enabled
         immediate: yes
       loop: "{{ custom_ports }}"

     - name: Block specific port (example: 23/tcp for telnet)
       firewalld:
         port: 23/tcp
         permanent: yes
         state: disabled
         immediate: yes

     - name: Allow specific source IP for SSH
       firewalld:
         rich_rule: 'rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept'
         permanent: yes
         state: enabled
         immediate: yes

     - name: Create port range rule
       firewalld:
         port: 60000-61000/tcp
         permanent: yes
         state: enabled
         immediate: yes

     - name: Verify firewall configuration
       command: firewall-cmd --list-all
       register: advanced_rules

     - name: Display advanced firewall rules
       debug:
         msg: "{{ advanced_rules.stdout_lines }}"
   EOF
   ```

2. **Execute your advanced custom parameters script:**
   ```bash
   ansible-playbook -i inventory advanced-firewall.yml
   ```

#### Subtask 1.4: Implement Rich Rules for Complex Scenarios
Rich rules provide precise traffic screening by blending source paths, ports, limit tags, and logging controls into a single expression.

1. **Construct a security hardening rich rules playbook configuration module:**
   ```bash
   cat > rich-rules.yml << 'EOF'
   ---
   - name: Configure Firewall Rich Rules
     hosts: all
     become: yes
     tasks:
       - name: Allow HTTP only from specific network
         firewalld:
           rich_rule: 'rule family="ipv4" source address="10.0.0.0/8" service name="http" accept'
           permanent: yes
           state: enabled
           immediate: yes

       - name: Block specific IP from accessing SSH
         firewalld:
           rich_rule: 'rule family="ipv4" source address="192.168.1.100" service name="ssh" drop'
           permanent: yes
           state: enabled
           immediate: yes

       - name: Rate limit SSH connections
         firewalld:
           rich_rule: 'rule service name="ssh" accept limit value="3/m"'
           permanent: yes
           state: enabled
           immediate: yes

       - name: Allow ICMP ping from internal network only
         firewalld:
           rich_rule: 'rule family="ipv4" source address="192.168.0.0/16" icmp-block-inversion="yes" accept'
           permanent: yes
           state: enabled
           immediate: yes

       - name: Log dropped packets on port 80
         firewalld:
           rich_rule: 'rule port port="80" protocol="tcp" log prefix="HTTP-DROP" level="info" drop'
           permanent: yes
           state: enabled
           immediate: yes

       - name: List all rich rules
         command: firewall-cmd --list-rich-rules
         register: rich_rules_output

       - name: Display configured rich rules
         debug:
           msg: "{{ rich_rules_output.stdout_lines }}"
   EOF
   ```

2. **Execute your rich rules playbook configuration:**
   ```bash
   ansible-playbook -i inventory rich-rules.yml
   ```

---

### Task 2: Manage Zones and Services with firewalld in Ansible

#### Subtask 2.1: Understanding and Configuring Firewall Zones
Isolate target networks into custom trust environments (`zones`) to partition internal traffic metrics safely away from public exposure paths.

1. **Open your zone management orchestration workbook file:**
   ```bash
   cat > zones-management.yml << 'EOF'
   ---
   - name: Manage Firewall Zones
     hosts: all
     become: yes
     tasks:
       - name: List all available zones
         command: firewall-cmd --get-zones
         register: available_zones

       - name: Display available zones
         debug:
           msg: "Available zones: {{ available_zones.stdout }}"

       - name: Get default zone
         command: firewall-cmd --get-default-zone
         register: default_zone

       - name: Display default zone
         debug:
           msg: "Default zone: {{ default_zone.stdout }}"

       - name: Create custom zone for DMZ servers
         firewalld:
           zone: dmz-custom
           permanent: yes
           state: present

       - name: Configure DMZ zone with specific services
         firewalld:
           zone: dmz-custom
           service: "{{ item }}"
           permanent: yes
           state: enabled
           immediate: yes
         loop:
           - http
           - https
           - ssh

       - name: Add interface to specific zone (example)
         firewalld:
           zone: public
           interface: eth0
           permanent: yes
           state: enabled
           immediate: yes
   EOF
   ```
*(Note: Ensure your targeted interfaces match actual remote system labels discovered during Task 1 hardware discovery steps).*

2. **Run your zone architecture modification script:**
   ```bash
   ansible-playbook -i inventory zones-management.yml
   ```

---

### 📁 File Structure
At the conclusion of all security configuration tasks, your working layout will match this tree structure:

```text
~/firewall-lab/
├── advanced-firewall.yml   # Playbook setting variable custom ports and scopes
├── basic-firewall.yml      # Playbook establishing standard system services policies
├── inventory               # Production target host metadata connection mapping
├── rich-rules.yml          # Playbook evaluating logging controls and source dropping
└── zones-management.yml    # Playbook controlling custom zone trust environments
```

---

## 🏁 Conclusion
In this lab, you successfully built out a scalable, policy-driven host security framework. By completing these tasks, you have mastered:
* **Declarative Hardening**: Using the `firewalld` module with `permanent: yes` and `immediate: yes` properties to guarantee rules take effect right away and survive server reboots.
* **Granular Screening**: Structuring powerful rich rules to safely introduce connection logging, source rate limits, and network block drops.
* **Zone Containment**: Initializing custom traffic zones (`dmz-custom`) to group multi-interface systems into safe isolation tiers automatically.
