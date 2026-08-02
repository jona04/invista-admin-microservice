locals {
  admin_fqdn = "${var.admin_subdomain}.${var.domain_name}"

  # Zona fixa e global do CloudFront, usada por qualquer registro alias que
  # aponte para uma distribuicao.
  cloudfront_zone_id = "Z2FDTNDATAQYW2"

  # Enquanto o alias nao migrou, o DNS aponta para a distribuicao antiga.
  admin_target = var.custom_domain_active ? aws_cloudfront_distribution.admin.domain_name : var.legacy_distribution_domain
}

resource "aws_route53_zone" "main" {
  name    = var.domain_name
  comment = "invista - gerenciado por terraform"
}

resource "aws_route53_record" "admin_a" {
  zone_id = aws_route53_zone.main.zone_id
  name    = local.admin_fqdn
  type    = "A"

  alias {
    name                   = local.admin_target
    zone_id                = local.cloudfront_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "admin_aaaa" {
  zone_id = aws_route53_zone.main.zone_id
  name    = local.admin_fqdn
  type    = "AAAA"

  alias {
    name                   = local.admin_target
    zone_id                = local.cloudfront_zone_id
    evaluate_target_health = false
  }
}

# Nao replicamos `admin-api` nem `users-api` da zona antiga: os dois apontavam
# para load balancers que nao existem mais em us-east-1 e nao resolvem. O
# backend real hoje e o app Heroku consumido direto pelo frontend.
