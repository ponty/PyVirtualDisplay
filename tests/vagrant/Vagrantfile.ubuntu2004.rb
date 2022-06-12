Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provider "virtualbox" do |vb|
    #vb.gui = true
    vb.memory = "2048"

    vb.name = "pyvirtualdisplay_ubuntu2004"
  end

  config.vm.provision "shell", path: "tests/vagrant/ubuntu2004.sh"
  config.ssh.extra_args = ["-t", "cd /vagrant; bash --login"]
end

# export VAGRANT_VAGRANTFILE=tests/vagrant/Vagrantfile.20.04.rb;export VAGRANT_DOTFILE_PATH=.vagrant_${VAGRANT_VAGRANTFILE}
# vagrant up && vagrant ssh