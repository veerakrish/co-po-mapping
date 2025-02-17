# OpenStack Setup Checklist

## Hardware Setup
- [ ] All 7 computers have Ubuntu Server installed
- [ ] All network cables connected to switch
- [ ] All 4 access points connected to switch
- [ ] All computers powered on
- [ ] All network lights showing activity

## Controller Node Setup
- [ ] Ubuntu updated
- [ ] MicroStack installed
- [ ] Controller initialized
- [ ] Join command saved
- [ ] Network created
- [ ] VM template created

## Compute Nodes Setup (do for each node)
Compute Node 1:
- [ ] Ubuntu updated
- [ ] MicroStack installed
- [ ] Successfully joined to controller
- [ ] Shows up in compute service list

Compute Node 2:
- [ ] Ubuntu updated
- [ ] MicroStack installed
- [ ] Successfully joined to controller
- [ ] Shows up in compute service list

(Repeat for nodes 3-6)

## Network Setup
- [ ] Switch configured
- [ ] AP1 configured and working
- [ ] AP2 configured and working
- [ ] AP3 configured and working
- [ ] AP4 configured and working
- [ ] Network showing in OpenStack

## Software Deployment
- [ ] Shared storage configured on controller
- [ ] NFS mounts working on all compute nodes
- [ ] License server installed and running
- [ ] MATLAB installed on shared storage
- [ ] Client access scripts created
- [ ] Environment modules configured
- [ ] Test installation from one client
- [ ] Verify multiple simultaneous connections

## Additional Software (Add as needed)
Software Name: ________________
- [ ] Requirements evaluated
- [ ] Deployment method chosen
- [ ] Installation completed
- [ ] License configured
- [ ] Access tested
- [ ] Documentation created

## Testing
- [ ] Can create test VM
- [ ] All compute nodes visible
- [ ] Network working
- [ ] Access points visible

## Labels Applied
- [ ] Controller labeled
- [ ] All compute nodes labeled
- [ ] All cables labeled
- [ ] All access points labeled

Use this checklist to track progress. Mark each item when completed.
If any item fails, refer to the simple_setup_guide.md for instructions.
