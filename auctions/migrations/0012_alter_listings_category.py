# Generated by Django 4.0.6 on 2022-07-12 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_listings_highest_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Home Appliance', 'Home Appliance'), ('Sports', 'Sports'), ('Toys and Baby Products', 'Toys and Baby Products'), ('Digital Goods', 'Digital Goods'), ('Food and Beverages', 'Food and Beverages'), ('Stationary', 'Stationary'), ('Bags and Accessories', 'Bags and Accecories'), ('Books', 'Books'), ('Vehicles', 'Vehicles'), ('Others', 'Others')], max_length=64),
        ),
    ]
