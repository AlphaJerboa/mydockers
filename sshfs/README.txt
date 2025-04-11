= Usage

== Server

./data should be owned by root due to chroot requirements
./data/upload should be owned by the user


== Client
mkdir /<my_mount_point>

sshfs -v -o ssh_command='ssh -T' -o PubkeyAuthentication=yes -o IdentityFile=~/.ssh/<my_private_key> -p 2222 sshfsuser@127.0.0.1:/ /<my_mount_point>

