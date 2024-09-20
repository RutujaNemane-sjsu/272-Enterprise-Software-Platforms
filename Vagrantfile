# Vagrantfile for setting up Flask app in a VM
Vagrant.configure("2") do |config|
    # Use Ubuntu 20.04 as the base image
    config.vm.box = "ubuntu/focal64"
  
    # Set up the VM memory and CPU (adjust according to your needs)
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 2
    end
  
    # Expose port 5000 to access the Flask app from the host
    config.vm.network "forwarded_port", guest: 5000, host: 5001
  
    # Provisioning: Install required software and dependencies
    config.vm.provision "shell", inline: <<-SHELL
      # Update package list and install Python, pip, and SQLite
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip sqlite3
  
      # Install Flask
      pip3 install flask
  
      # Set up your Flask app
      sudo mkdir -p /vagrant/flask_blog
      sudo cp -r /vagrant/* /vagrant/flask_blog
      cd /vagrant/flask_blog
  
      # Run the Flask app (you might modify this to run in the background)
      python3 app.py
    SHELL
  end
  