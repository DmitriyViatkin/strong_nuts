from django.db import migrations, models
import django.db.models.deletion


def create_delivery_methods(apps, schema_editor):
    DeliveryMethod = apps.get_model('order_management', 'DeliveryMethod')
    db_alias = schema_editor.connection.alias
    DeliveryMethod.objects.using(db_alias).create(slug='NP', name='Нова Пошта', is_free=False, cost=60)
    DeliveryMethod.objects.using(db_alias).create(slug='courier', name='Кур\'єр', is_free=False, cost=100)
    DeliveryMethod.objects.using(db_alias).create(slug='pickup', name='Самовивіз', is_free=True, cost=0)


def map_old_delivery_to_fk(apps, schema_editor):
    ClientOrder = apps.get_model('order_management', 'ClientOrder')
    DeliveryMethod = apps.get_model('order_management', 'DeliveryMethod')
    db_alias = schema_editor.connection.alias
    slug_to_id = {m.slug: m.id for m in DeliveryMethod.objects.using(db_alias).all()}
    for order in ClientOrder.objects.using(db_alias).all():
        new_id = slug_to_id.get(order.delivery_old)
        if new_id:
            order.delivery_new_id = new_id
            order.save(update_fields=['delivery_new_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0007_remove_clientorder_comment_en_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=50, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=255, verbose_name='Назва')),
                ('is_free', models.BooleanField(default=False, verbose_name='Безкоштовна')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Вартість')),
            ],
            options={'verbose_name': 'Метод доставки', 'verbose_name_plural': 'Методи доставки'},
        ),
        migrations.RunPython(create_delivery_methods, migrations.RunPython.noop),
        migrations.RenameField(model_name='clientorder', old_name='delivery', new_name='delivery_old'),
        migrations.AddField(
            model_name='clientorder',
            name='delivery_new',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='order_management.deliverymethod',
                verbose_name='Метод доставки',
            ),
        ),
        migrations.RunPython(map_old_delivery_to_fk, migrations.RunPython.noop),
        migrations.RemoveField(model_name='clientorder', name='delivery_old'),
        migrations.RenameField(model_name='clientorder', old_name='delivery_new', new_name='delivery'),
    ]
