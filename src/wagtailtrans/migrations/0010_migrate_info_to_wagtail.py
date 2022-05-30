# Generated by Django 3.1.5 on 2021-01-08 11:07

from django.db import migrations


def transfer_info(apps, schema_editor):
    Language = apps.get_model("wagtailtrans", "Language")
    TranslatablePage = apps.get_model("wagtailtrans", "TranslatablePage")
    Locale = apps.get_model("wagtailcore", "Locale")

    for language in Language.objects.all():
        locale, created = Locale.objects.get_or_create(language_code=locale.language_code)

    for page in TranslatablePage.objects.filter(canonical_page__isnull=True):
        page.locale = Locale.objects.get(language_code=page.locale.language_code)
        page.save()
        for transl_page in page.translations.all():
            transl_page.translation_key = page.translation_key
            transl_page.locale = Locale.objects.get(
                language_code=transl_page.locale.language_code
            )
            transl_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailtrans", "0009_create_initial_language"),
    ]

    operations = [
        migrations.RunPython(transfer_info),
    ]
