variable "jenkins_instances" {
  description = "Number of Jenkins instances to provision"
  type        = number
  default     = 3
}

variable "jenkins_image" {
  description = "Jenkins Docker image to use"
  type        = string
  default     = "jenkins/jenkins:lts"
}

variable "base_port" {
  description = "Base port for Jenkins web UI"
  type        = number
  default     = 8081
}

variable "base_agent_port" {
  description = "Base port for Jenkins agents"
  type        = number
  default     = 50001
}