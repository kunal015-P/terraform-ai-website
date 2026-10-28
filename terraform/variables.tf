
variable "aws_region" {
  description = "AWS region for regional resources"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "ai-static-website"

  validation {
    condition     = can(regex("^[a-z0-9-]{3,30}$", var.project_name))
    error_message = "Use 3-30 lowercase letters, numbers, or hyphens."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "bedrock_model_id" {
  description = "Amazon Bedrock model ID"
  type        = string
  default     = "amazon.nova-lite-v1:0"
}

variable "allowed_origins" {
  description = "Allowed website origins for the AI API"
  type        = list(string)
  default     = ["*"]
}
