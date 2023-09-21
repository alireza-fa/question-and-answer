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
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=myproject <myemail@example.com>
```

Replace the placeholders with actual values. Run `source .env` to load environment variables before running the app. Now values can be accessed via `os.environ.get("KEY")`.