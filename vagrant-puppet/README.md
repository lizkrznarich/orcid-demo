#Standardizing Local Development Environments with Vagrant and Puppet
Vagrant/Puppet code for a demo presented at OR2016. These files create a very basic Vagrant machine provisioned using Puppet.

See the [slides](orcid-or2016-vagrant-puppet.pdf) for a brief intro to Vagrant and Puppet!

#Prerequisites
1. Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
2. Install [Vagrant](https://www.vagrantup.com/downloads.html)

#Start the virtual machine!
1. Clone the demo files
        
        git clone https://github.com/lizkrznarich/OR2016.git

2. Change to the demo files directory
        
        cd OR2106/vagrant-puppet

3. Start the Vagrant machine
        
        vagrant up

#Resources
- [A great 3-part tutorial on Vagrant & Puppet](http://www.erikaheidi.com/blog/a-begginers-guide-to-vagrant-getting-your-portable-development-e) by [Erika Heidi](https://github.com/erikaheidi)
- [Vagrant documentation](https://www.vagrantup.com/docs)
- [Puppet documentation](https://docs.puppet.com/puppet)