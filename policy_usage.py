import boto3

def find_iam_principals_by_policy(policy_arn, output_file_principals):
    iam_client = boto3.client('iam')
    
    # Lists the IAM users, roles, and groups that the specified managed policy is attached to
    response = iam_client.list_entities_for_policy(
        PolicyArn=policy_arn
    )
    
    users = response.get('PolicyUsers', [])
    roles = response.get('PolicyRoles', [])
    groups = response.get('PolicyGroups', [])
    
    with open(output_file_principals, 'w') as file:
        print(f"Policy {policy_arn}:")

        print("* Users:")
        for user in users:
            file.write(f"{policy_arn};User;{user['UserName']}\n")
            print(f"\t- {user['UserName']}", end=", ")

        print(f"\n* Groups:")
        for group in groups:
            file.write(f"{policy_arn};Group;{group['GroupName']}")
            print(f"\t- {group['GroupName']}", end=", ")

        print(f"\n* Roles:")
        for role in roles:
            file.write(f"{policy_arn};Role;{role['RoleName']}")
            print(f"\t- {role['RoleName']}", end=", ")

        print("\n\n")
