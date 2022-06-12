Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "pyvirtualdisplay_ubuntu2204_main"
    #   vb.gui = true
    vb.memory = "2048" 
  end

  config.vm.provision "shell", path: "tests/vagrant/ubuntu2204.sh"

  config.ssh.extra_args = ["-t", "cd /vagrant; bash --login"]
end
