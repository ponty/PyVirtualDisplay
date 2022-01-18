Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provider "virtualbox" do |vb|
    #vb.gui = true
    vb.memory = "2048"

    vb.name = "pyvirtualdisplay_2004"

    # 	https://bugs.launchpad.net/cloud-images/+bug/1829625
    # vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
    # vb.customize ["modifyvm", :id, "--uartmode1", "file", "./ttyS0.log"]
  end

  config.vm.provision "shell", path: "tests/vagrant/vagrant.20.04.sh"

  config.ssh.extra_args = ["-t", "cd /vagrant; bash --login"]
end
