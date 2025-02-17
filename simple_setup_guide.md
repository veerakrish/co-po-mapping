# Simple Setup Guide for OpenStack Distributed System

## Before You Start
1. Have 7 computers ready (1 controller + 6 compute nodes)
2. Each computer should have:
   - 16GB RAM
   - Quad Core CPU
   - 500GB or more storage
   - Network card
3. Have 4 wireless access points ready
4. One network switch
5. Network cables

## Step 1: Prepare Each Computer
On each computer, do these steps:

1. Download Ubuntu Server 22.04 LTS
   - Go to: https://ubuntu.com/download/server
   - Click "Download Ubuntu Server 22.04 LTS"

2. Create Ubuntu USB installer
   - Download Rufus from: https://rufus.ie/
   - Insert USB stick (8GB or larger)
   - Open Rufus
   - Select your USB drive
   - Select the Ubuntu ISO you downloaded
   - Click START

3. Install Ubuntu Server
   - Connect keyboard, mouse, and monitor
   - Insert the USB drive
   - Start the computer and boot from USB
   - Choose "Install Ubuntu Server"
   - Select language: English
   - Select keyboard layout
   - Choose "Minimal Installation"
   - For network, choose "ens33" or similar
   - For storage, use entire disk
   - Create admin user:
     - Name: openstack
     - Password: (choose a strong password)
   - Wait for installation to complete
   - Remove USB and restart

## Step 2: Set Up Controller Node (First Computer)

1. Log in to Ubuntu

2. Update the system (copy and paste these commands):
```bash
# Update package list and upgrade system
sudo apt update
sudo apt upgrade -y
```

3. Install OpenStack requirements:
```bash
# Install required packages
sudo apt install snapd -y
sudo snap install microstack --beta
```

4. Set up as controller:
```bash
# Initialize as controller
sudo microstack init --auto --control
```
- This will take 15-30 minutes
- You'll see lots of text scrolling
- Wait until it's finished

5. Save the join command:
```bash
# Get the command needed for compute nodes
sudo microstack add-compute
```
- Copy the command it shows you
- Save it in a text file
- You'll need this for other computers

## Step 3: Set Up Compute Nodes (Other 6 Computers)

On each compute node, do these steps:

1. Update system (same as controller):
```bash
sudo apt update
sudo apt upgrade -y
```

2. Install OpenStack:
```bash
sudo apt install snapd -y
sudo snap install microstack --beta
```

3. Join to controller:
- Use the command you saved from controller
- It looks something like:
```bash
sudo microstack init --auto --compute --join <some-long-code>
```

4. Verify connection:
```bash
sudo microstack.openstack compute service list
```
- Should show the new compute node in the list

## Step 4: Network Setup

1. Set up switch:
   - Connect all computers to the switch
   - Connect controller to port 1
   - Connect compute nodes to ports 2-7

2. Set up access points:
   - Connect APs to switch ports 8-11
   - Configure each AP:
     - AP1: Network name: CloudLab-1
     - AP2: Network name: CloudLab-2
     - AP3: Network name: CloudLab-3
     - AP4: Network name: CloudLab-4

3. On controller, set up networks:
```bash
# Create provider network
sudo microstack.openstack network create --share cloud-net

# Create subnet
sudo microstack.openstack subnet create --network cloud-net --subnet-range 192.168.1.0/23 cloud-subnet
```

## Step 5: Create VM Template

1. On controller, create small VM size:
```bash
# Create VM size template
sudo microstack.openstack flavor create --ram 1024 --disk 10 --vcpus 1 small-vm
```

2. Download base image:
```bash
# Get Ubuntu cloud image
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img

# Add it to OpenStack
sudo microstack.openstack image create --file focal-server-cloudimg-amd64.img --disk-format qcow2 ubuntu-20.04
```

## Checking If Everything Works

1. Check compute nodes:
```bash
sudo microstack.openstack compute service list
```
- Should show all 6 compute nodes

2. Check network:
```bash
sudo microstack.openstack network list
```
- Should show your network

3. Try creating a test VM:
```bash
sudo microstack.openstack server create --flavor small-vm --image ubuntu-20.04 --network cloud-net test-vm
```

## Common Problems and Solutions

1. If a command doesn't work:
   - Check if you typed it exactly as shown
   - Try running the command with 'sudo' in front
   - Wait a minute and try again

2. If a compute node won't join:
   - Make sure it's connected to the network
   - Try rebooting the compute node
   - Run the join command again

3. If network doesn't work:
   - Check all cable connections
   - Make sure switch is powered on
   - Verify all computers have network lights on

## Need Help?
If something doesn't work:
1. Check the error message carefully
2. Make sure all computers are powered on
3. Verify network connections
4. Try rebooting the problem computer

Remember:
- Take your time with each step
- Double-check commands before running them
- Keep track of which computer is which
- Label everything clearly
