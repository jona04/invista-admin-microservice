variable "aws_region" {
  description = "Regiao da infraestrutura. CloudFront exige ACM em us-east-1."
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "Profile do ~/.aws/credentials que aponta para a conta destino."
  type        = string
  default     = "kriar-prod2"
}

variable "domain_name" {
  description = "Dominio raiz."
  type        = string
  default     = "invistapublicidade.com"
}

variable "admin_subdomain" {
  description = "Subdominio que serve o painel administrativo."
  type        = string
  default     = "admin"
}

variable "frontend_bucket_name" {
  description = <<-EOT
    Bucket de origem do painel. Nome de bucket e global, entao nao da para
    reaproveitar `invista-admin-frontend`, que ainda existe na conta antiga.
    Como o bucket e privado e so o CloudFront le, o nome nao aparece para
    o usuario final.
  EOT
  type        = string
  default     = "invista-prod-admin-frontend"
}

variable "frontend_dist_path" {
  description = "Diretorio local com o build do painel que sera publicado no bucket."
  type        = string
  default     = "frontend-dist"
}

variable "dns_delegated" {
  description = <<-EOT
    Marque true DEPOIS que os nameservers do registrador apontarem para a zona
    criada aqui. So entao a validacao DNS do certificado ACM consegue concluir,
    porque ela depende desta zona ser a autoritativa do dominio.
  EOT
  type        = bool
  default     = false
}

variable "custom_domain_active" {
  description = <<-EOT
    Marque true DEPOIS de liberar o alias `admin.invistapublicidade.com` da
    distribuicao da conta antiga. O CloudFront recusa o mesmo alias em duas
    distribuicoes ao mesmo tempo e o apply falha com CNAMEAlreadyExists.
    Enquanto false, a distribuicao nova responde apenas pelo dominio
    *.cloudfront.net e o DNS continua servindo pela antiga.
  EOT
  type        = bool
  default     = false
}

variable "legacy_distribution_domain" {
  description = <<-EOT
    Distribuicao CloudFront da conta antiga que atende o painel hoje. Usada
    como alvo do registro DNS durante a janela em que a zona ja migrou mas o
    alias ainda nao. Alias do Route 53 para CloudFront funciona entre contas.
  EOT
  type        = string
  default     = "d1wbcthgy7nne4.cloudfront.net"
}
