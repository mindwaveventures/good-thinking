# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant environment for Good Thinking
# By default 'vagrant up' will start a machine and provision application and database
# Multimachine environment - two machines are defined, 'web' and 'db'
# Docker environment - Builds from Dockerfile


# Provisioning script for web machine
$script_web = <<SCRIPT

# Install *just* python3.6 before other packages
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get -y install python3.6 python3.6-dev
sudo apt-get -y install python3-pip

# Install node
sudo apt-get install -y nodejs nodejs-legacy nodejs-dev npm
npm install yuglify

# Vagrant mounts the project directory as /home/vagrant/good-thinking
cd good-thinking
npm install
sudo -H pip3 install -r requirements.txt
chmod a+x good-thinking.sh
chmod a+x good-thinking-env-variables.sh

SCRIPT

# Provisioning script for db machine
$script_db = <<SCRIPT

# Install PostgreSQL 9.6
sudo apt-get purge --auto-remove postgresql-server-dev-9.5 postgresql-contrib-9.5 postgresql-client-9.5 postgresql-9.5 postgresql postgresql-contrib -y
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6 postgresql-contrib-9.6 postgresql-server-dev-9.6 postgresql-client-9.6 -y
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -u postgres createdb goodthinking

# Confirm Postgres is running:
/etc/init.d/postgresql status

SCRIPT

# All Vagrant configuration is done below.

Vagrant.configure("2") do |config|

  # Define default machine, web & db on single machine
  config.vm.define vm_name = "default" do |default|
    default.vm.box = "ubuntu/xenial64"
    default.vbguest.auto_update = false
    default.vm.box_check_update = true
    default.vm.network "forwarded_port", guest: 8001, host: 8001
    default.vm.network "private_network", ip: "192.168.33.20"
    default.vm.synced_folder ".", "/home/vagrant/good-thinking"

    default.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
    end

    default.vm.provision :shell, :privileged => false, :inline => $script_web
    default.vm.provision :shell, :privileged => false, :inline => $script_db

  end

  # Define db machine
  config.vm.define vm_name = "db", autostart: false do |db|
    db.vm.box = "ubuntu/xenial64"
    db.vbguest.auto_update = false
    db.vm.box_check_update = true
    db.vm.network "private_network", ip: "192.168.33.21"
    db.vm.synced_folder ".", "/home/vagrant/good-thinking"

    db.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
    end

    db.vm.provision :shell, :privileged => false, :inline => $script_db

  end

  # Define web machine
  config.vm.define vm_name = "web", autostart: false do |w|
    w.vm.box = "ubuntu/xenial64"
    w.vbguest.auto_update = false
    w.vm.box_check_update = true
    w.vm.network "forwarded_port", guest: 8001, host: 8001
    w.vm.network "private_network", ip: "192.168.33.20"
    w.vm.synced_folder ".", "/home/vagrant/good-thinking"

    w.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
    end

    w.vm.provision :shell, :privileged => false, :inline => $script_web

  end

  # Define Dockerised machine
  config.vm.define vm_name = "docker", autostart: false do |dk|
    dk.vm.box = "ubuntu/xenial64"
    dk.vbguest.auto_update = false
    dk.vm.box_check_update = true
    dk.vm.network "forwarded_port", guest: 80, host: 8080
    dk.vm.network "private_network", ip: "192.168.33.20"

    dk.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
    end

    dk.vm.provision :docker do |d|
      d.build_image "/vagrant -t goodthinking:latest"
    end

  end

end
