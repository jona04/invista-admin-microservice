output "zone_id" {
  description = "Hosted zone do dominio na conta nova."
  value       = aws_route53_zone.main.zone_id
}

output "nameservers" {
  description = "Nameservers a registrar no dominio. Passo manual: o registro do dominio ainda esta na conta antiga."
  value       = aws_route53_zone.main.name_servers
}

output "frontend_bucket" {
  description = "Bucket de origem do painel."
  value       = aws_s3_bucket.frontend.id
}

output "distribution_id" {
  description = "Distribuicao CloudFront nova."
  value       = aws_cloudfront_distribution.admin.id
}

output "distribution_domain" {
  description = "Dominio direto da distribuicao, para validar o painel antes do cutover do alias."
  value       = aws_cloudfront_distribution.admin.domain_name
}

output "certificate_arn" {
  description = "Certificado ACM. Nulo enquanto dns_delegated for false."
  value       = var.dns_delegated ? aws_acm_certificate_validation.admin[0].certificate_arn : null
}
