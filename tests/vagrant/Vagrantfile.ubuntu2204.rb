Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_version = "20220104.0.0"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "pyvirtualdisplay_ubuntu2204"
    #   vb.gui = true
    vb.memory = "2048" # ste high because of Xephyr memory leak
  end

  config.vm.provision "shell", path: "tests/vagrant/ubuntu2204.sh"

  config.ssh.extra_args = ["-t", "cd /vagrant; bash --login"]
end

# export VAGRANT_VAGRANTFILE=tests/vagrant/Vagrantfile.22.04.rb;export VAGRANT_DOTFILE_PATH=.vagrant_${VAGRANT_VAGRANTFILE}
# vagrant up && vagrant ssh
