# Lab Technician's Guide: Ubuntu Server Installation
## For OpenStack Cloud Setup

### What You Need
1. Empty USB drive (8GB or larger)
2. Ubuntu Server ISO file (ubuntu-22.04.5-live-server-amd64.iso)
3. Computer for installation
4. Network cable
5. Keyboard, mouse, and monitor

### PART 1: Create Bootable USB
1. **Download Rufus**
   - Go to: https://rufus.ie
   - Click "Download" (get the .exe file)
   - Save it to your desktop

2. **Start Rufus**
   - Double-click Rufus .exe file
   - If asked "Allow this app to make changes?" click Yes

3. **Make Bootable USB**
   - Insert empty USB drive
   - In Rufus:
     1. Device: Select your USB drive
     2. Boot selection: Click SELECT, find Ubuntu ISO file
     3. Click START
     4. If asked about download, click NO
     5. When warned all data will be destroyed, click OK
   - Wait until complete (about 5-10 minutes)
   - Close Rufus when done

### PART 2: BIOS Setup
1. **Enter BIOS**
   - Restart computer
   - Press key repeatedly during startup:
     * Dell: F2 or F12
     * HP: F10
     * Lenovo: F1 or F2
     * Custom PC: Delete or F2
   
2. **Change BIOS Settings**
   - Find "Virtualization" or "VT-x"
     * Usually under: Advanced, CPU Configuration, or Security
     * Enable it
   - Find "Boot Order" or "Boot Sequence"
     * Put USB first
   - Save and Exit
     * Usually F10 or Save Changes and Reset

### PART 3: Install Ubuntu Server

#### For Controller Node:
1. **Start Installation**
   - Insert USB drive
   - Start computer
   - When Ubuntu screen appears, press Enter

2. **Basic Choices**
   - Language: English
   - Keyboard: English (US)
   - Type of Install: Ubuntu Server
   - Just press Enter for these

3. **Network**
   - Wait for "ens33" or similar to show "connected"
   - Press Enter (Done)

4. **Storage**
   - Choose: "Use Entire Disk"
   - Enable: "Set up this disk as an LVM group"
   - Press Enter (Done)
   - When asked "Continue with changes?" select Continue

5. **User Setup** (VERY IMPORTANT)
   FOR CONTROLLER:
   ```
   Name: OpenStack Admin
   Server name: controller
   Username: openstack
   Password: [use strong password]
   ```

   FOR COMPUTE NODES:
   ```
   Name: OpenStack Admin
   Server name: compute1 (or compute2, compute3, etc.)
   Username: openstack
   Password: [SAME as controller]
   ```

6. **SSH Server**
   - Check: "Install OpenSSH server"
   - Press Enter (Done)

7. **Software**
   - Don't select anything
   - Press Enter (Done)

8. **Wait**
   - Installation will run (15-20 minutes)
   - DO NOT turn off computer

9. **Finish**
   - When "Installation Complete" appears
   - Click "Reboot Now"
   - Remove USB when asked

### PART 4: First Boot Check

1. **Login**
   - Wait for black screen with login
   - Type username: openstack
   - Type password: [your password]

2. **Check Network**
   ```
   ping 8.8.8.8
   ```
   - Press Ctrl+C to stop
   - If you see replies, network is working

3. **Update System**
   ```
   sudo apt update
   sudo apt upgrade -y
   ```
   - Type password when asked
   - Wait until complete (5-15 minutes)

### Labels & Records

1. **Label Each Computer**
   - Controller: Put label "CONTROLLER"
   - Others: "COMPUTE1", "COMPUTE2", etc.

2. **Record Information**
   ```
   Computer Role: [Controller/Compute1/etc.]
   Username: openstack
   Password: [write it down]
   ```

### Troubleshooting

1. **Won't Boot from USB**
   - Check USB is fully inserted
   - Enter BIOS and check boot order
   - Try different USB port
   - Remake bootable USB

2. **No Network**
   - Check network cable connection
   - Try different network port
   - Check cable with different computer

3. **Installation Fails**
   - Take photo of error message
   - Try installation again
   - If fails twice, try different USB

### Important Rules
1. Use EXACTLY the same username and password on all computers
2. Label every computer clearly
3. Keep passwords written down safely
4. Don't proceed to OpenStack setup until ALL computers are ready

### Need Help?
If something doesn't work:
1. Check all cables
2. Read error message carefully
3. Try steps again
4. Take photos of any error messages
5. Contact supervisor if problem persists

### Next Steps
After ALL computers are installed:
1. Keep them turned on
2. Keep them connected to network
3. Wait for OpenStack setup instructions
