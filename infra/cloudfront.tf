data "aws_cloudfront_cache_policy" "caching_optimized" {
  name = "Managed-CachingOptimized"
}

resource "aws_cloudfront_origin_access_control" "frontend" {
  name                              = "${var.frontend_bucket_name}-oac"
  description                       = "Acesso do CloudFront ao bucket do painel invista"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "admin" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2"
  comment             = "invista admin"
  default_root_object = "index.html"

  # PriceClass_All mantem os pontos de presenca da America do Sul, que e de
  # onde vem o acesso ao painel. Classes menores excluem a regiao.
  price_class = "PriceClass_All"

  # Vazio ate o alias ser liberado da distribuicao antiga. Ver a variavel
  # custom_domain_active.
  aliases = var.custom_domain_active ? [local.admin_fqdn] : []

  origin {
    origin_id                = "frontend"
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend.id
  }

  default_cache_behavior {
    target_origin_id       = "frontend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    cache_policy_id        = data.aws_cloudfront_cache_policy.caching_optimized.id
  }

  # SPA em Angular: qualquer rota desconhecida precisa devolver o index para o
  # roteador do proprio app resolver, senao um refresh em /alguma-rota quebra.
  dynamic "custom_error_response" {
    for_each = [400, 403, 404]

    content {
      error_code            = custom_error_response.value
      response_code         = 200
      response_page_path    = "/index.html"
      error_caching_min_ttl = 10
    }
  }

  # O certificado e anexado assim que existe, antes e independentemente do
  # alias. E o que permite mover o alias com `associate-alias` sem derrubar o
  # painel: o CloudFront exige um certificado que cubra o dominio ja presente
  # na distribuicao de destino antes de aceitar a associacao.
  viewer_certificate {
    cloudfront_default_certificate = var.dns_delegated ? false : true
    acm_certificate_arn            = var.dns_delegated ? aws_acm_certificate_validation.admin[0].certificate_arn : null
    ssl_support_method             = var.dns_delegated ? "sni-only" : null
    minimum_protocol_version       = var.dns_delegated ? "TLSv1.2_2021" : null
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}
