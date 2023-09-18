# Generated by Django 4.2.4 on 2023-08-27 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0018_order_razor_pay_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='razor_pay_order_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='razor_pay_payment_signature',
        ),
        migrations.CreateModel(
            name='Payment_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('plan_choosen', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='news.plans')),
            ],
        ),
    ]