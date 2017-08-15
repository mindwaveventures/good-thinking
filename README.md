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
export DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/cms`
export AWS_ACCESS_KEY_ID=<aws_access_key_id>
export AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
export AWS_STORAGE_BUCKET_NAME=<aws_storage_bucket_name>
```

(Ensure postgres is running with: `postgres -D /usr/local/var/postgres/`)

(For the most up to date setup see the wagtail [getting started guide](https://wagtail.io/developers/))

```bash
alias dj="python manage.py" # handy django alias
psql -c "create database cms" # create the cms database
dj migrate # set up the database
dj createsuperuser # create the admin account
dj runserver # start the django server
```

The project should now be running at: `http://localhost:8000/admin`

#### Dumpdata

You can add the current dumpdata from the project by switching to the `dumpdata` branch and running:

```bash
psql -c "drop database cms"
psql -c "create database cms" # now have clean db
dj migrate
dj loaddata dumpdata.json
```

If you get the following error when running `loaddata`:

```bash
DETAIL:  Key (group_id, collection_id, permission_id)=(1, 1, 5) already exists.
```

You should run the following command:

```bash
psql -d cms -c "delete from wagtailcore_groupcollectionpermission where collection_id=1"
dj loaddata dumpdata.json
```

You can re-dump the dumpdata with the command:

```bash
dj dumpdata --natural-foreign --natural-primary > dumpdata.json
```

To set up the needed remotes for the project you should run the following:

```bash
# Remove all remotes
for r in $(git remote);do;git remote rm $r;done;
# Add the correct remotes
git remote add old https://git.heroku.com/ldmw-cms.git
git remote add heroku https://git.heroku.com/ldmw.git
git remote add staging https://git.heroku.com/ldmw-staging.git
git remote add origin https://github.com/ldmw/cms.git
```

git remote -v should output:

```bash
old https://git.heroku.com/ldmw-cms.git
staging https://git.heroku.com/ldmw-staging.git
heroku https://git.heroku.com/ldmw.git
origin https://github.com/ldmw/cms.git
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

### Deployment

The cms is set to automatically push from the master branch to the cms staging area (https://ldmw-cms-staging.herokuapp.com/admin/). When we're happy this is working, we will push manually to the production site.

### Add Pages

Static Pages consisting of just a heading paragraph/s and body paragraph/s can be added using the `static page` page type on wagtail.

<img width="371" alt="screen shot 2017-06-27 at 10 34 08" src="https://user-images.githubusercontent.com/8939909/27580950-2a928942-5b24-11e7-94c7-97fc20dcf70a.png">

These pages will be available at the site on `/{page-title}`. For example, the crisis page is visible at `/crisis`.

You can link to these pages from elsewhere by using an internal link, and selecting the page you want to link to.

<img width="852" alt="screen shot 2017-05-10 at 15 18 12" src="https://cloud.githubusercontent.com/assets/8939909/25903364/138bbe9a-3594-11e7-9b9f-a0f23de93d52.png">
