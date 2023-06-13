from datetime import datetime
import account
import argparse
import dotenv
import csv

# aws-list-ebs
# Generates a comma-delimited (CSV) file listing all EBS volumes within the specified AWS account.

# Setup command-line arguments


def setup_cli_args():
    parser = argparse.ArgumentParser(
        description='Creates a comma-delimited (CSV) file listing all EBS volumes in the specified account.')

    parser.add_argument(
        "-p", "--profile", dest="profile", help="A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes.")

    parser.add_argument(
        "-r", "--region", help="Set a region if not already included in profile.", dest="region")

    parser.add_argument(
        "-o", "--output", help="Output (CSV) filename.", dest="output", default="volumes.csv")

    return parser.parse_args()


# Displays startup paramters
def display_startup_parameters(args):
    print("*******************************************")
    print("  Region:     {0}".format(args.region))

    if (args.profile is None):
        print("  Profile:    Using env configuration")
    else:
        print("  Profile:    {0}".format(args.profile))

    print("  Date:       {0}".format(datetime.now().strftime("%c")))
    print("  Output:     {0}".format(args.output))
    print("*******************************************")

# Display AWS Account settings


def display_account_info(account):
    print("Processing...")
    print("  Account ID: {0}".format(account.account_id))
    print("  Region:     {0}".format(account.session.region_name))

    if (account.profile_name is None):
        print("  Profile:    Using env configuration")
    else:
        print("  Profile:    {0}".format(account.profile_name))

# Creates a CSV file with EBS Volume information


def write_csv_file(filename, rows, field_names):
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(field_names)
            writer.writerows(rows)
    except BaseException as e:
        print('An error occurred when writing to ', filename)
    else:
        print("{0} rows successfully saved to {1}\r\n".format(len(rows), filename))

# Returns a list of EBS Volume details for each of the EBS Volumes in the specified account


def get_ebs_volume_details(client, account_id, region_name):
    # Get a list of all EBS Volumes
    volume_details = client.describe_volumes()
    volume_rows = []

    for volume in volume_details['Volumes']:
        iops = ''
        name = ''
        drive = ''
        instance_id = ''
        device = ''
        state = ''
        tags = ''

        if (volume['VolumeType'] != 'standard'):
            iops = volume['Iops']

        if ('Tags' in volume):
            for tag in volume['Tags']:
                tags += tag['Key'] + ":" + tag['Value'] + ","

                if (tag['Key'] == 'Name'):
                    name = tag['Value']

                if (tag['Key'] == 'drive'):
                    drive = tag['Value']
        if (len(tags) > 0):
            tags = tags.rstrip(',')

        for attachment in volume['Attachments']:
            if ('InstanceId' in attachment):
                instance_id = attachment['InstanceId']

            if ('Device' in attachment):
                device = attachment['Device']

            if ('State' in attachment):
                state = attachment['State']

        ec2_arn = "arn:aws:ec2:{0}:{1}:{2}/{3}".format(
            region_name,
            account_id,
            "instance",
            instance_id
        )

        volume_arn = "arn:aws:ec2:{0}:{1}:{2}/{3}".format(
            region_name,
            account_id,
            "volume",
            volume['VolumeId']
        )

        volume_rows.append([
            account_id,
            ec2_arn,
            instance_id,
            volume_arn,
            volume['VolumeId'],
            name,
            device,
            drive,
            volume['VolumeType'],
            volume['Size'],
            iops,
            state,
            tags])

    return volume_rows


# load the environment variables
dotenv.load_dotenv()

# Get command-line arguments
args = setup_cli_args()

# Get the list of comma-delimited profiles
profiles = args.profile.split(',')

# Initialize the list that will hold each data row
volume_rows = []

display_startup_parameters(args)

# Iterate over all AWS profiles and concatenate the data
for profile in [p.strip() for p in profiles]:
    # Create AWS Account object using the profile name specified
    aws_account = account.Account(profile, args.region)

    display_account_info(aws_account)

    rows = list(get_ebs_volume_details(aws_account.session.client(
        'ec2'), aws_account.account_id, aws_account.region_name))

    print("{0} rows processed.\r\n".format(len(rows)))

    volume_rows.extend(rows)

field_names = ['Account ID', 'EC2 ARN', 'EC2 Instance ID', 'Volume ARN',
               'Volume ID', 'Name', 'Device', 'Drive', 'Type', 'Size', 'IOPS', 'State', 'Tags']

write_csv_file(args.output, volume_rows, field_names)
