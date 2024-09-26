#!/usr/bin/env python

import boto3
import os
import sys
from download_policies import download_policies
from verify_policies import check_all_policies
from policy_usage import find_iam_principals_by_policy

if __name__ == "__main__":
    aws_region = 'us-east-1'
    
    if len(sys.argv) < 2:
     print("Usage ./cdiamp.py <profile-name>")
     exit(1)

    aws_profile = sys.argv[1]

    OUTPUT_DIR = f"results/{aws_profile}/iam-policies"
    OUTPUT_FILE_RISKY_POLICIES = f"results/{aws_profile}/identified_risky_policies.csv"

    boto3.setup_default_session(profile_name=aws_profile, region_name=aws_region)
    iam_client = boto3.client('iam')

    # check if folder already exists and it is not empty
    if not os.path.isdir(OUTPUT_DIR) or not os.listdir(OUTPUT_DIR):
        # we download the policies
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        download_policies(iam_client, OUTPUT_DIR)

    # only if file not exists we check
    if not os.path.exists(OUTPUT_FILE_RISKY_POLICIES):
        check_all_policies(OUTPUT_DIR, OUTPUT_FILE_RISKY_POLICIES)

    with open(OUTPUT_FILE_RISKY_POLICIES, 'r') as file:
        for line in file:
            policy_name, policy_arn, risky_permission = line.split(';')
            output_file_principals = f"results/{aws_profile}/{policy_name}_principals.csv"
            find_iam_principals_by_policy(policy_arn, output_file_principals)
