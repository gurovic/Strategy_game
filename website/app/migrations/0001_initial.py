# Generated by Django 4.2.5 on 2023-11-15 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InvokerReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CompilerReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compiled_file', models.FileField(blank=True, null=True, upload_to='compiler_report', verbose_name='Файл')),
                ('time', models.DurationField(verbose_name='Время выполнения')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('status', models.IntegerField(choices=[(0, 'Ok'), (1, 'Compiler Error'), (2, 'Compilation Error'), (3, 'Timelimit')], default=0, verbose_name='Статус')),
                ('error', models.TextField(blank=True, editable=False, null=True, verbose_name='Ошибка')),
                ('invoker_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.invokerreport', verbose_name='Репорт инвокера')),
            ],
            options={
                'verbose_name': 'Репорт компилятора',
                'verbose_name_plural': 'Репорты компилятора',
            },
        ),
    ]