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

### Using the CMS

The CMS can be accessed at https://ldmw-cms.herokuapp.com/admin/

#### Editing the Homepage

Access the Homepage through the Explorer:
<img width="586" alt="screen shot 2017-05-03 at 13 55 42" src="https://cloud.githubusercontent.com/assets/8939909/25661391/53bc1a6e-3008-11e7-879b-3ed594765446.png">

On the Homepage, click `Edit`, and you should be taken to the EDITING HOME PAGE page. From here you can edit the various fields on the Homepage. When you're done, you can click `publish`, which will publish your changes to the live site.

<img width="315" alt="screen shot 2017-05-03 at 13 57 29" src="https://cloud.githubusercontent.com/assets/8939909/25661424/7e60c21a-3008-11e7-9968-c2423576b8b8.png">

#### Adding Resources

From the Homepage, enter the Resources page.

<img width="1075" alt="screen shot 2017-05-03 at 13 58 47" src="https://cloud.githubusercontent.com/assets/8939909/25661502/d6f52d6c-3008-11e7-8c36-7a121086014d.png">

From here you can edit the existing resources, or add a new one by selecting `Add Child Page`. When prompted to choose a page type, select `Resource`.

<img width="418" alt="screen shot 2017-05-03 at 14 02 07" src="https://cloud.githubusercontent.com/assets/8939909/25661606/3bc1c778-3009-11e7-8517-d2ee8c7ddcce.png">

On the `Content` page, fill in the details of the resource you are adding. Then click on the `Promote` tab to add the tags.

<img width="371" alt="screen shot 2017-05-03 at 14 15 10" src="https://cloud.githubusercontent.com/assets/8939909/25662047/f5a4c2e8-300a-11e7-8bbf-0bb57f5d57bf.png">

The three types of tag are `Main Tags` (Categories/Sleep issues such as 'insomnia', 'fatigue' etc.), `Audience Tags` ('Men', 'Women' etc.), and `Content Tags` ('video', 'blog', 'article' etc.). Tags must be one word, or multiple words separated by a dash.

<img width="462" alt="screen shot 2017-05-03 at 14 13 59" src="https://cloud.githubusercontent.com/assets/8939909/25662024/dddabf96-300a-11e7-9090-328cf040d382.png">

These tags will be added to the site if they did not already exist. When you have done this, click publish and the resource will be added to the site.
