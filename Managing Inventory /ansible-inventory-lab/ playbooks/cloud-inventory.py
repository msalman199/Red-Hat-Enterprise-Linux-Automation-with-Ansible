Add advanced dynamic inventory logic:
#!/usr/bin/env python3
"""
Advanced Dynamic Inventory Script
Simulates cloud provider integration
"""

import json
import sys
import os
import subprocess
from datetime import datetime

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
        # In real scenarios, this would use cloud provider APIs
        instances = [
            {
                'name': 'web1',
                'ip': '192.168.1.10',
                'type': 't2.micro',
                'tags': {'Role': 'webserver', 'Environment': 'production'}
            },
            {
                'name': 'web2',
                'ip': '192.168.1.11',
                'type': 't2.micro',
                'tags': {'Role': 'webserver', 'Environment': 'production'}
            },
            {
                'name': 'db1',
                'ip': '192.168.1.20',
                'type': 't2.small',
                'tags': {'Role': 'database', 'Environment': 'production'}
            }
        ]
        return instances
        
    def build_inventory(self):
        """Build the inventory structure"""
        instances = self.discover_instances()
        
        # Initialize inventory structure
        self.inventory = {
            'all': {
                'vars': {
                    'cloud_provider': self.cloud_provider,
                    'region': self.region,
                    'discovered_at': datetime.now().isoformat()
                }
            },
            '_meta': {
                'hostvars': {}
            }
        }
        
        # Group instances by role
        for instance in instances:
            role = instance['tags'].get('Role', 'ungrouped')
            group_name = f"{role}s" if not role.endswith('s') else role
            
            # Create group if it doesn't exist
            if group_name not in self.inventory:
                self.inventory[group_name] = {
                    'hosts': [],
                    'vars': {}
                }
            
            # Add host to group
            self.inventory[group_name]['hosts'].append(instance['name'])
            
            # Add host variables
            self.inventory['_meta']['hostvars'][instance['name']] = {
                'ansible_host': instance['ip'],
                'ansible_user': 'student',
                'instance_type': instance['type'],
                'cloud_provider': self.cloud_provider,
                'region': self.region
            }
            
            # Add tags as variables
            for tag_key, tag_value in instance['tags'].items():
                self.inventory['_meta']['hostvars'][instance['name']][f"tag_{tag_key.lower()}"] = tag_value
        
        # Create environment-based groups
        env_group = f"{self.environment}_servers"
        self.inventory[env_group] = {
            'children': list(self.inventory.keys())[1:-1]  # Exclude 'all' and '_meta'
        }
        
        return self.inventory
    
    def get_inventory(self):
        """Return the complete inventory"""
        return self.build_inventory()
    
    def get_host_vars(self, hostname):
        """Return variables for a specific host"""
        inventory = self.get_inventory()
        return inventory.get('_meta', {}).get('hostvars', {}).get(hostname, {})

def main():
    """Main execution function"""
    cloud_inv = CloudInventory()
    
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print(json.dumps(cloud_inv.get_inventory(), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        print(json.dumps(cloud_inv.get_host_vars(sys.argv[2]), indent=2))
    else:
        print("Usage: {} --list or {} --host <hostname>".format(sys.argv[0], sys.argv[0]))
        sys.exit(1)

if __name__ == '__main__':
    main()
