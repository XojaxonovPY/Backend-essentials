from invoke import task


@task
def mig(c):
    c.run("python manage.py makemigrations")


@task
def upg(c):
    c.run("python manage.py migrate")


@task
def superuser(c):
    c.run("python manage.py createsuperuser")


@task
def apps(c):
    c.run("python manage.py startapp apps")


@task
def load(c):
    c.run(
        "python manage.py loaddata products.json categories.json disdricts.json images.json regions.json sellers.json tags.json options.json attrs.json settings.json")


@task
def dump(c):
    c.run("python manage.py dumpdata apps.ProductImage > images.json")


@task
def celery(c):
    c.run("celery -A DjangoAPI worker --loglevel=info --pool=solo")


@task
def flower(c):
    c.run("celery -A DjangoAPI flower")


@task
def bot(c):
    c.run("python bot/main.py")


@task
def beat(c):
    c.run("celery -A DjangoAPI beat -l info -S django")


@task
def restart(c):
    c.run('docker rm -f django_container')
    c.run('docker rmi -f docker_django')
    c.run('docker build . -t django')
    c.run('docker run --name django_container -p 8000:8000 docker_django')
