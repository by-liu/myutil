
ssh-keygen -t rsa

cat ~/.ssh/id_rsa.pub | ssh $1 "mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys"
