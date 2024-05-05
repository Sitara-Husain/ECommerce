# ECommerce

### Prerequisite:

    * Python 3.10
    * Postgress 15.2
    

### System Setup:

1. Environment setup:

    * Install pip and virtualenv:
        - sudo apt-get install python3-pip
        - pip install --upgrade pip
        - sudo pip3 install virtualenv or sudo pip install virtualenv

   * Create virtual environment:
       - virtualenv venv
         OPTIONAL:- In case finding difficulty in creating virtual environment by
                     above command , you can use the following commands too.
    
               *   Create virtualenv using Python3:-
                       - virtualenv -p python3.10 venv
       - Activate environment:
           - source venv/bin/activate
      
   * Clone project:

             ```
               https://github.com/Sitara-Husain/ECommerce.git
             ```

       - Checkout to branch
     
           ```
             git checkout dev
           ```
    
   * Install the requirements(according to server) by using command:
       - cd ECommerce/

       ```
         pip install -r requirements.txt
       ```
        
2. Database Setup:

        ```
         DATABASES = {
          'default': {
              'NAME': '*********',
              'USER': '*********',
              'PASSWORD': '*****',
              'HOST': '*********',
              'PORT': '*********',
          }
         }
        ```

3. Run migrations:

    ```
     $ python manage.py migrate
    ```

4. Run servers:

    ```
     $ python manage.py runserver
    ```
