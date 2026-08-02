terraform {
  backend "s3" {
    bucket       = "invista-tfstate"
    key          = "prod/terraform.tfstate"
    region       = "us-east-1"
    profile      = "kriar-prod2"
    encrypt      = true
    use_lockfile = true
  }
}

# Tudo aqui vive em us-east-1: o ACM consumido pelo CloudFront so pode ser
# emitido nessa regiao, e o bucket de origem acompanha para evitar salto entre
# regioes na primeira requisicao de cada objeto.
provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  default_tags {
    tags = {
      Project   = "invista"
      Env       = "prod"
      ManagedBy = "terraform"
    }
  }
}
