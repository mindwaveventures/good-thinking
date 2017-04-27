# cms

Content Management System for LDMW's amazingly relevant and useful content! :tada:

This project works in tandem with the lmdw app, for the client section of the project see: https://github.com/ldmw/app

### Setup

This project uses:
+ [`python`](https://www.python.org/) (v3.6)
+ [`postgres`](https://www.postgresql.org/download/) (9.6)

Clone the repository:

```bash
git clone https://github.com/ldmw/cms.git && cd cms
```

Ensure to have the following environment variables in your `$PATH`

```bash
export DATABASE_URL=<postgres_database_url>
```

(Ensure postgres is running with: `postgres -D /usr/local/var/postgres/`)

(For the most up to date setup see the wagtail [getting started guide](https://wagtail.io/developers/))

From the root, change into the `cms` directory:

Set up the database:

```bash
python manage.py migrate
```

If you get the error `FATAL: database "cms" does not exist`

You can create this database with:

```bash
psql -U $CMS_PG_USER -c "create database cms"
```

Then run this command again

Create an admin account and start the server:

```bash
python manage.py createsuperuser
python manage.py runserver
```

The project should now be running at: `http://localhost:8000/admin`

#### Dumpdata

The file dumpdata.json has been generated with:

```bash
$ psql -c "drop database cms"
$ psql -c "create database cms" # now have clean db
$ alias dj="python manage.py"
$ dj migrate
$ dj createsuperuser
Username: user
Email address: user@user.com
Password: password
$ dj runserver # Add initial data in wagtail
$ # "hello body" in homepage>body, "hello footer" in homepage>footer
$ # "insomnia" in articles>insomnia>title, "hello insomnia" in articles>insomnia>body
$ # "fatigue" in articles>fatigue>title, "hello fatigue" in articles>fatigue>body
$ dj dumpdata --natural-foreign --natural-primary > dumpdata.json
```
