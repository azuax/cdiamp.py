import json
import os

RISKY_PERMISSIONS = [
    'iam:CreatePolicyVersion',
    'iam:SetDefaultPolicyVersion',
    'iam:CreateAccessKey',
    'iam:CreateLoginProfile',
    'iam:UpdateLoginProfile',
    'iam:UpdateAccessKey',
    'iam:CreateServiceSpecificCredential',
    'iam:ResetServiceSpecificCredential',
    'iam:AttachUserPolicy',
    'iam:AttachGroupPolicy',
    'iam:AttachRolePolicy',
    'iam:createrole',
    'iam:PutUserPolicy',
    'iam:PutGroupPolicy',
    'iam:PutRolePolicy',
    'iam:AddUserToGroup',
    'iam:UpdateAssumeRolePolicy',
    'iam:UploadSSHPublicKey',
    'iam:DeactivateMFADevice',
    'iam:ResyncMFADevice',
    'iam:UpdateSAMLProvider',
    'iam:ListSAMLProviders',
    'iam:GetSAMLProvider',
    'iam:UpdateOpenIDConnectProviderThumbprint',
    'iam:ListOpenIDConnectProviders',
    'iam:GetOpenIDConnectProvider'
]

def check_policy(policy_path):
    with open(policy_path, 'r') as file:
        content = file.read()
        for risky_permission in RISKY_PERMISSIONS:
            policy_json = json.loads(content)
            if risky_permission in content:
                return [policy_json["Policy"]["PolicyName"], policy_json["Policy"]["Arn"], risky_permission]
            else:
                return [policy_json["Policy"]["PolicyName"], policy_json["Policy"]["Arn"], None]

def check_all_policies(policy_dir, output_file_risky_policy):
    risky_policies = []
    for root, dirs, files in os.walk(policy_dir):

        for file in files:
            policy_path = os.path.join(root, file)
            policy_name, policy_arn, risky_policy = check_policy(policy_path)

            print(f"Checked policy {policy_name}")
            if risky_policy:
                risky_policies.append([policy_name, policy_arn, risky_policy])

    if len(risky_policies) > 0:
        with open(output_file_risky_policy, 'w') as file:
            for rp in risky_policies:
                file.write(f"{rp[0]};{rp[1]};{rp[2]}\n")
                print(f"Risky policy {rp[0]} has permission {rp[2]}")
