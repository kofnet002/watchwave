# Video Platform API built with Django Rest Framework

<a href="https://www.django-rest-framework.org/" target="_blank">
    <img src="https://mmnsfubzyoequbbehhrp.supabase.co/storage/v1/object/public/watchwave/Backend%20Documentation/IMG_0100.JPG" width=100% alt='Django rest framework'>
</a>

### Project is hosted live with the front end on <a href="https://watchwave.vercel.app" target="_blank">watchwave</a>.

## A fully functional Video Platform - Django Rest API project build and tested with <a href="https://www.django-rest-framework.org/" target="_blank">restframework</a> and deployed to <a href="https://koyeb.com/" target="_blank">Koyeb</a>.

The project was inspired by <a href="https://amalitech.org">AmaliTech</a> as part of their NSS Digital Training programs. Every piece of this project required time and futher reading since I customized most of Django's <a href="https://djoser.readthedocs.io/en/latest/getting_started.html" target="_blank">Djoser</a> library .
The activities involved in this project are as follows:

1. Database model (table) development and configurations
2. Writing the various API views for all the neccessary methods of each view
3. Admin panel management configurations.
4. Adding all the neccesary URL endpoints to for all the various views and thier methods. Not forgetting the admin panel too.
5. Writing tests for all the views and thier methods. I also used Postman for testing as well.
6. Including a <a href="https://watchwave-watchwave.koyeb.app" target="_blank">documentation</a> for the project through a python module called <a href="https://drf-spectacular.readthedocs.io/en/latest/" target="_blank">drf-spectacular</a> by <a href="https://www.openapis.org/" target="_blank">OpenAPI Initiative</a>.
7. Deploy the Django REST API to <a href="https://koyeb.com/" target="_blank">Koyeb</a>

## Features

### Normal user

- Create an account with the credentials below
  - username
  - email
  - password
- Activate your account via link sent by email.
- Logging in to watch videos.
- Able to watch next or previous videos in the queue.
- Share video links across all platforms

### Admin

- Loggin in to upload videos with
  - title
  - description
  - video file
- Able to manage user accounts
- Able to manage videos on the dasboard with reflects on the hosted db
- To delete videos or video preview files, log into the cloudindary account since videos are hosted or serve from the cloud.

## Image of the WebAPI

<a href="https://watchwave-watchwave.koyeb.app" target="_blank">
    <img src="https://mmnsfubzyoequbbehhrp.supabase.co/storage/v1/object/public/watchwave/Backend%20Documentation/Backend%20Documentation.png" width=100% alt='Backe end view'>
</a>

## Images of the Front End Application

<a href="https://mywatchwave.vercel.app/login" target="_blank">
    <img src="https://mmnsfubzyoequbbehhrp.supabase.co/storage/v1/object/public/watchwave/Frontend/Screenshot%20from%202024-03-31%2020-31-09.png" width=100% alt='Front end view'>
</a>
<a href="https://mywatchwave.vercel.app/login" target="_blank">
    <img src="https://mmnsfubzyoequbbehhrp.supabase.co/storage/v1/object/public/watchwave/Frontend/Screenshot%20from%202024-03-31%2020-33-17.png" width=100% alt='Front end view'>
</a>

## Technologies used for building the system

1. <a href="https://www.django-rest-framework.org" target="_blank">Django Rest Framework</a> for handling the API views and URLs.

2. <a href="https://cloudinary.com/" target="_blank">Cloudinary</a> for hosting the videos and the `video previews` when scrubbing the timeline. `Video Previews` are the images that shows when the user hovers over the timeline of the video player. `Create and account on Cloudinary and get the following credentials`

- CLOUDINARY_CLOUD_NAME
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET

3. I built the <a href="https://mywatchwave.vercel.app/login" target="_blank">Front end</a> like the `youtube video player`.

4. <a href="supabase.com" target="_blank">Supabase</a> for Database management and hosting of static images as well.

5. <a href="https://koyeb.com" target="_blank">Koyeb</a> for hosting the application.

6. <a href="https://sendgrid.com/en-us" target="_blank">SendGrid</a>, the platform I used for sending Emails. `Create and account and get your API for sending emails`.

## Prerequisites

```
    python3.10
    django
    djanfo-restframework
```

## Project setup

1. #### Clone this repository

```
    git clone https://github.com/kofnet002/watchwave.git
    cd watchwave/
```

2. #### Create a virtual environment to manage the packages & activate it

```
    python -m venv venv
    .venv/bin/activate
```

3. #### Install all the neccessary packages/dependencies

```
    pip install -r requirements.txt
```

5. ### Setup environment variables

- In the root directory, create the file <strong>`.env`</strong> and the following environment variables

```
SECRET_KEY = any long random combination for alphabets and numbers

================ DB CONFIGURATION ===================
## There are 2 ways of setting up the database configuration, in the settings.py file, I used the approach 1

## APPROACH 1
DATABASES['default'] = dj_database_url.config(
    default='postgres://user:password@localhost:port/dbname',
)

## APPROACH 2
# If you go by this approach, make sure to add the necessary credentials as stated below.
ENGINE = 'django.db.backends.postgresql'
NAME = your db name
HOST = your db host
USER = your db user
PASSWORD= your db password
PORT='5432'

SITE_NAME = 'WatchWave' # Site name that will show on the admin dasboard as well as the emai the user will receive

ADMIN_SITE_HEADER = 'WatchWave' # Head on the admin dashboard

DOMAIN = 'mywatchwave.vercel.app' # Frontend domain without the domain

SENDGRID_API_KEY = your sendgrid api key # For sending emails

DEFAULT_FROM_EMAIL = your account to send the mail from  # eg. abc@xyz.com


CLOUDINARY_CLOUD_NAME = your cloudinary cloud name
CLOUDINARY_API_KEY= your cloudinary api key
CLOUDINARY_API_SECRET = your cloudinary api secret

```

4. In the root directory of the project in the terminal, run the code below to create a superuser to manage all the users of the application. be sure python is installed before you proceed with this stage.
   `The application needs you to activate your account first, but as a super admin, your account will be activated by default.`

```
    python manage createsuperuser
```

6. #### Run the program with the following command

```
    python3 manage runserver
```

`Open your broswer and then visit http:127.0.0.1:8000` or `localhost:8000`

## Admin

Since some extra work is being done in the background when uploading videos, the admin dasboard provided by django is not suitable for uploading videos. Instead you can visit <a href="https://mywatchwave.vercel.app/dashboard">Admin dashboard</a> to upload videos.

## Behind the scene when uploading a video

- I leverage the power of <a href="https://ffmpeg.org" target="_blank">ffmpeg</a> to snapshot the current uploading video every 10s and save it along with the video. The snapshots or the video previews displays just like <a href="https://youtube.com">YouTube</a>. That is when you hover the mouse over the video timeline, the video previews will show on the screen and on the timeline as well.

## Get Involved

We welcome contributions and participation from the community to help make this e-commerce backend API even better! Whether you're looking to fix bugs, add new features, or improve documentation, your help is greatly appreciated. Here's how you can get involved:

### Reporting Issues 🚩

If you encounter any bugs or issues, please report them using the <a href="https://github.com/kofnet002/watchwave/issues" target="_blank">Issues</a> section of my GitHub repository. When reporting issues, please include:

- A clear and descriptive title.
- A detailed description of the problem, including steps to reproduce it.
- Any relevant logs or error messages.
  Your environment details (e.g., Django version, DRF version, database, etc.).

### Contributing Code 💁🏼

I love receiving pull requests from the community! If you have an improvement or a new feature you'd like to add, please feel free to do so 👍
