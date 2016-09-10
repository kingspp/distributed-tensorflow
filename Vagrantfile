# -*- mode: ruby -*-
# # vi: set ft=ruby :

require 'fileutils'
require 'open-uri'
require 'tempfile'
require 'yaml'

Vagrant.require_version ">= 1.6.0"

$update_channel = "alpha"

CLUSTER_IP="10.3.0.1"
NODE_IP = "172.22.22.22"
NODE_MEMORY_SIZE = 2048
USER_DATA_PATH = File.expand_path("user-data")
SSL_TARBALL_PATH = File.expand_path("ssl/controller.tar")
DOCKER_IMAGES = File.expand_path("docker_images.tar.xz")

system("mkdir -p ssl && lib/init-ssl-ca ssl") or abort ("failed generating SSL CA artifacts")
system("lib/init-ssl ssl apiserver controller IP.1=#{NODE_IP},IP.2=#{CLUSTER_IP}") or abort ("failed generating SSL certificate artifacts")
system("lib/init-ssl ssl admin kube-admin") or abort("failed generating admin SSL artifacts")

Vagrant.configure("2") do |config|
  # always use Vagrant's insecure key
  config.ssh.insert_key = false

  config.vm.box = "coreos-%s" % $update_channel
  config.vm.box_version = ">= 1151.0.0"
  config.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant.json" % $update_channel

  ["vmware_fusion", "vmware_workstation"].each do |vmware|
    config.vm.provider vmware do |v, override|
      v.vmx['numvcpus'] = 1
      v.vmx['memsize'] = NODE_MEMORY_SIZE
      v.gui = false

      override.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant_vmware_fusion.json" % $update_channel
    end
  end

  config.vm.provider :virtualbox do |v|
    v.cpus = 1
    v.gui = false
    v.memory = NODE_MEMORY_SIZE

    # On VirtualBox, we don't have guest additions or a functional vboxsf
    # in CoreOS, so tell Vagrant that so it can be smarter.
    v.check_guest_additions = false
    v.functional_vboxsf     = false
  end

  # plugin conflict
  if Vagrant.has_plugin?("vagrant-vbguest") then
    config.vbguest.auto_update = false
  end

  config.vm.network :private_network, ip: NODE_IP

  config.vm.provision :file, :source => SSL_TARBALL_PATH, :destination => "/tmp/ssl.tar"
  config.vm.provision :shell, :inline => "mkdir -p /etc/kubernetes/ssl && tar -C /etc/kubernetes/ssl -xf /tmp/ssl.tar", :privileged => true

  config.vm.provision :file, :source => DOCKER_IMAGES, :destination => "/tmp/docker_images.tar.xz"
  config.vm.provision :shell, :inline => "cd /tmp/ && tar -xvf docker_images.tar.xz", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/pause.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/addon.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/dns.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/heapster.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/hyperkube.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/dashboard.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/health.tar", :privileged => true
  config.vm.provision :shell, :inline => "docker load -i /tmp/docker_images/dnsmasq.tar", :privileged => true

  config.vm.provision :file, :source => USER_DATA_PATH, :destination => "/tmp/vagrantfile-user-data"
  config.vm.provision :shell, :inline => "mv /tmp/vagrantfile-user-data /var/lib/coreos-vagrant/", :privileged => true

end
