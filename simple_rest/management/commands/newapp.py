import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a new app, but with more...'
    ADMIN_FILE_CONTENT = """
from simple_rest.utils.admin_utils.register_models_to_admin import ModelRegisterer
from {app_name} import models

ModelRegisterer(models).register()
    """

    URLS_FILE_CONTENT = """
from django.urls import path

urlpatterns = [
#    path(r'', SampleView.as_view(), name='sample'),
]
    """

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        self.create_app(app_name)
        self.create_urls_file_for_app(app_name)
        self.create_test_directory_for_app(app_name)
        self.create_views_directory_for_app(app_name)
        self.create_models_directory_for_app(app_name)
        self.create_other_directories_for_app(app_name)
        self.change_admin_file(app_name)
        self.add_to_settings(app_name)

    def create_app(self, app_name: str) -> None:
        call_command('startapp', app_name)

    def create_urls_file_for_app(self, app_name: str) -> None:
        urls_file = f'{app_name}/urls.py'
        self.override_file_content(urls_file, self.URLS_FILE_CONTENT)
        project_url_path = self.get_project_url_path()
        content = self.get_file_content(project_url_path)
        app_url = app_name.replace('_', '-')
        url_file_line = f"path(r'/api/{app_url}/', include('{app_name}.urls')),"
        content = content.replace(']', f'    {url_file_line}\n]')
        self.override_file_content(project_url_path, content)

    def add_to_settings(self, app_name):
        pass

    def get_project_url_path(self) -> str:
        return settings.ROOT_URLCONF.replace('.', '/') + '.py'

    def create_test_directory_for_app(self, app_name: str) -> None:
        old_test_file = f'{app_name}/tests.py'
        new_tests_directory = f'{app_name}/tests'
        self.remove_file(old_test_file)
        self.create_package(new_tests_directory)

    def create_views_directory_for_app(self, app_name: str) -> None:
        old_views_file = f'{app_name}/views.py'
        new_views_directory = f'{app_name}/views'
        self.remove_file(old_views_file)
        self.create_package(new_views_directory)

    def create_models_directory_for_app(self, app_name: str) -> None:
        old_models_file = f'{app_name}/models.py'
        new_models_directory = f'{app_name}/models'
        self.remove_file(old_models_file)
        self.create_package(new_models_directory)

    def create_other_directories_for_app(self, app_name: str) -> None:
        new_consts_directory = f'{app_name}/consts'
        self.create_package(new_consts_directory)
        new_serializers_directory = f'{app_name}/serializers'
        self.create_package(new_serializers_directory)
        new_tasks_directory = f'{app_name}/tasks'
        self.create_package(new_tasks_directory)
        new_permissions_checkers_directory = f'{app_name}/permissions_checkers'
        self.create_package(new_permissions_checkers_directory)

    def change_admin_file(self, app_name: str) -> None:
        admin_file = f'{app_name}/admin.py'
        new_admin_content = self.ADMIN_FILE_CONTENT.format(app_name=app_name)
        self.override_file_content(admin_file, new_admin_content)

    def remove_file(self, path: str) -> None:
        if os.path.exists(path):
            os.remove(path)

    def create_package(self, path: str) -> None:
        directory_full_path = os.path.join(settings.BASE_DIR, path)
        os.mkdir(directory_full_path)
        init_full_path = os.path.join(settings.BASE_DIR, path, '__init__.py')
        open(init_full_path, 'w+').close()

    def override_file_content(self, path: str, content) -> None:
        file_full_path = os.path.join(settings.BASE_DIR, path)
        with open(file_full_path, 'w+') as f:
            f.write(content)

    def get_file_content(self, path: str) -> str:
        file_full_path = os.path.join(settings.BASE_DIR, path)
        with open(file_full_path, 'r') as f:
            content = f.read()
        return content
