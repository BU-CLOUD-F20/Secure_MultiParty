"""ubuntu baremetal ring of nodes"""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

pc = portal.Context()

pc.defineParameter("node_type", "Hardware Type",
                   portal.ParameterType.NODETYPE, "any")
pc.defineParameter("node_count", "Number of Machines",
                   portal.ParameterType.INTEGER, 3)

params = pc.bindParameters()

request = portal.context.makeRequestRSpec()

node = []
link = []

# Create selected number of nodes
for i in range(params.node_count):
    node.append(request.RawPC('node-%d' % i))
    node[-1].disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
    node[-1].hardware_type = params.node_type

# Create a LAN for all the connections
lan = request.LAN("lan")

# Create a link between each of the nodes to make a ring
for i in range(params.node_count):
    iface = node[i].addInterface("if1")
    iface.component_id = "eth1"
    iface.addAddress(pg.IPv4Address("192.168.1."+str(i+1), "255.255.255.0"))
    lan.addInterface(iface)

# Install and execute scripts on each node
for i in range(params.node_count):
    node[i].addService(pg.Install(url="https://www.dropbox.com/s/7t91cf0ugt66ypl/cloudlab_setup.tar.gz", path="/home/mpc"))
    node[i].addService(pg.Execute(shell="bash", command="/home/mpc/setup.sh"))

# Print the generated rspec
pc.printRequestRSpec(request)
