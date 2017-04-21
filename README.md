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
export CMS_PG_USER=<cms_postgres_username>
export CMS_PG_PASS=<cms_postgres_password>
export CMS_HOST=<cms_host>
export CMS_PORT=<cms_port>
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

