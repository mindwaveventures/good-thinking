# -*- mode: ruby -*-
# vi: set ft=ruby :

# detailed instructions for installing
$script = <<SCRIPT

sudo -i
# update ubuntu (security etc.)
apt-get update
# apt-get upgrade -y

apt-get install -y nodejs nodejs-legacy npm build-essential

npm -g install yuglify

add-apt-repository ppa:jonathonf/python-3.6
apt-get update
apt-get -y install python3.6 python3.6-dev

# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

apt-get -y install python3-pip

# PostgreSQL
apt-get purge --auto-remove postgresql-server-dev-9.5 postgresql-contrib-9.5 postgresql-client-9.5 postgresql-9.5 postgresql postgresql-contrib -y
add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get install postgresql-9.6 postgresql-contrib-9.6 postgresql-server-dev-9.6 postgresql-client-9.6 -y
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -u postgres createdb goodthinking
# Confirm Postgres is running:
/etc/init.d/postgresql status

cd /home/ubuntu

sudo -u ubuntu mkdir good-thinking
sudo -u ubuntu cd good-thinking

for d in cms crisis feedback home likes media resources search static staticfiles; do sudo -u ubuntu ln -s /vagrant/$d .; done

for f in elm-package.json good-thinking-env-variables.sh good-thinking.sh manage.py package.json requirements.txt; do sudo -u ubuntu ln -s /vagrant/$f .; done

sudo -u ubuntu npm install
sudo -u ubuntu pip3 install -r requirements.txt

chmod a+x good-thinking.sh
chmod a+x good-thinking-env-variables.sh

SCRIPT


# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false
  config.vm.box_check_update = true

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080
 config.vm.network "forwarded_port", guest: 8001, host: 8001

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"
 config.vm.network "private_network", ip: "192.168.33.20"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  config.vm.provision :shell, :inline => $script
end
