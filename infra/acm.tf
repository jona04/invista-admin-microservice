# O certificado so e criado apos a delegacao dos nameservers: a validacao e por
# DNS e depende desta zona responder pelo dominio. Criar antes deixaria o
# apply travado esperando uma validacao que nunca conclui.

resource "aws_acm_certificate" "admin" {
  count = var.dns_delegated ? 1 : 0

  domain_name               = var.domain_name
  subject_alternative_names = ["*.${var.domain_name}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "acm_validation" {
  for_each = var.dns_delegated ? {
    for opt in aws_acm_certificate.admin[0].domain_validation_options :
    opt.domain_name => opt
    # O certificado cobre `dominio` e `*.dominio`, que geram o mesmo registro de
    # validacao. Sem esse distinct o for_each colide com chave duplicada.
    if opt.domain_name == var.domain_name
  } : {}

  zone_id         = aws_route53_zone.main.zone_id
  name            = each.value.resource_record_name
  type            = each.value.resource_record_type
  records         = [each.value.resource_record_value]
  ttl             = 60
  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "admin" {
  count = var.dns_delegated ? 1 : 0

  certificate_arn         = aws_acm_certificate.admin[0].arn
  validation_record_fqdns = [for r in aws_route53_record.acm_validation : r.fqdn]
}
