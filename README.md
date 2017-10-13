# cms

Content Management System for [Good Thinking](https://good-thinking.uk)

### Urls
The site is found at https://good-thinking.uk
The wagtail cms for the site is at https://good-thinking.uk/admin

The staging site is https://ldmw-staging.herokuapp.com
The staging cms is https://ldmw-staging.herokuapp.com/admin

### Setup

This project uses:
+ [`python`](https://www.python.org/) (v3.6)
+ [`postgres`](https://www.postgresql.org/download/) (9.6)
+ [`elm`](http://elm-lang.org/) (0.18)
+ (optional)[`node`](https://nodejs.org/en/) (6.11) (Node is not necessary to run the project, however we're using it as a convenient way to install/build our elm files)

Clone the repository:

```bash
git clone https://github.com/mindwaveventures/cms.git && cd cms
```

Ensure you have the following environment variables in your `$PATH`

```bash
export DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/cms`
export AWS_ACCESS_KEY_ID=<aws_access_key_id>
export AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
export AWS_STORAGE_BUCKET_NAME=<aws_storage_bucket_name>
export GOOGLE_MAPS_KEY=<google_maps_key>
```

The google maps api key can easily be obtained by clicking the `get a key` button [here](https://developers.google.com/maps/documentation/javascript/get-api-key)

(Ensure postgres is running with: `postgres -D /usr/local/var/postgres/`)

(For the most up to date setup see the wagtail [getting started guide](https://wagtail.io/developers/))

```bash
alias dj="python manage.py" # handy django alias
psql -c "create database cms" # create the cms database
dj migrate # set up the database
dj createsuperuser # create the admin account
dj runserver # start the django server
elm make ./cms/elm/Main.elm --output=./cms/static/js/elm.js # compile elm files
```

The project should now be running at: `http://localhost:8000`
The wagtail dashboard can be found at `http://localhost:8000/admin`

#### Load testing

[Artillery](https://artillery.io/docs/) is used for load testing. You can
install artillery with the command `npm install -g artillery`, and continue
following through the
[getting started guide](https://artillery.io/docs/getting-started/).

We have 2 files for testing the staging and production sites.
You can load test the staging site by making any changes you'd like to
`staging-load-test.yml` and running the command `artillery run staging-load-test.yml`.

Similarly, you can load test the production site by editing `prod-load-test.yml`
as necessary, and running `artillery run prod-load-test.yml`.


#### Wireframes

You can see our last updated set of wireframes here:
+ [Homepage](https://user-images.githubusercontent.com/26304634/29663584-b84cb7d6-88c3-11e7-8ff5-5cd00bfce682.png)
+ [Homepage mobile](https://user-images.githubusercontent.com/26304634/29663601-cb58c338-88c3-11e7-8ab8-ac5ba7d00ac9.png)
+ [Subpage](https://user-images.githubusercontent.com/26304634/29663627-f0c51cac-88c3-11e7-9af6-5456a585470f.png)

#### Data

You can get the current data from the database by running:

```bash
  heroku pg:backups:download -a ldmw
  pg_restore --verbose --clean --no-acl --no-owner -d cms latest.dump
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

## Using the CMS

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

### Add Pages

Static Pages consisting of just a heading paragraph/s and body paragraph/s can be added using the `static page` page type on wagtail.

<img width="371" alt="screen shot 2017-06-27 at 10 34 08" src="https://user-images.githubusercontent.com/8939909/27580950-2a928942-5b24-11e7-94c7-97fc20dcf70a.png">

These pages will be available at the site on `/{page-title}`. For example, the crisis page is visible at `/crisis`.

You can link to these pages from elsewhere by using an internal link, and selecting the page you want to link to.

<img width="852" alt="screen shot 2017-05-10 at 15 18 12" src="https://cloud.githubusercontent.com/assets/8939909/25903364/138bbe9a-3594-11e7-9b9f-a0f23de93d52.png">

### Topic Pages

The resources are displayed on individual topic pages. In order to make them display, you have to tag them with a topic tag that corresponds to the slug of the topic page. For example, a resource tagged with `anxious` would display on the `anxious` page (https://www.good-thinking.uk/anxious/).

### Assessments

The Expert 24 assessments work in the same way as other resources. You add a new page of type `assessment` to the resources page, then tag it with the topic you would like it to appear under.

Resources can be added to the results of these assessments by adding a hidden tag to the resource that corresponds to a tag on the disposition of the assessment results. Only resources that match the topic of the assessment will display.

### Deployment

The cms is set to automatically push from the master branch to the staging area (https://ldmw-staging.herokuapp.com/). When we're happy this is working, we push manually to the production site.
