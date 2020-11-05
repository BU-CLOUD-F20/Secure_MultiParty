# Accessing a Second VM with SSH Agent Forwarding

1. While we can ssh to an initial VM on OpenStack when we associate it with a floating IP address (e.g. `ssh -i ~/.ssh/moc.key -A pwolfe@128.31.25.149`) we only have a limited number of floating IP addresses. The solution to access other VMs on our private subnet on OpenStack is to ssh through the first VM
1. A clean way of accomplishing this without copying keys to the first VM or changing the settings to allow password based login on the other VMs is through SSH Agent Forwarding.
1. Following the suggestions on [this MOC guide page](https://docs.massopen.cloud/en/latest/openstack/Troubleshooting-SSH-login.html?highlight=ssh-agent) (despite being marked as deprecated) we can accomplish this. An example follows:
```
# Check that ssh-agent is launched
ps -aux | grep ssh-agent
# If it isn't launched or is not responding, launch the agent, otherwise skip ahead
ssh-agent > agent_variables.tmp
source agent_variables.tmp
rm agent_variables.tmp
# Add the MOC authentication key (the one used to access the VM on the floating IP)
# e.g. ssh-add ~/.ssh/moc.key
ssh-add ~/.ssh/<private_key_filename>
# Check that the key was added
ssh-add -l
# SSH to the first VM making sure to forward the agent
# Note: rather than using the -A flag permitted hosts for forwarding can be configured in ~/.ssh/config
# e.g. ssh -A pwolfe@128.31.25.149
ssh -A <user>@<VM_IP_address>
# To verify that the agent was forwarded properly there should be an output for the following command entered on the first VM
echo $SSH_AUTH_SOCK
# If this worked properly, attempt to ssh to another VM using its subnet address
# e.g. ssh 192.168.100.22
ssh <VM_IP_address_2>
```
Note: see add_key_to_agent.sh at the top level of the repository for a script that can be minimally tweaked for easier logging into VMs on OpenStack.
