
output "website_url" {
  description = "CloudFront HTTPS website URL"
  value       = "https://${aws_cloudfront_distribution.website.domain_name}"
}

output "website_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.website.bucket
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.website.id
}

output "chat_api_url" {
  description = "AI chatbot API endpoint"
  value       = "${aws_apigatewayv2_api.chat.api_endpoint}/chat"
}
