# Software Deployment Guide for OpenStack Cloud

## Software Deployment Options

### Option 1: Central Installation (Recommended for MATLAB)
Best for software that:
- Uses network licensing
- Has high storage requirements
- Needs frequent updates
- Requires significant computing power

#### Setup Steps for Central Installation:
1. Install on Controller Node:
```bash
# Create shared storage directory
sudo mkdir -p /opt/shared/software
sudo chmod 755 /opt/shared/software

# Mount this directory on all compute nodes
# On each compute node, run:
sudo mkdir -p /opt/shared/software
sudo mount controller:/opt/shared/software /opt/shared/software
```

2. Install License Server (for MATLAB):
```bash
# On Controller Node:
sudo mkdir -p /opt/licenses/matlab
# Copy MATLAB license file to this directory
sudo chmod 644 /opt/licenses/matlab/license.dat
```

3. Create Network Share:
```bash
# Install NFS server on controller
sudo apt install nfs-kernel-server -y

# Configure exports
echo "/opt/shared/software *(ro,sync,no_subtree_check)" | sudo tee -a /etc/exports
echo "/opt/licenses *(ro,sync,no_subtree_check)" | sudo tee -a /etc/exports

# Apply changes
sudo exportfs -a
```

### Option 2: VM Template Installation
Best for software that:
- Has minimal license requirements
- Runs independently
- Has moderate storage needs
- Needs specific OS configurations

#### Setup Steps for VM Template:

1. Create Base VM:
```bash
# Create a larger VM for software installation
sudo microstack.openstack server create \
  --flavor small-vm \
  --image ubuntu-20.04 \
  --network cloud-net \
  software-template
```

2. Install Software:
```bash
# Get VM IP
sudo microstack.openstack server list

# Connect to VM
ssh ubuntu@<VM-IP>

# Install software dependencies
sudo apt update
sudo apt install -y required-packages

# Mount and install your software
# For MATLAB:
sudo mkdir /mnt/matlab
sudo mount -o loop matlab_installer.iso /mnt/matlab
sudo /mnt/matlab/install
```

3. Create Template:
```bash
# Shutdown VM
sudo microstack.openstack server stop software-template

# Create image
sudo microstack.openstack image create \
  --server software-template \
  software-image
```

## Example: MATLAB Deployment

### Method 1: Central Installation (Recommended)

1. On Controller Node:
```bash
# Create MATLAB directory
sudo mkdir -p /opt/shared/matlab/R2023b

# Install MATLAB
sudo ./install_matlab.sh \
  --destinationFolder /opt/shared/matlab/R2023b \
  --fileInstallationKey <your-key> \
  --licensePath /opt/licenses/matlab/license.dat \
  --mode silent

# Create module file for environment
sudo mkdir -p /opt/shared/modules/matlab
sudo nano /opt/shared/modules/matlab/R2023b.lua
```

2. Create Environment Module:
```lua
-- MATLAB R2023b module file
local version = "R2023b"
local base = "/opt/shared/matlab/" .. version

whatis("MATLAB " .. version)

prepend_path("PATH", pathJoin(base, "bin"))
setenv("MATLAB_HOME", base)
setenv("MLM_LICENSE_FILE", "/opt/licenses/matlab/license.dat")
```

3. Configure Client Access:
```bash
# Create startup script
sudo nano /opt/shared/matlab/matlab_client.sh
```
```bash
#!/bin/bash
export MLM_LICENSE_FILE=/opt/licenses/matlab/license.dat
/opt/shared/matlab/R2023b/bin/matlab "$@"
```

### Method 2: VM Template (Alternative)

1. Create MATLAB VM Template:
```bash
# Create larger flavor for MATLAB
sudo microstack.openstack flavor create \
  --ram 4096 \
  --disk 40 \
  --vcpus 2 \
  matlab-flavor

# Create VM
sudo microstack.openstack server create \
  --flavor matlab-flavor \
  --image ubuntu-20.04 \
  --network cloud-net \
  matlab-template
```

2. Install MATLAB on Template:
- Connect to VM
- Install MATLAB
- Configure license
- Create template image

## Adding New Software

### General Steps for Any Software:

1. Evaluate Software Requirements:
- License type (network/standalone)
- Storage needs
- Computing requirements
- Update frequency

2. Choose Deployment Method:
- Central Installation if:
  * Network license
  * Large storage needs
  * Frequent updates
- VM Template if:
  * Standalone license
  * Moderate resources
  * Infrequent updates

3. Prepare Installation:
```bash
# For central installation
sudo mkdir -p /opt/shared/[software-name]/[version]

# For VM template
sudo microstack.openstack flavor create \
  --ram [RAM-MB] \
  --disk [DISK-GB] \
  --vcpus [CPU-COUNT] \
  [software-name]-flavor
```

4. Create Documentation:
```bash
# Document installation
sudo nano /opt/shared/docs/[software-name].md
```

## Best Practices

1. Version Control:
- Keep multiple versions in separate directories
- Use environment modules for version management
- Document version changes

2. License Management:
- Centralize license servers
- Monitor license usage
- Set up license alerts

3. Storage Management:
- Regular cleanup of unused versions
- Backup of configuration files
- Monitor disk usage

4. Access Control:
- Set appropriate permissions
- Log access patterns
- Monitor resource usage

5. Updates:
- Schedule regular updates
- Test updates in staging
- Document update procedures

## Troubleshooting

1. License Issues:
```bash
# Check license server
lmutil lmstat -a -c /opt/licenses/[software]/license.dat
```

2. Access Issues:
```bash
# Check permissions
ls -la /opt/shared/[software]

# Check mount points
df -h
mount | grep shared
```

3. Performance Issues:
```bash
# Check resource usage
top
free -h
df -h
```
