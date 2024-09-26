# CDIAMP - Check Dangerous IAM Permissions in AWS

**Note**: Currently in version 0.0.1 only for fast and easy use. Only recommended if you know what are you looking for.

## Introduction

This tool is based in the HackTrick's list of dangerous AWS permissions available at:
[Hacktricks | AWS - IAM Privesc](https://cloud.hacktricks.xyz/pentesting-cloud/aws-security/aws-privilege-escalation/aws-iam-privesc)

Each one of those permissions could leads to an insecure permission and it is recommended to address the potential issue.

## Usage

First, you need to create an AWS user with programmatic access and assign it the AWS Managed Policy [SecurityAudit](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/SecurityAudit.html).

Then, configure an AWS profile with the access and secret key of that user.

```sh
aws configure --profile <profilename>
```

Create the virtual environment for the dependency libraries

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Finally, run the tool with the profile name as parameter.

```sh
./cdiamp.py <profilename>
```

## What does it do this tool?

1. It creates a folder with the profile name.
2. It downloads all the policies available in the AWS account to the folder `results/<profilename>/iam-policies`.
3. Performs an iteration over the list of dangerous permissions and it checks if it exists. Yeah, I know it is a raw search, but it will work most if not all times.
4. If there is a match, it will generate a csv file, `results/<profilename>/identified_risky_policies.csv` with the following format:

```csv
Policy Name;Policy ARN;Dangerous Permission
```

5. Then, for each match, it will search who is using the policy (Principals) and generate one file for each policy with the name `<policy name>_principals.csv`. This file will have the following format:

```csv
Policy ARN;Type of Principal;Principal Name
```

Where the principals could be:

-   User
-   Group
-   Role

## ToDo

-   [ ] Consider Wildcards in the actions.
-   [ ] Identify if the dangerous permission is related to an `Allow` effect in the policy.
-   [ ] Configure more input arguments, like the destination folder.
-   [ ] Allow the usage of access keys for performing the API calls instead of configure a profile.
-   [ ] Check if there are policy versions and verify on those too.
-   [ ] Add header rows for output files.
-   [ ] Do not create empty files if there isn't any principal related to a risky permission.
-   [ ] Modify the file `identified_risky_policies.csv` to have more info such as how many principals are related to the policy.
-   [ ] Any suggestion you may have!
