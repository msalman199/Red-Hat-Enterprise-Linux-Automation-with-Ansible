# Automating Network Configuration

This repository contains the complete materials, playbooks, and configuration templates for **Lab 13: Automating Network Configuration**. This lab guides you through using Ansible to orchestrate interface management, static routing matrices, and host DNS resolvers inside enterprise networking environments.

---

## 🎯 Objectives
By the end of this lab, you will be able to:
* Configure network connections and interfaces using Ansible's `nmcli` module.
* Automate static IP address assignment and network adapter state management.
* Establish persistent routing table configurations through declarative playbooks.
* Configure global multi-tier DNS servers and domain search paths automatically.
* Master the core engineering patterns of infrastructure-as-code network automation.
* Troubleshoot and fix common NetworkManager or configuration binding errors.

---

## 📋 Prerequisites
Before starting this lab, you should have:
* A basic understanding of Linux networking topologies (IPv4 addressing, subnets, gateways).
* Strong familiarity with Ansible playbook components (tasks, handlers, modules, variables).
* Full working fluency with YAML serialization syntax rules.
* Working knowledge of SSH private key validation patterns.
* Standard command-line interaction experience with Linux host configurations.

---

## 💻 Lab Environment Setup
Ready-to-Use Cloud Machines are provisioned natively by **Al Nafi** for this lab. Simply click **Start Lab** inside your provisioning dashboard to spin up your virtualization lab automatically.

Your infrastructure sandbox contains:
* **1 Ansible Control Node** (`ansible-controller`) with software and dependencies pre-installed.
* **2 Managed Target Nodes** (`node1` and `node2`) running ready for assignment operations.
* **Access Mapping**: Pre-configured internal private networking and pre-authenticated SSH infrastructure keys.

---

## 🛠️ Lab Tasks

### Task 1: Configure Network Interfaces Using nmcli Module

#### Subtask 1.1: Verify Initial Network Configuration
Inspecting operational hardware configurations avoids IP collision traps during static infrastructure modifications.

1. **Connect to your central orchestration control node:**
   ```bash
   ssh student@ansible-controller
   ```

2. **Verify node communication matrices via an instant ping test run:**
   ```bash
   ansible all -m ping
   ```

3. **Inspect current hardware adapters and NetworkManager active connections:**
   ```bash
   ansible all -m shell -a "ip addr show"
   ansible all -m shell -a "nmcli connection show"
   ```

#### Subtask 1.2: Create Ansible Inventory and Basic Playbook Structure
Establish your targeting configuration workspace and inventory mapping parameters.

1. **Create your project network automation workspace layout:**
   ```bash
   mkdir ~/lab13-network-automation
   cd ~/lab13-network-automation
   ```

2. **Generate your production network inventory routing map layout file:**
   ```bash
   cat > inventory << EOF
   [webservers]
   node1 ansible_host=192.168.1.10
   node2 ansible_host=192.168.1.11

   [all:vars]
   ansible_user=student
   ansible_ssh_private_key_file=~/.ssh/id_rsa
   EOF
   ```

3. **Validate target configuration boundaries with your new inventory definitions module:**
   ```bash
   ansible -i inventory all -m ping
   ```

#### Subtask 1.3: Configure Static IP Addresses
Dynamically map targeted host names to respective explicit static boundaries by mapping target values using system network facts.

