import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

from django.core.management import call_command


def save_fixtures(app_name):
    fixture_dir = "src/fixtures"
    fixture_filename = f"{app_name}_fixtures.json"

    if not os.path.exists(fixture_dir):
        os.makedirs(fixture_dir)

    call_command(
        "dumpdata", app_name, output=os.path.join(fixture_dir, fixture_filename)
    )


save_fixtures("comments")
save_fixtures("favorite")
save_fixtures("follow")
save_fixtures("ingredients")
save_fixtures("reactions")
save_fixtures("recipes")
save_fixtures("users")
save_fixtures("view")
