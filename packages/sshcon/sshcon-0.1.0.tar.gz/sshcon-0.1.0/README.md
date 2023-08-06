# sshcon ⚡

> Python SSH connector for linux systems

Very simple python SSH connector for linux systems based on super fast SSH2 protocol library -> [ssh2-python][https://github.com/ParallelSSH/ssh2-python].

## Installation

```shell
pip install sshcon
```

## How to use

```python
from sshcon.main import SshCon


hostname = "myserver"
ssh_user = "myuser"
ssh_ke = ".ssh/mykey"
ssh = SshConn(hostname, ssh_user, ssh_key)

# Run command and save output to the variable
ls = ssh.run(["ls", "-latr", path("/mnt"], capture_output=True, check=True).stdout

# Mount directory
ssh.mount(source="storage:/data", "/mnt", force=True, mkdir=True)

# Remove files
ssh.remove("/my/folder/*.tar", force=True)

# Read text
text = ssh.read_text("/folder/text.txt")

# Write text
ssh.write_text("Ahoj", "/folder/text.txt")

# Check if file
if ssh.isfile("/my/file):
    print("It's a file!")
```

## Todo

- [ ] Add readthedocs
- [ ] Update readme
