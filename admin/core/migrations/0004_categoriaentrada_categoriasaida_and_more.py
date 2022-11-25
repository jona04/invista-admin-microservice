# Generated by Django 4.1.2 on 2022-11-24 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_update_valor_total_nota"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoriaEntrada",
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
                ("descricao", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="CategoriaSaida",
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
                ("descricao", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="nota",
            name="valor_total_nota",
            field=models.FloatField(
                blank=True, default=0.0, null=True, verbose_name="Total"
            ),
        ),
        migrations.AlterField(
            model_name="servico",
            name="valor_total_servico",
            field=models.FloatField(
                blank=True, default=0.0, null=True, verbose_name="Total"
            ),
        ),
        migrations.CreateModel(
            name="SaidaChapa",
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
                ("quantidade", models.IntegerField()),
                ("observacao", models.TextField()),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.categoriaentrada",
                    ),
                ),
                (
                    "chapa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.chapa"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntradaChapa",
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
                ("quantidade", models.IntegerField()),
                ("marca", models.CharField(max_length=100)),
                ("valor_unitario", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.categoriaentrada",
                    ),
                ),
                (
                    "chapa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.chapa"
                    ),
                ),
            ],
        ),
    ]
