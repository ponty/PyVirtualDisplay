Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "pyvirtualdisplay_1804"
    #   vb.gui = true
    vb.memory = "4096" # ste high because of Xephyr memory leak
  end

  config.vm.provision "shell", path: "tests/vagrant/vagrant.18.04.sh"

  config.ssh.extra_args = ["-t", "cd /vagrant; bash --login"]
end

# export VAGRANT_VAGRANTFILE=Vagrantfile.18.04.rb;export VAGRANT_DOTFILE_PATH=.vagrant_${VAGRANT_VAGRANTFILE}
# vagrant up && vagrant ssh
