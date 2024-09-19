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
  
      # Navigate to the synced folder where the Flask app is located
      cd /vagrant
  
      # Run the Flask app (you might modify this to run in the background)
      FLASK_APP=app.py flask run --host=0.0.0.0
    SHELL
  end
  