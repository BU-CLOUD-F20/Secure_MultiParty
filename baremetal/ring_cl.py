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
iface =[]

# Create selected number of nodes
for i in range(params.node_count):
    node.append(request.RawPC('node-%d' % i))
    node[-1].disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD'
    node[-1].hardware_type = params.node_type
    
# Create two interfaces for each node
for i in range(params.node_count):
    iface.append(node[i].addInterface('interface-%d' % i))
    iface.append(node[i].addInterface('interface-%d' % (i+3)))

# Create links between each node
for i in range(params.node_count):
    link.append(request.Link('link-%d' % i))
    
for i in range(params.node_count):
    link[i].addInterface(iface[i])
    link[i].addInterface(iface[i+3])
    link[i].link_multiplexing = True
    link[i].best_effort = True

# Print the generated rspec
pc.printRequestRSpec(request)
