# Generated by Django 2.2.3 on 2019-11-14 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_auto_20191023_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoNotaServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='servico',
            name='desconto',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='fineshed_at',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='obs',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='status',
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desconto', models.FloatField(null=True, verbose_name='Desconto')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('uploaded_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Em aberto'), (1, 'Pago')], default=0,
                                               verbose_name='Situação')),
                ('servico', models.ManyToManyField(null=True, through='core.GrupoNotaServico', to='core.Servico')),
            ],
        ),
        migrations.AddField(
            model_name='gruponotaservico',
            name='nota',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Nota'),
        ),
        migrations.AddField(
            model_name='gruponotaservico',
            name='servico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Servico'),
        ),
    ]