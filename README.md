# scp-uploader
Upload filesets over SCP to remote hosts. For deploying code or anything else you might like.

This is a Python script. To use download the [deploy.py](https://github.com/mukatee/scp-uploader/blob/master/src/deploy.py) and [file_data.py](https://github.com/mukatee/scp-uploader/blob/master/src/file_data.py) files.

The possible deployment targets (the stuff to upload) are defined in a config.ini file.
This file should be parseable with Python [ConfigParser](https://docs.python.org/3/library/configparser.html) class.

Following attributes are supported:

- -dst_ip: IP address (or DNS name) for remote host where to upload.
- -dst_dir: Directory on remote host where to store uploaded files/dirs.
- -src_dir: Directory on localhost from which to upload.
- -file_prefix: If a file starts with this in src_dir, upload it.
- -file_postfix: If a file ends with this in src_dir, upload it.
- -file_names: Upload files with exactly these names.
- -sections: For creating upload groups.

Additionally, SSH configuration information needs to be passed on command line parameters:

- -h print help
- -c name of configuration file to load. defaults to "config.ini"
- -u username for SSH login
- -p password for SSH login

For example, a simple configuration might look something like this:

```python
[my_service_config]
dst_ip=192.168.56.101
dst_port=22
dst_dir=/home/randomguy/my_service
src_dir=../my_service
file_names=my_service.properties,hello.xml
```

Assuming this was store in a file called "my_config.ini", the command to run it might be "python deploy.py -u bob -p my_pass -c my_config.ini".
This would try to open an SCP connection to the IP address "192.168.56.101" using the user name "bob" and password "my_pass".
If this is successfull, it would upload the files "my_service.properties" and "hello.xml" from the local directory "../my_service" to a remote
directory "/home/randomguy/my_service". If the remote directory does not exists, and the logger in user has the rights,
the script will try to create that directory before the upload. Any existing file with same name and path will be overwritten.

If no file names are specified, the whole directory is uploaded recursively:

```python
[my_service_lib]
dst_ip=192.168.56.101,service1.target.example
dst_port=22
dst_dir=/home/randomguy/my_service
src_dir=../my_service/lib
```

This would upload the local test_data directory to ""/home/randomguy/my_service/lib" both to the host at IP address 192.168.56.101,
and the other host with DNS name service1.target.example.

It is possible to select a subset of files from a directory using file_prefix and file_postfix attributes:

```python
[my_service_jar]
dst_ip=192.168.56.102
dst_port=22
dst_dir=/home/randomguy/my_service
src_dir=../my_service
file_prefix=service
file_postfix=.jar
```

This would uploader any file starting with "service" and wnding with ".jar".
For example, if you have a dynamic file name with version numbers such as service-0.1.1.jar or service-0.1.2.jar this would handle all the cases.
You may specify either prefix or postfix or both. You may not specify pre/postfix and specific filenames at the same time.

Finally, it is possible to group targets:

```python
[my_service]
sections=my_service_config,my_service_lib,my_service_jar
```

This would upload all files associated with the previous defined "my_service_config", "my_service_lib", and "my_service_jar".
It is also possible to build groups of groups and so on.

As the configuration file is a Python ConfigParser file, all options of that format are available. For example:

```python
[DEFAULT]
remote_host=192.168.56.101
remote_home=/home/t_e_e_m_u
dst_port=22

[full_dir]
dst_ip=%(remote_host)s
dst_dir=%(remote_home)s/testtarget/full_dir/
src_dir=./test_data/
```

This defines all sections to have the dst_port default value of 22 if not specified.
It also defines the "remote_host" and "remote_home" parameters that can be referenced from the rest of the sections.
Convenient if changing the deployment target in many places due to IP address change etc.

Besides the command line, it is also possible to invoke this from Python code:

```python
error, args, config = deploy.parse_args(["-c", "path_to/config_file.ini", "-u", "username", "-p", "password", "target"])
deploy.deploy(args, config)
```

This just emulates the command line arguments so the syntax is exactly the same as for command line.
In this case the configuration file is loaded from "path_to/config_file.ini", the SSH username is given as "username"
and the SSH password as "password". The deployment target (config file section) used is "target".
