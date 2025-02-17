# Distributed OpenStack Architecture for 80 Students

## Hardware Configuration

### Cloud Controller Node (1 system)
- Hardware: 16GB RAM, Quad Core CPU
- Role: OpenStack control services
- Services: Keystone, Horizon, Heat, minimal Nova
- RAM allocation:
  - OS + Base services: 4GB
  - OpenStack services: 8GB
  - Buffer: 4GB

### Compute Nodes (6 systems)
- Hardware per node: 16GB RAM, Quad Core CPU
- Role: VM hosting
- Services: Nova-compute, Neutron agent
- RAM allocation per node:
  - OS + Services: 4GB
  - VMs: 12GB (can host ~13-14 VMs with 1GB RAM each)
- Total VM capacity: ~80 VMs (13-14 VMs × 6 nodes)

### Network Configuration
- 4 Access Points:
  - AP1: Covers Compute Nodes 1-2
  - AP2: Covers Compute Nodes 2-3
  - AP3: Covers Compute Nodes 4-5
  - AP4: Covers Compute Nodes 5-6
- Each AP handles 20 client connections

## Network Architecture
```
[Cloud Controller] -----> [Switch] -----> [4 Access Points]
         |                    |
         |                    |
    [Compute1]           [Compute4]
    [Compute2]           [Compute5]
    [Compute3]           [Compute6]
```

## Resource Distribution

### Per Compute Node
- VMs per node: 13-14
- RAM per VM: 1GB
- vCPU per VM: 0.5 (shared)
- Storage per VM: 10GB

### Load Balancing
- Round-robin VM distribution
- Auto-failover between nodes
- Dynamic resource allocation

## Network Addressing
- Management Network: 10.0.0.0/24
  - Controller: 10.0.0.10
  - Compute1: 10.0.0.11
  - Compute2: 10.0.0.12
  - etc.

- VM Network: 192.168.1.0/23
  - DHCP Range 1: 192.168.1.0/24 (APs 1-2)
  - DHCP Range 2: 192.168.2.0/24 (APs 3-4)

## Failover Strategy
- If one compute node fails:
  - VMs can be redistributed to other nodes
  - Temporary reduction in RAM per VM to 768MB if needed
  - Critical VMs prioritized

## MATLAB Service Distribution
- MATLAB Network License Server on Controller Node
- MATLAB Runtime distributed across compute nodes
- Shared storage for MATLAB toolboxes

## Scaling Considerations
- Each VM starts with 1GB RAM
- Can scale down to 768MB under load
- CPU sharing ratio 4:1 (4 vCPUs per physical core)
- Storage thin provisioning enabled