1. **Open your primary address mapping playbook module:**
   ```bash
   cat > configure-static-ip.yml << 'EOF'
   ---
   - name: Configure Static IP Addresses
     hosts: all
     become: yes
     vars:
       network_configs:
         node1:
           ip: "192.168.1.100"
           gateway: "192.168.1.1"
           dns: "8.8.8.8"
         node2:
           ip: "192.168.1.101"
           gateway: "192.168.1.1"
           dns: "8.8.8.8"
     
     tasks:
       - name: Configure static IP for ethernet interface
         community.general.nmcli:
           conn_name: "{{ ansible_default_ipv4.interface }}"
           ifname: "{{ ansible_default_ipv4.interface }}"
           type: ethernet
           ip4: "{{ network_configs[inventory_hostname].ip }}/24"
           gw4: "{{ network_configs[inventory_hostname].gateway }}"
           dns4: "{{ network_configs[inventory_hostname].dns }}"
           state: present
         notify: restart_network

       - name: Bring up the connection
         community.general.nmcli:
           conn_name: "{{ ansible_default_ipv4.interface }}"
           state: up

     handlers:
       - name: restart_network
         service:
           name: NetworkManager
           state: restarted
   EOF
   ```

2. **Deploy your static connection layout maps live onto your production nodes:**
   ```bash
   ansible-playbook -i inventory configure-static-ip.yml
   ```

3. **Verify the new runtime addressing modifications on remote instances:**
   ```bash
   ansible -i inventory all -m shell -a "ip addr show"
   ```

#### Subtask 1.4: Configure Additional Network Interfaces
Leverage host play list indices to dynamically generate unique secondary host allocations.

1. **Generate your secondary network connection expansion configuration playbook:**
   ```bash
   cat > configure-secondary-interface.yml << 'EOF'
   ---
   - name: Configure Secondary Network Interface
     hosts: all
     become: yes
     
     tasks:
       - name: Create secondary network connection
         community.general.nmcli:
           conn_name: "secondary-net"
           ifname: "{{ ansible_default_ipv4.interface }}"
           type: ethernet
           ip4: "10.0.0.{{ ansible_play_hosts.index(inventory_hostname) + 10 }}/24"
           state: present
         
       - name: Verify secondary connection exists
         community.general.nmcli:
           conn_name: "secondary-net"
           state: present
         register: secondary_result
         
       - name: Display connection status
         debug:
           msg: "Secondary network connection configured: {{ secondary_result.changed }}"
   EOF
   ```

2. **Deploy the secondary interface parameters:**
   ```bash
   ansible-playbook -i inventory configure-secondary-interface.yml
   ```

3. **Confirm that the secondary connections exist on all managed targets:**
   ```bash
   ansible -i inventory all -m shell -a "nmcli connection show"
   ```

---

### Task 2: Set Up Routing and DNS Configurations

#### Subtask 2.1: Configure Custom Routing Tables
Use a combined approach containing both `nmcli` modules and persistent network configuration path loops to establish durable server routing setups.

1. **Open your static routing configuration workbook file:**
   ```bash
   cat > configure-routing.yml << 'EOF'
   ---
   - name: Configure Advanced Routing
     hosts: all
     become: yes
     vars:
       custom_routes:
         - destination: "172.16.0.0/16"
           gateway: "192.168.1.1"
           metric: 100
         - destination: "10.10.0.0/16"
           gateway: "192.168.1.1"
           metric: 200
     
     tasks:
       - name: Add custom static routes
         community.general.nmcli:
           conn_name: "{{ ansible_default_ipv4.interface }}"
           type: ethernet
           routes4: "{{ custom_routes | map(attribute='destination') | list }}"
           route_metric4: "{{ custom_routes[0].metric }}"
           state: present
         notify: reload_connection
         
       - name: Configure routing table entries
         lineinfile:
           path: /etc/sysconfig/network-scripts/route-{{ ansible_default_ipv4.interface }}
           line: "{{ item.destination }} via {{ item.gateway }} metric {{ item.metric }}"
           create: yes
         loop: "{{ custom_routes }}"
         notify: reload_connection
         
       - name: Display current routing table
         shell: "ip route show"
         register: routing_table
         
       - name: Show routing configuration
         debug:
           var: routing_table.stdout_lines

     handlers:
       - name: reload_connection
         community.general.nmcli:
           conn_name: "{{ ansible_default_ipv4.interface }}"
           state: down
         notify: bring_up_connection
         
       - name: bring_up_connection
         community.general.nmcli:
           conn_name: "{{ ansible_default_ipv4.interface }}"
           state: up
   EOF
   ```

