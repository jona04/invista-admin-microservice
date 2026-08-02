resource "aws_s3_bucket" "frontend" {
  bucket = var.frontend_bucket_name
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Somente esta distribuicao le o bucket. A conta antiga usava Origin Access
# Identity, que a AWS considera legado; aqui trocamos por Origin Access Control,
# que assina com SigV4 e restringe pela ARN da distribuicao.
resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  policy = data.aws_iam_policy_document.frontend.json
}

data "aws_iam_policy_document" "frontend" {
  statement {
    sid     = "AllowCloudFrontRead"
    effect  = "Allow"
    actions = ["s3:GetObject"]

    resources = ["${aws_s3_bucket.frontend.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.admin.arn]
    }
  }
}

locals {
  # O bucket antigo servia o build sob o prefixo /invista, compensado por um
  # origin_path na distribuicao. Aqui o build vai para a raiz e o origin_path
  # deixa de existir.
  frontend_files = fileset("${path.module}/${var.frontend_dist_path}", "**")

  content_types = {
    css   = "text/css"
    html  = "text/html"
    ico   = "image/x-icon"
    js    = "application/javascript"
    json  = "application/json"
    map   = "application/json"
    svg   = "image/svg+xml"
    txt   = "text/plain"
    woff  = "font/woff"
    woff2 = "font/woff2"
  }
}

resource "aws_s3_object" "frontend" {
  for_each = local.frontend_files

  bucket = aws_s3_bucket.frontend.id
  key    = each.value
  source = "${path.module}/${var.frontend_dist_path}/${each.value}"

  # etag force o reupload quando o conteudo muda, em vez de comparar so o nome.
  etag = filemd5("${path.module}/${var.frontend_dist_path}/${each.value}")

  content_type = lookup(
    local.content_types,
    lower(reverse(split(".", each.value))[0]),
    "application/octet-stream"
  )
}
