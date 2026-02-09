# Configure Terraform
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Configure Docker provider
provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}

# Create a custom network for Jenkins instances
resource "docker_network" "jenkins_network" {
  name = "jenkins-fleet-network"
}

# Jenkins Master Instance 1
resource "docker_container" "jenkins_master_1" {
  name  = "jenkins-master-1"
  image = docker_image.jenkins.image_id

  ports {
    internal = 8080
    external = 8081
  }

  ports {
    internal = 50000
    external = 50001
  }

  networks_advanced {
    name = docker_network.jenkins_network.name
  }

  env = [
    "JENKINS_OPTS=--prefix=/jenkins1"
  ]
}

# Jenkins Master Instance 2
resource "docker_container" "jenkins_master_2" {
  name  = "jenkins-master-2"
  image = docker_image.jenkins.image_id

  ports {
    internal = 8080
    external = 8082
  }

  ports {
    internal = 50000
    external = 50002
  }

  networks_advanced {
    name = docker_network.jenkins_network.name
  }

  env = [
    "JENKINS_OPTS=--prefix=/jenkins2"
  ]
}

# Jenkins Master Instance 3
resource "docker_container" "jenkins_master_3" {
  name  = "jenkins-master-3"
  image = docker_image.jenkins.image_id

  ports {
    internal = 8080
    external = 8083
  }

  ports {
    internal = 50000
    external = 50003
  }

  networks_advanced {
    name = docker_network.jenkins_network.name
  }

  env = [
    "JENKINS_OPTS=--prefix=/jenkins3"
  ]
}

# Pull Jenkins Docker image
resource "docker_image" "jenkins" {
  name = "jenkins/jenkins:lts"
}