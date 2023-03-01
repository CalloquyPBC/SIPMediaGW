HOST = "172.16.1.30"

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/focal64"

  config.vm.network "public_network", ip: HOST

  config.vm.synced_folder ".", "/sipmediagw", type: "virtualbox",  owner: "vagrant", group: "vagrant"

  config.vm.provider "virtualbox" do |vb|
      vb.memory = "16384"
      vb.cpus = 8
  end

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
    v.name = "SIPMediaGW_AllInOne"
  end
end
