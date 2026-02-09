output "jenkins_instances" {
  description = "Jenkins instance details"
  value = {
    master_1 = {
      name    = docker_container.jenkins_master_1.name
      web_url = "http://localhost:8081"
    }
    master_2 = {
      name    = docker_container.jenkins_master_2.name
      web_url = "http://localhost:8082"
    }
    master_3 = {
      name    = docker_container.jenkins_master_3.name
      web_url = "http://localhost:8083"
    }
  }
}

output "network_name" {
  description = "Docker network name"
  value       = docker_network.jenkins_network.name
}