2. **Deploy your routing entries:**
   ```bash
   ansible-playbook -i inventory configure-routing.yml
   ```

3. **Verify the active routing infrastructure tables:**
   ```bash
   ansible -i inventory all -m shell -a "ip route show"
   ```

#### Subtask 2.2: Configure DNS Settings
Combine NetworkManager settings overrides with structural template blocks to enforce naming system priority rules securely.

1. **Open your domain host name resolution configuration playbook file:**
   ```bash
   cat > configure-dns.yml << 'EOF'
   ---
   - name: Configure DNS Settings
     hosts: all
     become: yes
     vars:
       dns_servers:
         primary: "8.8.8.8"
         secondary: "8.8.4.4"
         tertiary: "1.1.1.1"
       search_domains:
         - "example.com"
         - "lab.local"
         - "internal.net"
     
     tasks:
       - name: Configure DNS servers in NetworkManager connection
         community.general.nmcli:
           conn_name: "{{ ansible_default_ipv4.interface }}"
           type: ethernet
           dns4: 
             - "{{ dns_servers.primary }}"
             - "{{ dns_servers.secondary }}"
             - "{{ dns_servers.tertiary }}"
           dns4_search: "{{ search_domains }}"
           state: present
         notify: restart_network
         
       - name: Create custom resolv.conf backup
         copy:
           src: /etc/resolv.conf
           dest: /etc/resolv.conf.backup
           remote_src: yes
           
       - name: Configure /etc/resolv.conf
         template:
           src: resolv.conf.j2
           dest: /etc/resolv.conf
           backup: yes
         notify: test_dns
         
       - name: Set DNS resolution priority
         lineinfile:
           path: /etc/nsswitch.conf
           regexp: '^hosts:'
           line: 'hosts: files dns myhostname'
           backup: yes

     handlers:
       - name: restart_network
         service:
           name: NetworkManager
           state: restarted
           
       - name: test_dns
         shell: "nslookup google.com"
         register: dns_test
         ignore_errors: yes
   EOF
   ```

2. **Build your structural templates directory and open the dynamic template engine file:**
   ```bash
   mkdir -p templates
   cat > templates/resolv.conf.j2 << 'EOF'
   # Generated by Ansible - Lab 13
   # Search domains
   {% if search_domains is defined %}
   search {% for domain in search_domains %}{{ domain }} {% endfor %}
   {% endif %}

   # Nameservers
   nameserver {{ dns_servers.primary }}
   nameserver {{ dns_servers.secondary }}
   nameserver {{ dns_servers.tertiary }}
   EOF
   ```

3. **Deploy your dynamic resolver parameters:**
   ```bash
   ansible-playbook -i inventory configure-dns.yml
   ```

---

### 📁 File Structure
At the completion of all network configuration tasks, your working layout will match this tree structure:

```text
~/lab13-network-automation/
├── configure-dns.yml                   # Playbook orchestrating DNS and resolve metrics
├── configure-routing.yml               # Playbook setting static route configuration rules
├── configure-secondary-interface.yml   # Playbook managing multi-homed link loops
├── configure-static-ip.yml            # Playbook establishing primary static addressing
├── inventory                           # Production target device mapping file
└── templates/
    └── resolv.conf.j2                  # Jinja2 dynamic system naming resolver template
```

---

## 🏁 Conclusion
In this lab, you successfully built out a scalable network automation framework. By completing these tasks, you have mastered:
* **Interface Abstraction**: Using the `nmcli` module to declare network interface states cleanly, without modifying system files manually.
* **Persistent Routing**: Implementing consistent static routes via configuration drops to handle internal network data streams across multi-homed targets safely.
* **Dynamic Resolution**: Bundling NetworkManager bindings with structural Jinja2 templates to provide robust naming and domain failover handling.
