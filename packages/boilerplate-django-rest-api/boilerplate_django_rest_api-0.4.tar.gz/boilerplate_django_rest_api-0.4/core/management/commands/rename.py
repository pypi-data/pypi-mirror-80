import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Renames the Django project"

    def add_arguments(self, parser):
        parser.add_argument(
            "old",
            type=str,
            nargs="+",
            help="The old Django project name"
        )
        parser.add_argument(
            "new",
            type=str,
            nargs="+",
            help="The new Django project name"
        )

    def handle(self, *args, **kwargs):
        old_project_name = kwargs["old"][0]
        new_project_name = kwargs["new"][0]

        files_to_rename = [
            f"{old_project_name}/settings.py",
            f"{old_project_name}/wsgi.py",
            f"{old_project_name}/asgi.py",
            f"{old_project_name}/urls.py",
            "manage.py",
        ]

        for f in files_to_rename:
            with open(f, "r") as file:
                content = file.read()

            content = content.replace(old_project_name, new_project_name)

            with open(f, "w") as file:
                file.write(content)

        os.rename(old_project_name, new_project_name)

        self.stdout.write(
            self.style.SUCCESS("Project {} has been renamed to {}".format(old_project_name, new_project_name))
        )
