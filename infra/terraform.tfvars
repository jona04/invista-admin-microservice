# Os dois flags abaixo destravam etapas que dependem de acoes fora do Terraform.
# Suba um de cada vez, na ordem, conforme o README.

# true depois que os nameservers do registrador apontarem para esta zona.
dns_delegated = true

# true depois que o alias admin.invistapublicidade.com for liberado da
# distribuicao da conta antiga.
custom_domain_active = true
