fedora-software
===============

Web interface to Fedora Software database


Development instance
--------------------

Clone the git repository:

    git clone git@github.com:misli/fedora-software.git
    cd fedora-software

Initialize database:

    ./manage.py syncdb

Run development server:

    ./manage.py runserver

Import data form appstream-data

    ./manage.py updatedb


Translations
------------

https://docs.djangoproject.com/en/1.8/topics/i18n/translation/

Update translations:

    pushd fedora_software
        django-admin makemessages -l cs
        vim locale/cs/LC_MESSAGES/django.po
        django-admin compilemessages
    popd
