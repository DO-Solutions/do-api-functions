import os
import json
from pydo import Client

def main(args):
    """
    Retrieve or control droplet information from the DigitalOcean API.
    
    Args:
        args (dict): Input parameters
            - api_token: DigitalOcean API token
            - droplet_id: Optional specific droplet ID to retrieve or control
            - tag: Optional tag to filter droplets
            - limit: Optional limit for the number of droplets to return (default: 10)
            - action: Optional action to perform on droplet (power_on, power_off)
    
    Returns:
        dict: API response containing droplet information or action status in the 'body' key
    """
    # Extract parameters
    api_token = os.environ.get('DO_API_TOKEN')  # Get token from environment variable
    droplet_id = args.get('droplet_id')
    tag = args.get('tag')
    limit = args.get('limit', 10)
    action = args.get('action')
    
    # Validate environment variable
    if not api_token:
        return {
            'body': {
                'error': 'DO_API_TOKEN environment variable is not set',
                'status': 'error'
            }
        }
    
    try:
        # Initialize DigitalOcean client
        client = Client(token=api_token)
        
        # Check if we need to perform an action on a droplet
        if droplet_id and action:
            droplet_id = int(droplet_id)  # Convert to integer as the API expects
            
            if action == 'power_on':
                # Call the post method with the action type
                response = client.droplet_actions.post(droplet_id=droplet_id, body={"type": "power_on"})
                return {
                    'body': {
                        'action': response,
                        'status': 'success',
                        'message': f'Power on initiated for droplet {droplet_id}'
                    }
                }
            elif action == 'power_off':
                # Call the post method with the action type
                response = client.droplet_actions.post(droplet_id=droplet_id, body={"type": "power_off"})
                return {
                    'body': {
                        'action': response,
                        'status': 'success',
                        'message': f'Power off initiated for droplet {droplet_id}'
                    }
                }
            else:
                return {
                    'body': {
                        'error': f'Unsupported action: {action}. Supported actions: power_on, power_off',
                        'status': 'error'
                    }
                }
        
        # Get specific droplet or list of droplets
        if droplet_id:
            droplet_id = int(droplet_id)  # Convert to integer as the API expects
            response = client.droplets.get(droplet_id=droplet_id)
            droplets = [response['droplet']] if 'droplet' in response else []
        else:
            # Apply tag filter if provided
            params = {'per_page': limit}
            if tag:
                params['tag_name'] = tag
                
            response = client.droplets.list(**params)
            droplets = response.get('droplets', [])
        
        # Extract relevant information from each droplet
        droplet_info = []
        for droplet in droplets:
            networks = droplet.get('networks', {})
            public_networks = networks.get('v4', [])
            public_ip = next((network['ip_address'] for network in public_networks 
                             if network['type'] == 'public'), None)
            
            droplet_info.append({
                'id': droplet.get('id'),
                'name': droplet.get('name'),
                'status': droplet.get('status'),
                'created_at': droplet.get('created_at'),
                'memory': droplet.get('memory'),
                'vcpus': droplet.get('vcpus'),
                'disk': droplet.get('disk'),
                'region': droplet.get('region', {}).get('name'),
                'image': droplet.get('image', {}).get('name'),
                'ip_address': public_ip,
                'tags': droplet.get('tags', [])
            })
        
        return {
            'body': {
                'droplets': json.dumps(droplet_info),
                'count': len(droplet_info),
                'status': 'success'
            }
        }
        
    except Exception as e:
        return {
            'body': {
                'droplets': json.dumps([]),
                'count': 0,
                'status': 'error',
                'error': str(e)
            }
        }

# For local testing
if __name__ == "__main__":
    import sys
    
    # Example 1: List droplets (default behavior)
    test_args_list = {
        'limit': 5
    }
    
    # Example 2: Power on a specific droplet
    test_args_power_on = {
        'droplet_id': 12345,  # Replace with actual droplet ID
        'action': 'power_on'
    }
    
    # Example 3: Power off a specific droplet
    test_args_power_off = {
        'droplet_id': 12345,  # Replace with actual droplet ID
        'action': 'power_off'
    }
    
    # Choose which example to run
    # Uncomment the test_args you want to use
    test_args = test_args_list
    # test_args = test_args_power_on
    # test_args = test_args_power_off
    
    result = main(test_args)
    print(json.dumps(result, indent=2))