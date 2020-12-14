"""ubuntu baremetal multi-site ring of nodes"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

pc = portal.Context()

pc.defineParameter("node_type1", "Hardware Type for Site 1",
                   portal.ParameterType.NODETYPE, "any")
pc.defineParameter("node_type2", "Hardware Type for Site 2",
                   portal.ParameterType.NODETYPE, "any")                   
pc.defineParameter("node_count", "Number of Machines",
                   portal.ParameterType.INTEGER, 3)

params = pc.bindParameters()
request = portal.context.makeRequestRSpec()

node = []

# Site 1 - node 0
node0 = request.RawPC('node-0')
node0.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD'
node0.Site("Site1")
node0.hardware_type = params.node_type1
iface1 = node0.addInterface('interface-1')
iface2 = node0.addInterface('interface-2')

# Site 1 - node 1
node1 = request.RawPC('node-1')
node1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD'
node1.Site("Site1")
node1.hardware_type = params.node_type1
iface3 = node1.addInterface('interface-3')
iface4 = node1.addInterface('interface-4')

# Site 2 - node 2
node2 = request.RawPC('node-2')
node2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD'
node2.Site("Site2")
node2.hardware_type = params.node_type2
iface5 = node2.addInterface('interface-5')
iface6 = node2.addInterface('interface-6')

#Link 1
link1 = request.Link('link-1')
link1.addInterface(iface1)
link1.addInterface(iface3)
link1.Link_multiplexing = True
link1.best_effort = True

#Link 2
link2 = request.Link('link-2')
link2.addInterface(iface4)
link2.addInterface(iface5)
link2.Link_multiplexing = True
link2.best_effort = True

#Link 3
link3 = request.Link('link-3')
link3.addInterface(iface6)
link3.addInterface(iface2)
link3.Link_multiplexing = True
link3.best_effort = True

# Print the generated rspec
pc.printRequestRSpec(request)
