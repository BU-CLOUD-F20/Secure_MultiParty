"""ubuntu baremetal multi-site LAN"""


# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

pc = portal.Context()

pc.defineParameter("node_type_1", "Hardware Type for Site 1",
                   portal.ParameterType.NODETYPE, "any")
pc.defineParameter("node_type_2", "Hardware Type for Site 2",
                   portal.ParameterType.NODETYPE, "any")
pc.defineParameter("node_count", "Number of Machines",
                   portal.ParameterType.INTEGER, 3)

params = pc.bindParameters()

request = portal.context.makeRequestRSpec()

node = []

# Create selected number of nodes
for i in range(params.node_count):
    node.append(request.RawPC('node-%d' % i))
    node[i].disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD'
    if (i < params.node_count - 1):     #Condition can be changed based on requirement
        node[i].Site("Site1")
        node[i].hardware_type = params.node_type_1
    else:
        node[i].Site("Site2")
        node[i].hardware_type = params.node_type_2

# Create a LAN for all the connections
lan = request.LAN("lan")
lan.bandwidth = 100000

# Create a link between each of the nodes to make a ring
for i in range(params.node_count):
    iface = node[i].addInterface("eth1")
    iface.addAddress(pg.IPv4Address("192.168.1."+str(i+1), "255.255.255.0"))
    lan.addInterface(iface)

# Install and execute scripts on each node
#for i in range(params.node_count):
#    node[i].addService(pg.Install(url="https://www.dropbox.com/s/45bcc0k861h82kg/cloudlab_setup.tar.gz", path="/home/mpc"))
#    node[i].addService(pg.Execute(shell="bash", command="/home/mpc/cloudlab_setup/setup.sh"))

# Print the generated rspec
pc.printRequestRSpec(request)
