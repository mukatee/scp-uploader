__author__ = 'teemu kanstren'

import configparser
from file_data import FileData
from argparse import ArgumentParser
# pip install scp for paramiko
import paramiko
from scp import SCPClient
import os
import sys

#attribute names for configuration file
KEY_DESTINATION_IP="dst_ip"
KEY_DESTINATION_PORT="dst_port"
KEY_DESTINATION_DIR="dst_dir"
KEY_SOURCE_DIR="src_dir"
KEY_FILE_PREFIX="file_prefix"
KEY_FILE_POSTFIX="file_postfix"
KEY_FILE_NAMES="file_names"
KEY_SECTIONS="sections"

#find files matching a given prefix and postfix from a path
#http://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string
def find_files_from_path(path, prefix, postfix):
    try:
        files = os.listdir(path)
    except FileNotFoundError as e:
        error = "Failed to load filelist for path '" + path + "': " + str(e) + "."
        return error, None
    return find_files_from_list(path, files, prefix, postfix)


#find file names from given list, matching a given prefix and postfix
def find_files_from_list(path, files, prefix, postfix):
    if len(files) == 0:
        error = "Empty file list, cannot search for files."
        return error, None
    if prefix is not None:
        files = [filename for filename in files if filename.startswith(prefix)]
    if postfix is not None:
        files = [filename for filename in files if filename.endswith(postfix)]
    if len(files) < 1:
        if prefix is not None and postfix is None:
            error = "Could not find file starting with '" + prefix + "'."
        elif prefix is None and postfix is not None:
            error = "Could not find file ending with '" + postfix + "' in path '" + path + "'."
        elif prefix is not None and postfix is not None:
            error = "Could not find file starting with '" + prefix + "' and ending with '" + postfix + "' in path '" + path + "'."
        else:
            error = "Could not find any files in path '" + path + "'"
        return error, None
    return None, files


def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def upload_file(ssh, localpath, remotepath):
    mkdir_p(ssh, remotepath)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(localpath, remotepath)


def upload_dir(ssh, localpath, remotepath):
    local_dirpath = os.path.join(localpath)
    #    local_libpath = os.path.join(localpath, filename)
    mkdir_p(ssh, remotepath)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_dirpath, remotepath, recursive=True)


# http://stackoverflow.com/questions/14819681/upload-files-using-sftp-in-python-but-create-directories-if-path-doesnt-exist
def mkdir_p(ssh, remote_directory):
    with paramiko.SFTPClient.from_transport(ssh.get_transport()) as sftp:
        dir_path = str()
        for dir_folder in remote_directory.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"/{0}".format(dir_folder)
            try:
                sftp.listdir(dir_path)
            except IOError:
                sftp.mkdir(dir_path)


#process a target group, expanding defined sections to actual file lists and combining those
def process_group(config, target, processed):
    print("expanding group: '" + target + "'")
    options = config.options(target)
    if len(options) > 1:
        print("NOTE: Deployment target '" + target + "' has '"+KEY_SECTIONS+"' defined with other attributes. When '"+KEY_SECTIONS+"' is defined, other attributes are ignored.")
    targets = config.get(target, KEY_SECTIONS).split(',')
    error = None
    files = []
    dir_names = []
    for group_target in targets:
        print("expanding target: '" + group_target + "' for group '" + target + "'")
        if group_target in processed:
            print("already processed target '" + group_target + "', skipping")
            continue
        processed.add(group_target)
        group_error, group_files, group_dirs = create_file_list(config, group_target, processed)
        if group_error is not None:
            if error is None:
                error = group_error
            else:
                error += group_error
        if group_files is not None:
            files.extend(group_files)
        if group_dirs is not None:
            dir_names.extend(group_dirs)
    if len(files) == 0:
        files = None
    return error, files, dir_names


