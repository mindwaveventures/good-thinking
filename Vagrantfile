# -*- mode: ruby -*-
# vi: set ft=ruby :

# detailed instructions for installing
$script = <<SCRIPT

# Update package lists
sudo apt-get update

# Upgrade packages (un-comment)
# sudo apt-get upgrade -y

# Install node
sudo apt-get install -y nodejs nodejs-legacy npm build-essential
sudo -S npm -g install yuglify

# Install *just* python3.6
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get -y install python3.6 python3.6-dev
sudo apt-get -y install python3-pip

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

# Vagrant mounts the project directory as /home/vagrant/good-thinking
cd good-thinking
sudo -H npm -g install
sudo -H pip3 install --upgrade pip
sudo -H pip3 install -r requirements.txt
chmod a+x good-thinking.sh
chmod a+x good-thinking-env-variables.sh

SCRIPT


# All Vagrant configuration is done below.

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.box_check_update = true
  config.vm.network "forwarded_port", guest: 8001, host: 8001
  config.vm.network "private_network", ip: "192.168.33.20"
  config.vm.synced_folder ".", "/home/vagrant/good-thinking"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
  end

  config.vm.provision :shell, :privileged => false, :inline => $script

end
