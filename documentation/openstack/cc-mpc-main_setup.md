# Summary of steps for fresh VM

The following commands were used to configure dependencies and enable access by all the team members to the primary VM on OpenStack. The following commands are an example as taken from a particular user perspective.

```
# SSH to VM provisioned as described in moc_vm_creation.md
ssh -i ~/.ssh/moc.key pwolfe@128.31.25.149

# Configuring cc-mpc-main from the ubuntu account
sudo apt update
sudo apt upgrade
sudo apt install build-essential openmpi-bin libsodium23 libsodium-dev
sudo apt autoclean
sudo apt autoremove
sudo useradd -m -s /bin/bash -G sudo pwolfe
sudo mkdir /home/pwolfe/.ssh
sudo cp /home/ubuntu/.ssh/authorized_keys /home/pwolfe/.ssh/
sudo chown -hR pwolfe:pwolfe /home/pwolfe/.ssh

sudo useradd -m -s /bin/bash -G sudo sjain
sudo mkdir /home/sjain/.ssh
sudo nano /home/sjain/.ssh/authorized_keys
# copy and paste key then save
sudo chown -hR sjain:sjain /home/sjain/.ssh
sudo chmod 600 /home/sjain/.ssh/authorized_keys
sudo chmod 755 /home/sjain/.ssh
sudo passwd sjain
# enter default password

sudo useradd -m -s /bin/bash -G sudo hrehman
sudo mkdir /home/hrehman/.ssh
sudo nano /home/hrehman/.ssh/authorized_keys
# copy and paste key then save
sudo chown -hR hrehman:hrehman /home/hrehman/.ssh
sudo chmod 600 /home/hrehman/.ssh/authorized_keys
sudo chmod 755 /home/hrehman/.ssh
sudo passwd hrehman
# enter default password

sudo useradd -m -s /bin/bash -G sudo ylin
sudo mkdir /home/ylin/.ssh
sudo nano /home/ylin/.ssh/authorized_keys
# copy and paste key then save
sudo chown -hR ylin:ylin /home/ylin/.ssh
sudo chmod 600 /home/ylin/.ssh/authorized_keys
sudo chmod 755 /home/ylin/.ssh
sudo passwd ylin
# enter default password

sudo useradd -m -s /bin/bash -G sudo shu
sudo mkdir /home/shu/.ssh
sudo nano /home/shu/.ssh/authorized_keys
# copy and paste key then save
sudo chown -hR shu:shu /home/shu/.ssh
sudo chmod 600 /home/shu/.ssh/authorized_keys
sudo chmod 755 /home/shu/.ssh
sudo passwd shu
# enter default password

# Shutdown and restart
sudo shutdown -r now

# Upon reboot, copy codebase and build/test using makefiles (example copy with scp below)
scp -r -i ~/.ssh/moc.key ccproject pwolfe@128.31.25.149:/home/pwolfe/
```
