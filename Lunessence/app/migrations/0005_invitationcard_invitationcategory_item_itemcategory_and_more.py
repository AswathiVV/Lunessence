# Generated by Django 5.1.2 on 2025-02-10 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_buy_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('img1', models.FileField(upload_to='')),
                ('img2', models.FileField(blank=True, null=True, upload_to='')),
                ('img3', models.FileField(blank=True, null=True, upload_to='')),
                ('img4', models.FileField(blank=True, null=True, upload_to='')),
                ('size', models.CharField(max_length=50)),
                ('theme', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InvitationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to='')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='destinationwedding',
            name='category',
        ),
        migrations.RemoveField(
            model_name='buy',
            name='category',
        ),
        migrations.AddField(
            model_name='buy',
            name='wedding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.destinationwedding'),
        ),
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groom_name', models.CharField(max_length=100)),
                ('bride_name', models.CharField(max_length=100)),
                ('wedding_date', models.DateField()),
                ('location', models.TextField()),
                ('guest_count', models.PositiveIntegerField(default=1)),
                ('time', models.TimeField()),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('buy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.buy')),
            ],
        ),
        migrations.AddField(
            model_name='buy',
            name='invitation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.invitationcard'),
        ),
        migrations.AddField(
            model_name='invitationcard',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.invitationcategory'),
        ),
        migrations.CreateModel(
            name='BuyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('buy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyitem_set', to='app.buy')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.itemcategory'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
