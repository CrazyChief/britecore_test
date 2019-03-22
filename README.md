# BriteCore test project

## Contents

* [Requirements](#requirements)
* [Local development](#local-development)
* [Production deployment](#production-deployment)

## Requirements

* Ubuntu 16.04 (for deployment)
* Python 3.6 (make sure python header `python3.6-dev` files are installed)
* PostgreSQL >= 9.4 (9.6 is recommended)
* Node.js >= 9.1.0 (7.x-8.x might work as well though)
* Yarn >= 1.3.2

## Local development

### Database setup

You can use whatever db user and db name you want, but we will use `britecore_test` everywhere here.
```bash
sudo su - postgres
createuser britecore_test -DRSP  # Set britecore_test as a password
createdb britecore_test -O britecore_test
```

### Git repo setup
```bash
git clone git@github.com:CrazyChief/britecore_test.git
cd britecore_test
```

> All the following commands are considered to be executed from the dir `britecore_test` we've changed into in the step above, unless otherwise is specified.

### Local settings configuration
```bash
make environment
```

You have to edit `britecore_test/.env` now, especially `DJANGO_SETTINGS_MODULE` you what to use, `DATABASES` settings, etc.

### Virtual environment activation

If you ever need to use some direct commands (not Makefile targets) you can simply activate virtual environment by the following:
```bash
source .env/bin/activate
```

### Install requirements
```bash
make requirements
```

### Create migrations
```bash
make migrations
```

### Apply migrations
```bash
make migrate
```

### Run tests
```bash
make test
```

### Create superuser
```bash
make superuser
```

### Run Django server
```bash
make run
```

### Run make install-f to install all node modules, provided in `package.json`
```bash
make install-f
```

### Run make serve (if you make changes to js/vue files)
```bash
make serve
```

#### Or do the following (in case you want to run commands directly from `frontend` folder ):
```bash
cd frontend
yarn serve
```


## Production deployment
Activate your environment:
```bash
source .venv/bin/activate
```

Run command (if you didn't do this before. It will install requirements for python):
```bash
make requirements
```

Run command (if you didn't do this before. It will install frontend dependencies):
```bash
make install-f
```

Create Your own `SECRET_KEY` for this project. Just run this code in python shell:
```bash
>>> import random
>>> ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
```

### Zappa configuration

First of all you need to provide credentials of your AWS. So, provide it in `~/.aws/credentials` file:
```bash
[default]
aws_access_key_id = your_access_key_id
aws_secret_access_key = your_secret_access_key
region=us-east-1 // or another
```

After that initialize `zappa`. So, `cd` to folder with `manage.py` file
```bash
cd britecore_test
```
run
```bash
zappa init
```
and follow the instructions.
> Provide default settings to your `zappa_settings.json` file:
> * Name of environment - just accept the default 'dev'
> * S3 bucket for deployments - just accept the default
> * Zappa should automatically find the correct Django settings file so accept the default
> * Say 'no' to deploying globally

Edit the `zappa_settings.json` file to have an AWS region.
```bash
{
 "dev": {
     "aws_region": "us-east-1",
     "django_settings": "britecore_test.settings",
     "s3_bucket": "zappa-sxjkjah0x"
    }
}
```
> Don't forget to put commas in the proper place - JSON is fiddly!
> Also provide `"environment_variables"` to this json
>```bash
>"environment_variables": {
>    "SECRET_KEY": "YOUR_SECRET_KEY",
>    "DATABASE_URL": "psql://user:pass@rbd_url:5432/db_names",
>    "AWS_REGION": "YOUR_REGION",
>    "AWS_ACCESS_KEY_ID": "YOUR_KEY",
>    "AWS_SECRET_ACCESS_KEY": "YOUR_SECRET_KEY",
>},
>```
> This variable `"DATABASE_URL"` and appropriate `"vpc_config"` you will provide in [Provision your RDS Database in AWS](#Provision-your-RDS-Database-in-AWS) section.

Now it's easy to do the initial deployment
```bash
zappa deploy dev
```
Once we do, however, we get:
```bash
DisallowedHost at /
Invalid HTTP_HOST header: 'pet42wogc1.execute-api.us-east-2.amazonaws.com'. 
You may need to add 'pet42wogc1.execute-api.us-east-2.amazonaws.com' to ALLOWED_HOSTS.
```
> Note: `pet42wogc1.execute-api.us-east-2.amazonaws.com` it's my own host. You will have another.

Now edit `britecore_test/settings.py` and change ALLOWED_HOSTS to;
```bash
ALLOWED_HOSTS = [ '127.0.0.1', 'pet42wogc1.execute-api.us-east-2.amazonaws.com', ]
```

Open in your editor `frontend/src/services/config.js` and replace `pet42wogc1.execute-api.us-east-2.amazonaws.com` with your host.

After that do the following:
```bash
zappa update dev
```
Now we have deployed app in AWS Lambda.
But it's not enough. We need to store our static files.
You will need an AWS S3 bucket to host your static files. This should not be the same as your S3 bucket used by zappa to upload your code.
Create an S3 bucket and name it something like `zappa-static`. Replace all occurrences of this string with your chosen bucket name.

#### Configure CORS
Go to your S3 bucket properties, and under "Permissions", click on "Add CORS Configuration".
Paste this in:
```bash
<CORSConfiguration>
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>DELETE</AllowedMethod>
        <AllowedMethod>HEAD</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```

Now `cd` to the root folder. And prepare vue files by run:
```bash
make build
```
It will compile `.css` and `.js` files for frontend and store it in `britecore_test/dist/frontend` directory.

Configure Django-S3-Storage in `settings.py`. Find `YOUR_S3_BUCKET` variable and set value with your bucket name. After that push your static files to the cloud with command:
```bash
python manage.py collectstatic --noinput
```

Open your bucket in browser. Click on `frontend > js` folder, click on some `app.xxxxxxxx.js` file. You will see Object URL at the bottom. Copy thin URL to `js`, it will looks like this `https://s3.us-east-2.amazonaws.com/britecore-test-static/frontend/`. 
After that open in your editor `frontend/vue.config.js` and replace `https://s3.us-east-2.amazonaws.com/britecore-test-static/frontend/` to yours URL.

Run again:
```bash
make build
python manage.py collectstatic --noinput
```

Also run command for storing `webpack-stats.json` file:
```bash
zappa update dev
```

In this step we provide our static files...

#### Provision your RDS Database in AWS

And now we need to provide database settings.

So zip on over to [Creating an RDS Database](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html) and set up one. You should record some key information we'll need here:

* The subnets (there should be at least two) in which we can access the database
* The endpoint (hostname) of the database and the port
* The username and password for the root user

Provide Security Group for your DB (follow [this guide](https://docs.aws.amazon.com/en_us/AmazonRDS/latest/UserGuide/CHAP_SettingUp.html#CHAP_SettingUp.SecurityGroup))

Add `vpc_config` and environment variables to your `zappa_settings.json`:
```bash
{
    "dev": {
        "django_settings": "britecore_test.settings", 
        "s3_bucket": "zappatest-sxjkjah0x",
        "aws_region": "us-east-1",
        "vpc_config" : {
            "SubnetIds": [ "subnet-xxxxxxxx","subnet-xxxxxxxx" ], // use the private subnet
            "SecurityGroupIds": [ "sg-xxxxxxxx" ]
        },
        "environment_variables": {
            "DATABASE_URL": "psql://user:pass@rbd_url:5432/db_names",
        }
    }
}
```

##### Run the management command
```bash
zappa manage dev create_db
```
Don't worry, if you will get an error message like 'DB already exists'.

##### Run the management command to apply migrations
```bash
zappa manage dev migrate
```

##### Run this command to create superuser
```bash
zappa invoke --raw dev "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@yourdomain.com', 'YOUR_PASSWORD_HERE')"
```
If you need an access to admin page.

Well done! Now open website in your browser.

