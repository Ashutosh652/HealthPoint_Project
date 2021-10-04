# HealthPoint_Project

This is a web app created using django for the purpose of learning django. Note that this webapp is synchronous i.e. django vchannels is not used.

To run this on your computer:
  If you don't have any of the following packages installed, install them first. You can check which packages are installed by typing 'pip list' on your command line.
    1. Django
    2. django-crispy-forms
    3. django-phonenumber-field
    4. phonenumbers
    5. Pillow
    6. python-decouple
    7. pytz
    8. six
    9. sqlparse
   
   You can just type 'pip install -package name-' in your command line to install the packages.
   
   Then, you should be able to run it by following the following steps:
   1. Rename the '.env.example' file to '.env'.
   2. Open your command line and make sure that you are in the same directory as the manage.py file.
   3. Type 'python manage.py shell' and hit Enter. You should see three greater than (>>>) signs.
   4. Type 'from django.core.management.utils import get_random_secret_key' and hit Enter.
   5. Type 'get_random_secret_key()' and hit enter. You should now see a long string of characters in quotations. This ia a secret key.
   6. Minimize your command line and copy the secret key without the quotations and open the '.env' file.
   7. Paste it after the 'SECRET_KEY=' without any spaces.
   8. After 'EMAIL_FROM_USER=', type in your existing email address. It is recommended to create a new gmail account for this purpose.
   9. After 'EMAIL_HOST=', type 'smtp.gmail.com' if the email you entered is gmail. Make sure to open the settings of your gmail account and disable 'Two Step Verification'. You can find the steps to do that [here](https://support.google.com/accounts/answer/1064203?hl=en&co=GENIE.Platform%3DAndroid).
   10. Also make sure to allow less secure apps to access your gmail account. You can find the steps to do that [here](https://www.raramuridesign.com/kb/articles/gas-allowing-less-secure-apps-to-access-your-account.html).
   11. After 'EMAIL_HOST_PASSWORD=', enter the password of your gmail account.
   12. After 'EMAIL_USE_TLS=', type 'True' without the quotations.
   13. After 'EMAIL_PORT=', type '587' without the quotaions. Don't forget to save it.
   14. Open up your command line again and type 'exit()' and hit Enter. This will stop showing '>>>'.
   15. Type 'python manage.py makemigrations' and hit Enter.
   16. Type 'python manage.py migrate' and hit Enter.
   17. Type 'python manage.py createsuperuser' and hit Enter. It will prompt you to enter your name, email, username and password. You don't have to enter an existing email and password.
   18. Type 'python manage.py runserver' and hit Enter.
   19. Type in 'localhost:8000' in your browser and hot Enter. You should now see the website.
   20. Go to 'localhost:8000/admin' url. Type in the email and password you used to create the superuser in step 4 and log in.
   21. You should now see the admin panel. Click on 'Users' in the left sidebar. There should be only one user i.e. the superuser. Click on it.
   22. Scroll to the bottom and you should see some checkboxes. Make sure that 'is_active' and 'is_email_verified' both are checked and click on 'Save'.
   23. You should now be able to log in using the same email and password.
   24. You can now play around.
