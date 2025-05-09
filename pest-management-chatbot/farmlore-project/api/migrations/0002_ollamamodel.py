# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OllamaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Model name as recognized by Ollama (e.g., 'tinyllama', 'llama2')", max_length=100, unique=True)),
                ('display_name', models.CharField(help_text='Human-readable name for display', max_length=100)),
                ('description', models.TextField(blank=True, help_text="Description of the model's capabilities")),
                ('is_active', models.BooleanField(default=False, help_text='Whether this model is active and available for use')),
                ('is_default', models.BooleanField(default=False, help_text='Whether this is the default model')),
                ('default_temperature', models.FloatField(default=0.7, help_text='Default temperature parameter (0.0-1.0)')),
                ('default_max_tokens', models.IntegerField(default=500, help_text='Default max tokens for response generation')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(blank=True, null=True)),
                ('supports_chat', models.BooleanField(default=True, help_text='Whether the model supports chat completions')),
                ('supports_function_calling', models.BooleanField(default=False, help_text='Whether the model supports function calling')),
                ('supports_vision', models.BooleanField(default=False, help_text='Whether the model supports vision/image inputs')),
            ],
            options={
                'verbose_name': 'Ollama Model',
                'verbose_name_plural': 'Ollama Models',
                'ordering': ['-is_default', '-is_active', 'display_name'],
            },
        ),
    ] 