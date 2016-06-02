# -*- mode: ruby -*-
# vi: set ft=ruby :

# Before running, export REPO='https://github.com/YOUR-USERNAME/pdfhook.git' else:
REPO = ENV['REPO'] || 'https://github.com/codeforamerica/pdfhook.git'


Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  # config.vm.box_check_update = false

  config.vm.network "forwarded_port", guest: 5000, host: 5000
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"

  # config.vm.synced_folder ".", "/vagrant", type: "rsync"

  # config.vm.provider "virtualbox" do |vb|
  #   # Enable symlinks in shared folder
  #   vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root","1"]

  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end

  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  config.ssh.forward_agent = true

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get -y update
    sudo apt-get -y install python3-setuptools python3-pip python3.4-venv git libpq-dev
    sudo apt-get -y install default-jdk
    cd /home/vagrant
    rm -rf pdfhook
    git clone #{REPO}
    cd /pdfhook
    python3 -m venv .
    source bin/activate
    make install
    echo "Starting server, visit http://localhost:5000"
    make run
  SHELL
  
end
