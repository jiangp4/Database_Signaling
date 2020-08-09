# Generated by Django 3.0.1 on 2020-05-25 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AliasName',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('Symbol', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Alias', models.ManyToManyField(to='Association.AliasName')),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('ID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Gene', models.ManyToManyField(to='Association.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('ID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('signal_detail', models.CharField(default='', max_length=255)),
                ('condition', models.CharField(default='', max_length=255)),
                ('dataset', models.CharField(default='', max_length=255)),
                ('platform', models.CharField(default='', max_length=255)),
                ('platform_detail', models.CharField(default='', max_length=255)),
                ('signal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='association', to='Association.Signal')),
            ],
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('value_adj', models.FloatField()),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='association', to='Association.Gene')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='association', to='Association.Treatment')),
            ],
            options={
                'unique_together': {('treatment', 'gene')},
            },
        ),
    ]
