from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Usuario precisar ter um email")
        if not password:
            raise ValueError("Usuario precisar ter uma senha")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_financeiro = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Usuario precisar ter um email")
        if not password:
            raise ValueError("Usuario precisar ter uma senha")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_financeiro = False
        user.save(using=self._db)

        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_financeiro = models.BooleanField(default=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    

class Cliente(models.Model):
    nome = models.CharField("* Nome / Empresa", max_length=200)
    email = models.EmailField("* Email", max_length=100, null=True, blank=True)
    telefone = models.CharField("* Fone", max_length=20, null=True, blank=True)
    cnpj = models.CharField("CNPJ", max_length=40, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=40, null=True, blank=True)
    rua = models.CharField("Rua", max_length=40, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=40, null=True, blank=True)
    numero = models.IntegerField("Numero", null=True, blank=True)
    cidade = models.CharField("Cidade", max_length=40, null=True, blank=True)
    estado = models.CharField("Estado", max_length=40, null=True, blank=True)
    cep = models.CharField("Cep", max_length=40, null=True, blank=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField("Atualizado em", auto_now=True, null=True)
    nota = models.ManyToManyField("Nota", through="GrupoClienteNota", null=True)

    # pylint: disable=invalid-str-returned
    # pylint: disable=no-member
    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("cliente_especifico", args=[self.id])

    def get_list_services(self):
        return reverse("lista_servicos_cliente", args=[self.id])

    def get_list_notas(self):
        return reverse("lista_notas_cliente", args=[self.id])

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-created_at"]


class Chapa(models.Model):
    nome = models.CharField("Nome", max_length=100)
    valor = models.FloatField("Valor", blank=True, default=0.0)
    estoque = models.IntegerField(
        "Quantidade em Estoque", blank=True, default=None, null=True
    )
    marca = models.CharField(
        "Marca", blank=True, max_length=50, default=None, null=True
    )
    obs = models.CharField("Obs", max_length=255, blank=True, default=None, null=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField("Atualizado em", auto_now=True, null=True)

    # pylint: disable=invalid-str-returned
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Chapa"
        verbose_name_plural = "Chapas"
        ordering = ["nome"]


class Servico(models.Model):
    # pylint: disable=invalid-str-returned
    # pylint: disable=no-member

    nome = models.CharField("Nome Serviço", max_length=200)
    cliente = models.ForeignKey(
        Cliente,
        verbose_name="Cliente",
        related_name="clientes",
        on_delete=models.PROTECT,
    )
    chapa = models.ForeignKey(
        Chapa, verbose_name="Chapa", related_name="servico", on_delete=models.PROTECT
    )
    quantidade = models.IntegerField("Quantidade", null=False)
    created_at = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField("Atualizado em", auto_now=True, null=True)
    valor_total_servico = models.FloatField("Total", null=True, blank=True, default=0.0)

    def __str__(self):
        return self.nome

    def valor(self):
        return self.quantidade * self.chapa.valor

    class Meta:
        verbose_name = "Servico"
        verbose_name_plural = "Servicos"
        ordering = ["-created_at"]


class Nota(models.Model):
    # pylint: disable=no-member
    desconto = models.FloatField("Desconto", null=True, blank=False, default=0)
    numero = models.IntegerField("Numero Nota", null=True, blank=False, default=0)
    created_at = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField("Atualizado em", auto_now=True, null=True)
    cliente_nome = models.CharField(max_length=200, null=True, blank=True)
    obs = models.TextField("Observações", null=True, blank=True)
    servico = models.ManyToManyField(Servico, through="GrupoNotaServico", null=True)
    valor_total_nota = models.FloatField("Total", null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.numero)

    STATUS_CHOICE = (
        (0, "Em aberto"),
        (1, "Pago"),
    )

    status = models.IntegerField(
        "Situação", choices=STATUS_CHOICE, default=0, blank=True
    )

    # pylint: disable=function-redefined
    @property
    def numero(self):
        return self.id + 1000

    def get_absolute_url(self):
        return reverse("nota_especifica", args=[self.id])

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ["-created_at"]


class GrupoClienteNota(models.Model):
    # pylint: disable=no-member
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.cliente.nome)


class GrupoNotaServico(models.Model):
    # pylint: disable=no-member
    nota = models.ForeignKey(Nota, on_delete=models.PROTECT, null=True)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.nota.id)

    def save(self, *args, **kwargs):
        super(GrupoNotaServico, self).save(*args, **kwargs)
        cliente = self.servico.cliente
        nota = self.nota
        GrupoClienteNota.objects.create(
            cliente = cliente,
            nota = nota
        )


class CategoriaEntrada(models.Model):
    descricao = models.CharField(max_length=100)
  

class EntradaChapa(models.Model):
    quantidade = models.IntegerField()
    marca = models.CharField(max_length=100, null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    chapa = models.ForeignKey(Chapa, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaEntrada, on_delete=models.PROTECT)
    data = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    observacao = models.TextField(null=True, blank=True)
    

class CategoriaSaida(models.Model):
    descricao = models.CharField(max_length=100)


class SaidaChapa(models.Model):
    quantidade = models.IntegerField()
    observacao = models.TextField(null=True, blank=True)
    chapa = models.ForeignKey(Chapa, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaSaida, on_delete=models.PROTECT)
    data = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    observacao = models.TextField(null=True, blank=True)