#process a single deployment target (section in config file)
def process_target(config, target):
    files = []
    dir_names=[]
    #we assume here that dst_xxx attributes have been validated already to be present
    dst_ips = config.get(target, KEY_DESTINATION_IP).split(",")
    dst_dir = config.get(target, KEY_DESTINATION_DIR)
    dst_port = config.get(target, KEY_DESTINATION_PORT)

    if config.has_option(target, KEY_SOURCE_DIR):
        src_dir = config.get(target, KEY_SOURCE_DIR)
        file_postfix = None
        file_prefix = None
        error = None
        if config.has_option(target, KEY_FILE_POSTFIX):
            file_postfix = config.get(target, KEY_FILE_POSTFIX)
        if config.has_option(target, KEY_FILE_PREFIX):
            file_prefix = config.get(target, KEY_FILE_PREFIX)
        if (file_postfix is not None or file_prefix is not None) and config.has_option(target, KEY_FILE_NAMES):
            error = "Target '" + target + "' specifies both pre/postfix and '"+KEY_FILE_NAMES+"'. Remove one. Skipping target."
            return error, None, None
        file_names = []
        if file_prefix is not None or file_postfix is not None:
            error, file_names = find_files_from_path(src_dir, file_prefix, file_postfix)
        elif config.has_option(target, KEY_FILE_NAMES):
            file_names = config.get(target, KEY_FILE_NAMES).split(",")
        else:
            #upload whole dir recursively
            if not os.path.isdir(src_dir):
                error = "Directory '"+src_dir+"' not found (or is not a directory)."
                return error, None, None
            for dst_ip in dst_ips:
                dir_names.append(FileData(dst_ip, src_dir, dst_dir, dst_port))
            #error, file_names = find_files_from_path(src_dir, None, None)
        if error is not None:
            error = error + " Skipping deployment target '" + target + "'."
            return error, None, None
        for file_name in file_names:
            src_path = os.path.join(src_dir, file_name)
            dst_path = dst_dir
            # dst_path = os.path.join(dst_dir, file_name)
            for dst_ip in dst_ips:
                files.append(FileData(dst_ip, src_path, dst_path, dst_port))
    elif config.has_option(target, KEY_FILE_NAMES):
        file_names = config.get(target, KEY_FILE_NAMES)
        for file_name in file_names:
            for dst_ip in dst_ips:
                files.append(FileData(dst_ip, file_name, dst_dir, dst_port))
    if len(files) == 0 and len(dir_names) == 0:
        error = "Nothing to upload found for target '" + target + "'"
        return error, None, None
    return None, files, dir_names


#check the given configuration has minimum defined settings to progress. checks only they have some definition regardless of content.
def validate_input(config, target, processed):
    if target not in config:
        error = "Key '" + target + "' not found in configuration."
        return error

    if not config.has_option(target, KEY_DESTINATION_IP):
        error = "Configuration component '" + target + "' does not have '"+KEY_DESTINATION_IP+"' defined. Skipping."
        return error

    if not config.has_option(target, KEY_DESTINATION_DIR):
        error = "Configuration component '" + target + "' does not have '"+KEY_DESTINATION_DIR+"' defined. Skipping."
        return error

    if not config.has_option(target, KEY_DESTINATION_PORT):
        error = "Configuration component '" + target + "' does not have '"+KEY_DESTINATION_PORT+"' defined. Skipping."
        return error

    if not config.has_option(target, KEY_SOURCE_DIR) and not config.has_option(target, KEY_FILE_NAMES):
        error = "Configuration component '" + target + "' does not have '"+KEY_SOURCE_DIR+"' or '"+KEY_FILE_NAMES+"' defined. Skipping."
        return error

    return None


def create_file_list(config, target, processed):
    target = target.strip()

    if config.has_option(target, KEY_SECTIONS):
        return process_group(config, target, processed)

    error = validate_input(config, target, processed)
    if error is not None:
        return error, None, None

    return process_target(config, target)


