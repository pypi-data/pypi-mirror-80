# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import argparse
import sys

from ec2instanceconnectcli.EC2InstanceConnectCLI import EC2InstanceConnectCLI
from ec2instanceconnectcli.EC2InstanceConnectCommand import EC2InstanceConnectCommand
from ec2instanceconnectcli.EC2InstanceConnectLogger import EC2InstanceConnectLogger
from ec2instanceconnectcli import input_parser

DEFAULT_INSTANCE = ''
DEFAULT_PROFILE = None

def main(program, mode):
    """
    Parses system arguments sets defaults
    Calls `putty or psftp` to SSH or do file operations using EC2InstanceConnect.

    :param program: Client program to be used for SSH/SFTP operations.
    :type program: basestring
    :param mode: Identifies either SSH/SFTP operation.
    :type mode: basestring
    :return: Return code for remote command
    :rtype: int
    """

    usage = ""
    if mode == "ssh":
        usage = """
            mssh-putty [-t instance_id] [-u profile] [-r region] [-z availability_zone] [-i identity_file_ppk] [supported putty flags] target

            target                  => [user@]instance_id | [user@]dns_name
            [supported putty flags] => [-l login_name] [ -P port] [-m remote_command_file]
        """
    elif mode == "sftp":
        usage = """
            msftp-putty [-t instance_id] [-u profile] [-r region] [-z availability_zone] [-i identity_file_ppk] [supported psftp flags] target

            target                  => [user@]instance_id | [user@]dns_name
            [supported psftp flags] => [-l login_name] [ -P port] [-bc] [-b batchfile]
        """

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-r', '--region', action='store', help='AWS region', type=str, metavar='')
    parser.add_argument('-z', '--zone', action='store', help='Availability zone', type=str, metavar='')
    parser.add_argument('-i', '--identity', action='store', help="Required. Identity file in ppk format", type=str, required=True, metavar='')
    parser.add_argument('-u', '--profile', action='store', help='AWS Config Profile', type=str, default=DEFAULT_PROFILE, metavar='')
    parser.add_argument('-t', '--instance_id', action='store', help='EC2 Instance ID.  Required if target is hostname', type=str, default=DEFAULT_INSTANCE, metavar='')
    parser.add_argument('-d', '--debug', action="store_true", help='Turn on debug logging')

    args = parser.parse_known_args()

    #Read public key from ppk file.
    #Public key is unencrypted and in rsa format.
    pub_key_lines = []
    pub_key = "ssh-rsa "
    try:
        with open(args[0].identity, 'r') as f:
            pub_key_lines = f.readlines()

        #Validate that the identity file format is ppk.
        if pub_key_lines[0].find("PuTTY-User-Key-File-") == -1:
            print("Not a valid Putty key.")
            sys.exit(1)

        #public key starts from 4th line in ppk file.
        line_len = int(pub_key_lines[3].split(':')[1].strip())
        pub_key_lines = pub_key_lines[4:(4+line_len)]
        for pub_key_line in pub_key_lines:
            pub_key += pub_key_line[:-1]
    except Exception as e:
        print(str(e))
        sys.exit(1)

    logger = EC2InstanceConnectLogger(args[0].debug)
    try:
        instance_bundles, flags, program_command = input_parser.parseargs(args, mode)
    except Exception as e:
        print(str(e))
        parser.print_help()
        sys.exit(1)

    cli_command = EC2InstanceConnectCommand(program, instance_bundles, args[0].identity, flags, program_command, logger.get_logger())
    cli_command.get_command()

    try:
        mssh = EC2InstanceConnectCLI(instance_bundles, pub_key, cli_command, logger.get_logger())
        return mssh.invoke_command()
    except Exception as e:
        print("Failed with:\n" + str(e))
        sys.exit(1)
