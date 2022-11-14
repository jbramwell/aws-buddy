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
        "-p", "--profile", dest="profile", help="Specifies the AWS profile (from credentials file) to be used.")

    parser.add_argument(
        "-v", "--verbose", help="Verbose output.", action="store_true", dest="verbose", default=False)

    parser.add_argument(
        "-r", "--region", help="Set a region if not already included in profile.", dest="region")

    parser.add_argument(
        "-o", "--output", help="Output (CSV) filename.", dest="output", default="volumes.csv")

    return parser.parse_args()


# Displays startup paramters
def display_startup_parameters(args, account):
    print("*******************************************")
    print(" Account ID: {0}".format(account.account_id))
    print(" Region:     {0}".format(account.session.region_name))

    if (account.profile_name is None):
        print(" Profile:    Using env configuration")
    else:
        print(" Profile:    {0}".format(account.profile_name))

    print(" Date:       {0}".format(datetime.now().strftime("%c")))
    print(" Output:     {0}".format(args.output))
    print(" Verbose:    {0}".format(args.verbose))
    print("*******************************************")

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
        print("Results successfully saved to {0}".format(filename))

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

        if (volume['VolumeType'] != 'standard'):
            iops = volume['Iops']

        if ('Tags' in volume):
            for tag in volume['Tags']:
                if (tag['Key'] == 'Name'):
                    name = tag['Value']

                if (tag['Key'] == 'drive'):
                    drive = tag['Value']

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
            state])

    return volume_rows


# load the environment variables
dotenv.load_dotenv()

# Get command-line arguments
args = setup_cli_args()

# Create AWS Account object using the profile name specified
aws_account = account.Account(args.profile, args.region)

display_startup_parameters(args, aws_account)

volume_rows = list(get_ebs_volume_details(aws_account.session.client('ec2'), aws_account.account_id, aws_account.region_name))

field_names = ['Account ID', 'EC2 ARN', 'EC2 Instance ID', 'Volume ARN', 'Volume ID', 'Name', 'Device', 'Drive', 'Type', 'Size', 'IOPS', 'State']

write_csv_file(args.output, volume_rows, field_names)
