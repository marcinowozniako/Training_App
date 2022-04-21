import pytest
from django.apps import apps
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from training.apps import TrainingConfig


@pytest.fixture(scope='function')
def created_user(db):
    user = User.objects.create(username='tester')
    user.set_password('ExamplePass')
    user.save()
    user1 = User.objects.create(username='tester1')
    user1.set_password('ExamplePass1')
    user1.save()
    group_app, created = Group.objects.get_or_create(name=TrainingConfig.name)

    models = apps.all_models[TrainingConfig.name]
    for model in models:
        content_type = ContentType.objects.get(
            app_label=TrainingConfig.name,
            model=model
        )
        permissions = Permission.objects.filter(content_type=content_type)
        user.groups.add(group_app)
        user1.groups.add(group_app)
        group_app.permissions.add(*permissions)
