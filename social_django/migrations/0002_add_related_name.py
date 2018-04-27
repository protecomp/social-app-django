# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from social_core.utils import setting_name

USER_MODEL = getattr(settings, setting_name('USER_MODEL'), None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'
ASSOCIATION_SERVER_URL_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_SERVER_URL_LENGTH'), 150
)
ASSOCIATION_HANDLE_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_HANDLE_LENGTH'), 150
)

class Migration(migrations.Migration):
    replaces = [
        ('social_auth', '0002_add_related_name')
    ]

    dependencies = [
        ('social_django', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE {dbname}.social_auth_association MODIFY COLUMN server_url varchar({length}) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL ;'.format(
            dbname=settings.DATABASES['default']['NAME'],
            length=ASSOCIATION_SERVER_URL_LENGTH
        )),
        migrations.RunSQL('ALTER TABLE {dbname}.social_auth_association MODIFY COLUMN handle varchar({length}) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL ;'.format(
            dbname=settings.DATABASES['default']['NAME'],
            length=ASSOCIATION_HANDLE_LENGTH
        )),
        migrations.AlterField(
            model_name='usersocialauth',
            name='user',
            field=models.ForeignKey(
                related_name='social_auth', to=USER_MODEL, on_delete=models.CASCADE,
            )
        ),
        migrations.AlterUniqueTogether(
            name='usersocialauth',
            unique_together={('provider', 'uid')},
        ),
        migrations.AlterUniqueTogether(
            name='code',
            unique_together={('email', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='nonce',
            unique_together={('server_url', 'timestamp', 'salt')},
        ),
    ]
