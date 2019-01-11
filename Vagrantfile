# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'getoptlong'

opts = GetoptLong.new(
  [ '--vqfx-id', GetoptLong::OPTIONAL_ARGUMENT ],
  [ '--ports-map', GetoptLong::OPTIONAL_ARGUMENT ],
  [ '--dev-name', GetoptLong::OPTIONAL_ARGUMENT ]
)

id=2
port_map = ""
dev_name = ""
opts.each do |opt, arg|
  case opt
    when '--vqfx-id'
      id=arg
    when '--ports-map'
      port_map=arg
    when '--dev-name'
      dev_name=arg
  end
end

ports_map = port_map.split("*").each_with_object({}) do |str, h| 
  k,v = str.split(":")
  v.sub! '[', ''
  v.sub! ']', ''
  v.sub! ' ', ''
  val = v.split(",").map(&:to_i)
  #print val
  h[k] = val
end

puts 'DEV-TYPE:  ' + dev_name
puts 'ID:  ' + id.to_s

VAGRANTFILE_API_VERSION = "2"

## Define ports mapping to create a Full Mesh between all 4 vqfx

dataports_size = ports_map["#{id}"].count
puts 'PORT-SIZE:  ' + dataports_size.to_s
puts ports_map["#{id.to_sym}"]

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.ssh.insert_key = false

    re_name  = ( "vqfx" + id.to_s ).to_sym
    pfe_name = ( "vqfx" + id.to_s + "-pfe" ).to_sym
    srv_name  = ( "srv" + id.to_s ).to_sym

    if dev_name != "server"

        # ##############################
        # ## Packet Forwarding Engine ##
        # ##############################
        config.vm.define pfe_name do |vqfxpfe|
            vqfxpfe.ssh.insert_key = false
            vqfxpfe.vm.box = 'juniper/pfe'
            vqfxpfe.vm.boot_timeout = 1000

            # DO NOT REMOVE / NO VMtools installed
            vqfxpfe.vm.synced_folder '.', '/vagrant', disabled: true
            vqfxpfe.vm.network 'private_network', auto_config: false, nic_type: '82540EM', virtualbox__intnet: "vqfx_internal_#{id}"
        end

        ##########################
        ## Routing Engine  #######
        ##########################
        config.vm.define re_name do |vqfx|
            vqfx.vm.hostname = "vqfx#{id}"
            vqfx.vm.box = 'juniper/rebox'
            vqfx.vm.boot_timeout = 1000

            # DO NOT REMOVE / NO VMtools installed
            vqfx.vm.synced_folder '.', '/vagrant', disabled: true

            # Management port
            vqfx.vm.network 'private_network', auto_config: false, nic_type: '82540EM', virtualbox__intnet: "vqfx_internal_#{id}"
            vqfx.vm.network 'private_network', auto_config: false, nic_type: '82540EM', virtualbox__intnet: "reserved_bridge"

            # Dataplane ports (server) 
            #for seg_id in 0..serv_dataports_size-1 do
            #   #puts serv_ports_map["#{id}"][seg_id].to_s
            #   vqfx.vm.network 'private_network', auto_config: false, nic_type: '82540EM', virtualbox__intnet: serv_ports_map["#{id}"][seg_id].to_s
            #end

            # Dataplane ports (other spine and leaves)
            for seg_id in 0..dataports_size-1 do
               puts ports_map["#{id}"][seg_id].to_s
               vqfx.vm.network 'private_network', auto_config: false, nic_type: '82540EM', virtualbox__intnet: ports_map["#{id}"][seg_id].to_s
            end
        end

        config.vm.provision "ansible" do |ansible|
            ansible.limit = "all,localhost"
            ansible.playbook = "create_inventory.yml"
            ansible.extra_vars = {
              host_name:"vqfx#{id}"
            }
        end
    end

    if dev_name == "server"
        ##########################
        ## Server          #######
        ##########################
        config.vm.define srv_name do |srv|
            srv.vm.box = "ubuntu/xenial64"
            srv.vm.hostname = "server#{id}"
            
            for seg_id in 0..dataports_size-1 do
                puts "10.10.#{id}.#{seg_id}"
                puts ports_map["#{id}"][seg_id].to_s
                srv.vm.network 'private_network', ip: "10.10.#{id}.#{seg_id}", virtualbox__intnet: ports_map["#{id}"][seg_id].to_s
            end
            srv.ssh.insert_key = true
            srv.vm.provision "shell",
                inline: "sudo route add -net 10.10.0.0 netmask 255.255.0.0 gw 10.10.#{id}.254"
            srv.vm.provision 'shell', inline: 'echo "root:Juniper" | chpasswd'
            srv.vm.provision 'shell', inline: 'sudo sed -i "s/prohibit-password/yes/" /etc/ssh/sshd_config'
            srv.vm.provision 'shell', inline: 'sudo sed -i "s/PasswordAuthentication no/PasswordAuthentication yes/" /etc/ssh/sshd_config'
            srv.vm.provision 'shell', inline: 'sudo service ssh restart'
        end

        config.vm.provision "ansible" do |ansible|
            ansible.limit = "all,localhost"
            ansible.playbook = "create_inventory.yml"
            ansible.extra_vars = {
              host_name:"server#{id}"
            }
        end
    end

end
