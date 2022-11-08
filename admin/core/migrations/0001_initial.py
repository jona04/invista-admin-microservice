# Generated by Django 4.1.2 on 2022-11-03 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chapa",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100, verbose_name="Nome")),
                ("valor", models.FloatField(blank=True, verbose_name="Valor")),
                (
                    "estoque",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Quantidade em Estoque",
                    ),
                ),
                (
                    "marca",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=50,
                        null=True,
                        verbose_name="Marca",
                    ),
                ),
                (
                    "obs",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="Obs",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
            ],
            options={
                "verbose_name": "Chapa",
                "verbose_name_plural": "Chapas",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(max_length=200, verbose_name="* Nome / Empresa"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=100, null=True, verbose_name="* Email"
                    ),
                ),
                (
                    "telefone",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="* Fone"
                    ),
                ),
                (
                    "cnpj",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="CNPJ"
                    ),
                ),
                (
                    "cpf",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="CPF"
                    ),
                ),
                (
                    "rua",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="Rua"
                    ),
                ),
                (
                    "bairro",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="Bairro"
                    ),
                ),
                (
                    "numero",
                    models.IntegerField(blank=True, null=True, verbose_name="Numero"),
                ),
                (
                    "cidade",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="Cidade"
                    ),
                ),
                (
                    "estado",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="Estado"
                    ),
                ),
                (
                    "cep",
                    models.CharField(
                        blank=True, max_length=40, null=True, verbose_name="Cep"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
            ],
            options={
                "verbose_name": "Cliente",
                "verbose_name_plural": "Clientes",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="GrupoNotaServico",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Servico",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=200, verbose_name="Nome Serviço")),
                ("quantidade", models.IntegerField(verbose_name="Quantidade")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "valor_total_servico",
                    models.FloatField(blank=True, default=0.0, verbose_name="Total"),
                ),
                (
                    "chapa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="servico",
                        to="core.chapa",
                        verbose_name="Chapa",
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="clientes",
                        to="core.cliente",
                        verbose_name="Cliente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Servico",
                "verbose_name_plural": "Servicos",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Nota",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "desconto",
                    models.FloatField(default=0, null=True, verbose_name="Desconto"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                (
                    "obs",
                    models.TextField(blank=True, null=True, verbose_name="Observações"),
                ),
                (
                    "valor_total_nota",
                    models.FloatField(blank=True, default=0.0, verbose_name="Total"),
                ),
                (
                    "status",
                    models.IntegerField(
                        blank=True,
                        choices=[(0, "Em aberto"), (1, "Pago")],
                        default=0,
                        verbose_name="Situação",
                    ),
                ),
                (
                    "servico",
                    models.ManyToManyField(
                        null=True, through="core.GrupoNotaServico", to="core.servico"
                    ),
                ),
            ],
            options={
                "verbose_name": "Nota",
                "verbose_name_plural": "Notas",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="gruponotaservico",
            name="nota",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="core.nota"
            ),
        ),
        migrations.AddField(
            model_name="gruponotaservico",
            name="servico",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.servico",
            ),
        ),
        migrations.CreateModel(
            name="GrupoClienteNota",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.cliente",
                    ),
                ),
                (
                    "nota",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.nota",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cliente",
            name="nota",
            field=models.ManyToManyField(
                null=True, through="core.GrupoClienteNota", to="core.nota"
            ),
        ),
    ]