#parse deployment arguments as given from command line
def parse_args(sys_args):
    parser = ArgumentParser(
        description='Upload files and directories to remote host over SCP. Creates remote dirs if needed. Configuration in config.ini file.')
    parser.add_argument('-u', '--username', help='SSH username.')
    parser.add_argument('-p', '--password', help='SSH password.')
    #    parser.add_argument('-u', '--username', help='SSH username.', required=True)
    #    parser.add_argument('-p', '--password', help='SSH password.', required=True)
    parser.add_argument('-c', '--configfile', help='Configuration filename.', default='config.ini')
    parser.add_argument('-l', '--list', help='Lists the target values found in configuration file.', action='store_true')
    parser.add_argument('target',
                        #                        choices=('all', '<component_name>'),
                        help='Name of component to deploy. Use "all" to deploy all at once.".',
                        nargs="?")

    args = parser.parse_args(sys_args)

    if args.username == None or args.password == None:
        if args.list == False:
            error = "You need to specify either -l/--list or both -u/--username and -p/--password"
            sys.stderr.write(error)
            # parser.error(error)
            parser.print_usage()
            return error, args, None

    if args.username is not None and args.password is not None and args.target is None:
        error = "No deployment target specified. Doing nothing."
        return error, args, None

    config = configparser.ConfigParser()
#    config = configparser.ConfigParser(os.environ)
    config.read(args.configfile)
    sections = config.sections()
    if len(sections) == 0:
        error = "Unable to read content from config file '" + args.configfile + "'"
        return error, args, config
    # choise_list = ['all'] + sections
    # tests: file not found, target not found,
    if args.list == True:
        msg = "Targets found for '" + args.configfile + "': " + str(sections)
        print(msg)
        return msg, args, config
    return None, args, config


#create a list of all files/dirs to upload for all the given deployment targets
def create_total_filelist(config, targets):
    all_files = []
    all_dirs = []
    processed = set()
    for target in targets:
        print("processing deployment target '" + target + "'")
        processed.add(target)
        error, files, dir_names = create_file_list(config, target, processed)
        if error is not None:
            print(error)
        if files is not None:
            all_files.extend(files)
        if dir_names is not None:
            all_dirs.extend(dir_names)

    result_files = []
    for file in all_files:
        if file not in result_files:
            result_files.append(file)
        else:
            print('skipping duplicate file '+str(file)+"'")

    result_dirs = []
    for dir in all_dirs:
        if dir not in result_dirs:
            result_dirs.append(dir)
        else:
            print('skipping duplicate dir ' + str(dir) + "'")

    #the following is a trick to remove duplicates while preserving order (maybe useful to ensure something uploads first)
    #http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    #seen = set()
    #the "or" part of this seems to be only a trick to have seen.add() called only once when "file in seen" is false. set.add() returns nothing
    #result = [file for file in all_files if not (file in seen or seen.add(file))]
    return result_files, result_dirs


#try to actually deploy the given deployment target using the given configuration over ssh/scp
def deploy(args, config):
    if args.target == 'all':
        targets = config.sections()
    else:
        targets = [args.target]
    all_files, all_dirs = create_total_filelist(config, targets)

    #first we just print the list of found files and directories to give the user idea what they just triggered.
    #also collect count of files for logging upload progress
    f = 1
    print("final list of files to upload:")
    for file in all_files:
        print(str(f)+". "+str(file))
        f += 1
    f -= 1

    d = 1
    print("final list of dirs to upload:")
    for dir in all_dirs:
        print(str(d) + ". " + str(dir))
        d += 1
    d -= 1

    f2 = 1
    for file in all_files:
        print("uploading file "+str(f2)+"/"+str(f)+". "+str(file))
        ssh = create_ssh_client(file.dst_ip, file.dst_port, args.username, args.password)
        upload_file(ssh, file.src_path, file.dst_path)
        f2 += 1

    d2 = 1
    for dir in all_dirs:
        print("uploading dir " + str(d2) + "/" + str(d) + ". " + str(dir))
        ssh = create_ssh_client(dir.dst_ip, dir.dst_port, args.username, args.password)
        upload_dir(ssh, dir.src_path, dir.dst_path)
        d2 += 1


if __name__ == "__main__":
    error, args, config = parse_args(sys.argv[1:])
    if error is not None:
        exit()

    deploy(args, config)
