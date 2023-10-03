# question-and-answer
A web application for asking and answering questions about different things

## Setting Environment Variables

This project relies on environment variables to configure database, email settings etc. 

Create a `.env` file in the root directory and add the following:

```
SECRET_KEY='Django Secret Key, you can generate with get_random_secret_key() function from django.core.management.utils.'

DEBUG=True # Boolean

WEB_DOMAIN=localhost:8000  # Example
WEB_FRONT_DOMAIN=localhost:3000  # Example 

DB_NAME=my_database
DB_USER=root
DB_PASSWORD=mypassword  
DB_PORT=5432
DB_HOST=myhost
DB_HOST_DEBUG=localhost

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PASSWORD=mypassword
EMAIL_USER=myemail@example.com
EMAIL_PORT=587  
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL=myproject <myemail@example.com>

RABBITMQ_HOST=rabbit_host
RABBITMQ_HOST_DEBUG=localhost  # If Test in Docker and DEBUG = True replace with RABBITMQ_HOST
RABBITMQ_USER=rabbit_user
RABBITMQ_PASS=rabbit_pass
RABBITMQ_PORT=5672
RABBITMQ_PORT_DEBUG=5677
RABBITMQ_CONNECTION=amqp://rabbit_user:rabbit_pass@rabbit_host:rabbit_port

REDIS_HOST=redis_host
REDIS_HOST_DEBUG=localhost
REDIS_PASSWORD=redis_password  # If Test in Docker and DEBUG = True replace with REDIS_HOST
REDIS_PORT=6381
```

Replace the placeholders with actual values. Run `source .env` to load environment variables before running the app.
Now values can be accessed via `os.environ.get("KEY")`.


## Docker Compose
Exposing Database Port Externally
I have temporarily exposed the database container port externally for testing purposes only,
to allow managing data directly from inside the container without requiring a local service installation.

However, this is generally not recommended and in a production environment,
it is better to have the database inaccessible from outside without external access. Security best practices should be
followed for any applications used in production.
