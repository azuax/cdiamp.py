import os
import json

def list_policies(iam_client, scope='All'):
    """List all policies (both AWS-managed and customer-managed)"""
    policies = []
    paginator = iam_client.get_paginator('list_policies')
    for page in paginator.paginate(Scope=scope, MaxItems=1000):
        policies.extend(page['Policies'])
    return policies

def get_policy_document(iam_client, policy_arn, version_id):
    """Retrieve the policy document for a specific version"""
    response = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)
    return response['PolicyVersion']['Document']

def save_policy(output_dir, policy, policy_document):
    """Save the policy metadata and document to a JSON file"""
    policy_name = policy['PolicyName']
    policy_filename = f"{policy_name}.json"
    policy_path = os.path.join(output_dir, policy_filename)
    
    # Combine metadata and document
    policy_info = {
        "Policy": policy,
        "PolicyDocument": policy_document
    }
    
    with open(policy_path, 'w') as file:
        json.dump(policy_info, file, indent=4, default=str)
    
    print(f"Policy {policy_name} saved to {policy_path}")

def download_policies(iam_client, output_dir):
    """Main function to download and save all IAM policies"""
    policies = list_policies(iam_client)

    for policy in policies:
        policy_arn = policy['Arn']
        default_version_id = policy['DefaultVersionId']

        # Get the policy document for the default version
        policy_document = get_policy_document(iam_client, policy_arn, default_version_id)


        # Save the policy and its document
        save_policy(output_dir, policy, policy_document)