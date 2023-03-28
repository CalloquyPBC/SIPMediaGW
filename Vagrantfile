HOST = "172.16.1.30"

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/focal64"
  config.disksize.size = "100GB"

  config.vm.network "public_network", ip: HOST

  config.vm.synced_folder ".", "/sipmediagw", type: "virtualbox",  owner: "vagrant", group: "vagrant"

  config.vm.provider "virtualbox" do |vb|
      # Memory allocation
      vb.memory = "16384"
      # Configure the number of CPU cores
      vb.cpus = 16
      # DNS resolver
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      # DNS proxy
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      # IOAPIC for better performance
      vb.customize ["modifyvm", :id, "--ioapic", "on"]
      # Use UTC time from host
      vb.customize ["modifyvm", :id, "--rtcuseutc", "on"]
  end
  # Enable SSH agent forwarding
  config.ssh.forward_agent = true

   # Enable provisioning with a shell script
  config.vm.provision "shell", type: "shell" do |s|
    s.env = {
	  "HOST_IP" => HOST,
	}
	s.inline = "/sipmediagw/test/provision.sh"
  end
  # Set a specific VM name
  config.vm.provider "virtualbox" do |v|
    # File name of the VM
    v.name = "SIPMediaGW_AllInOne"
    # Display the VirtualBox GUI when booting the machine
    v.gui = 1
  end
end
