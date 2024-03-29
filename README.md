# AWS Buddy

A collection of Python scripts for listing information about AWS EC2s, Dedicated Hosts, and EBS Volumes.

# aws-list-ebs

Generates a list of all EBS Volumes in the specified AWS Account(s) and saves them to a comma-delimited (CSV) file.

## Data Fields

The following fields are included in the results:
- Account ID
- Device
- Drive
- EC2 ARN
- EC2 Instance ID
- IOPS
- Name
- Size
- State
- Tags
- Type
- Volume ARN
- Volume ID

## Usage

Usage: `python aws-list-volumes.py [-h] [-p PROFILE] [-o OUTPUT] [-r REGION]`

| switch |           | description                                                         |
|--------|-----------|:--------------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                                    |
| -p     | --profile | A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes. |
| -o     | --output  | The name of the file to write the comma-separated (CSV) results to. |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).   |

## Examples

Generates a comma-delimited (CSV) file listing all EBS volumes within the AWS Account configured in the *production* profile:
    
`python aws-list-ebs.py -p production -r us-east-1 -o volumes.csv `

Generates a comma-delimited (CSV) file listing all EBS volumes within the AWS accounts configured in the *production* and *non-prod* profiles:
    
`python aws-list-ebs.py -p "non-prod,production" -r us-east-1 -o volumes.csv `

# aws-list-dedicated-hosts

Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the specified AWS Account(s).

## Data Fields

The following fields are included in the results:

- Account ID
- Available Instance Capacity
- Available vCPUs
- Availability Zone
- EC2 ARN
- EC2 Instance ID
- EC2 Instance Type
- EC2 Name
- Host ID
- Host Name
- Host Reservation ID
- Instance Type
- Total Instance Capacity

## Usage

Usage: `python aws-list-dedicated-hosts.py [-h] [-p PROFILE] [-o OUTPUT] [-r REGION]`

| switch |           | description                                                         |
|--------|-----------|:--------------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                                    |
| -p     | --profile | A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes. |
| -o     | --output  | The name of the file to write the comma-separated (CSV) results to. |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).   |

## Examples

Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the AWS account configured in the *production* profile:
    
`python aws-list-dedicated-hosts.py -p production -r us-east-1 -o volumes.csv `

Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the AWS accounts configured in the *production* and *non-prod* profiles:
    
`python aws-list-dedicated-hosts.py -p "non-prod,production" -r us-east-1 -o volumes.csv `

# aws-tag-resources

Tags all (taggable) resources within an AWS account based on input filters and saves the results to a comma-delimited (CSV) file.

## Data Fields

The following fields are included in the results:

- Status Code
- Error Code
- Error Message
- Account ID
- Resource ARN
- Resource ID
- Service
- Region
- Resource Type
- Tags

## Usage

Usage: `python aws-tag-resources.py [-h] [-p PROFILE] [-o OUTPUT] [-r REGION] [-s SERVICES] [-f FILTER] [-e yes] -t "TAG=VALUE"`

| switch |            | description                                                         |
|--------|------------|:--------------------------------------------------------------------|
| -h     | --help     | Show this help message and exit.                                    |
| -t     | --tags     | A comma-separated list of key/value pairs for tags to be updated. The key/value list must be enclosed in quotes. |
| -s     | --services | A comma-separated list of AWS Services for which the Tags should be updated. |
| -f     | --filter   | The text specified within 'filter' must appear within the resource ARN to be tagged. |
| -x     | --eXecute  | By default, this command runs in 'what if' mode. Set this argument to 'yes' to update the tag values. |
| -p     | --profile  | A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes. |
| -o     | --output   | The name of the file to write the comma-separated (CSV) results to. |
| -r     | --region   | Set a region if not already included in profile (e.g. us-east-1).   |

## Examples

Generate a comma-delimited (CSV) file, in a "what if?" mode, for all Amazon S3 resources to be tagged using the *production* profile with an *environment* tag set to *production*:
    
`python aws-tag-resources.py -p production -r us-east-1 -o resources.csv -t "environment=production" -s "s3" -x no `

# Requirements

The following packages need to be installed prior to using this utility:

## boto3

`pip install boto3`

## dotenv

`pip install python-dotenv`

# Profiles

When calling the Python scripts described above, the profile name(s) specified in the -p (PROFILE) switch maps to one or more profiles defined in the AWS *credentials* file, which is located in one of the following locations:

| Operating System | File Location                           |
|------------------|-----------------------------------------|
| Windows          | `%USERPROFILE%\.aws\credentials` |
| Linux & macOS    | `~/.aws/credentials`                    |

Read more in [Shared Config and Credential Files](https://docs.aws.amazon.com/sdkref/latest/guide/file-format.html).
