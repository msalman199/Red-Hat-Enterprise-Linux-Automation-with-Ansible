#!/usr/bin/env python3
"""
Simple Dynamic Inventory Script for Ansible
This script demonstrates how to create dynamic inventory
"""

import json
import sys
import subprocess

def get_inventory():
    """Generate dynamic inventory"""
    
    # Simulate discovering hosts (in real scenarios, this would query cloud APIs)
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
        # Return full inventory
        print(json.dumps(get_inventory(), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        # Return host-specific variables
        print(json.dumps(get_host_vars(sys.argv[2]), indent=2))
    else:
        print("Usage: {} --list or {} --host <hostname>".format(sys.argv[0], sys.argv[0]))
        sys.exit(1)

if __name__ == '__main__':
    main()
