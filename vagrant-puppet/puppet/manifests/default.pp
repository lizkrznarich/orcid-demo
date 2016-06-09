# specify default paths
Exec {
  path => ["/usr/bin", "/bin", "/usr/sbin", "/sbin", "/usr/local/bin", "/usr/local/sbin"]
}

# install packages
class install-packages {
  exec { 'apt-get update':
    command => 'apt-get update',
  }

  $packages = [ "apache2", "php5", "php5-mysql", "curl", "vim", "wget", "zip", "unzip"]
  package { $packages:
    ensure => "installed",
    require => Exec['apt-get update'],
  }
}

# start apache
class apache {
  service { "apache2":
    ensure  => "running",
    require => Class["install-packages"],
  }
}

include install-packages
include apache