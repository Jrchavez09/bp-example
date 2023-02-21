# bp-example

### Flask Project Structure
```markdown
/bp-example
├── run.py
└── /example
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── /static
    └── /templates
        ├── /errors
        ├── /main
        └── /user
```
### App Structure with Blueprints
*Flask blueprints allow us to organize our applications by grouping logic into subdirectories.*
```markdown
/bp-example
├── /example
│   ├── /errors
│   │   ├── handlers.py                   # Error handlers
│   │   ├── __init__.py
│   │   └── /templates
│   │       └── /errors
│   │           ├── 403.html              # Error 403 page (forbidden page)                                                                           
│   │           ├── 404.html              # Error 404 page (page not found)                                                                     
│   │           └── 500.html              # Error 500 page (server error page)                                                                     
│   ├── __init__.py                       # Bundle all sections and expose the Flask APP                                                                                 
│   ├── /main                                                                                                   
│   │   ├── __init__.py                                                                                        
│   │   ├── routes.py                                                                                          
│   │   └── /templates                                                                                          
│   │       ├── _base.html                # Used by common pages like index, UI                                                                    
│   │       ├── /main                                                                                           
│   │       │   └── index.html            # default page                                                                           
│   │       └── navigation.html           # navigation bar                                                             
│   └── /user                                                                                                   
│       ├── forms.py                                                                                           
│       ├── __init__.py                                                                                        
│       ├── models.py                     # DB user table                                                                                   
│       ├── routes.py                                                                                          
│       └── /templates                                                                                          
│           └── /user                     # user pages (login, register)                                                                  
│               ├── login.html            # sign-in page                                                         
│               └── register.html         # sign-up page                                                       
├── LICENSE
├── /migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── /versions
│       └── 00280049dd2a_initial_migration.py
├── README.md
├── requirements.txt                      # Application dependencies
└── wsgi.py                               # Start the app in development and production
```
#### Getting started
```commandline
    mkdir hello_world
    cd hello_world
```
#### creating virtual environment
```
    python -m venv venv
```
####
```commandline
   hello_world $ ls
   venv
```
#### activate the environment
```commandline
   hello_world $ source venv/bin/activate
   (venv) ~/hello_world $
```
#### install
```commandline
    pip install Flask
```
#### set up the project
```commandline
   (venv) ~/hello_world $ touch run.py
   (venv) ~/hello_world $ mkdir src
   (venv) ~/hello_world $ touch src/__init__.py 
   (venv) ~/hello_world $ tree -I venv
   /hello_world
   ├── run.py
   └── /src
       └── __init__.py
```
#### ```run.py```
```python
   """
        application entry point.
   """
   from src import app
   
   if __name__ == '__main__':
        app.run(debug=True)
```

#### ```src/__init__.py```
```python
   """
        initialize flask app.
   """
   from flask import Flask

   app = Flask(__name__)
```
*create a new directory: ```src/main```*
```commandline

   (venv) ~/hello_world $ mkdir src/main
```
*inside the newly created directory create:*
```commandline
   (venv) ~/hello_world $ touch src/main/__init__.py
   (venv) ~/hello_world $ touch src/main/views.py
   (venv) ~/hello_world $ mkdir -p src/main/templates/main
   (venv) ~/hello_world $ touch src/main/templates/base.html
   (venv) ~/hello_world $ touch src/main/templates/main/index.html
   (venv) ~/hello_world $ tree -I venv
   .
   ├── run.py
   └── /src
       ├── __init__.py
       └── /main
           ├── __init__.py
           ├── /templates
           │   ├── base.html
           │   └── /main
           │       └── index.html
           └── views.py
```
#### Defining a Blueprint
*inside the ```main/views.py``` file.*
```python
   from flask import Blueprint
   
   """
        Defining  a Blueprint (Blueprint configuration)
   """
   main_bp = Blueprint(
       'main_bp', __name__,
       template_folder='templates'
   )
```
*The first parameter is the name you want to give your Blueprint. This name will be used later for internal routing. I guess it makes sense to keep things consistent by naming our Blueprint main_bp to stay consistent with our variable name. (although it is not really necessary).*

*We also pass an optional keyword argument called ```template_folder```. By defining this argument we are telling our Blueprint that we will have blueprint-specific templates.*

#### Creating routes inside a Blueprint
```python
   from flask import Blueprint
   
   """
        Defining  a Blueprint (Blueprint configuration)
   """
   main_bp = Blueprint(
       'main_bp', __name__,
       template_folder='templates'
   )

   @main_bp.route('/')
   def hello_world():
        return 'hello world'
```
*The only difference is that now we register our route using ```@main_bp.route('/')``` instead of ```@app.route('/')```. Creating our ```home_bp``` Blueprint automatically gives us a decorator function called ```@home_bp``` with which we can register our routes.*

#### Registering a Blueprint
*In the ```src/__init__.py``` file, we will create a Flask app and register our blueprints there:*
```python
   """
        initialize flask app.
   """
   from flask import Flask

   app = Flask(__name__)

   """
        register blueprints
   """
   # from example.main.views import main_bp
   from .main.views import main_bp

   app.register_blueprint(main_bp, url_prefix='/')
```
*To register the blueprint, we use the ```register_blueprint()``` method and pass the name of the blueprint.*

#### Template Routing with Blueprints
*Something to keep in mind is how the Jinja templates find the URLs for the registered routes in Blueprints. In an app without Blueprints, we would use something like this:*
```html
    <a href="{{ url_for('hello_world')">Hello World</a>
```
*But with Blueprints, the links must be defined as:*
```html
   <a href="{{ url_for('main_bp.hello_world')">Hello World</a> 
```
*The ```main_bp``` that we used earlier to define our Blueprint--The string ```... = Blueprints('main_bp', __name__, ...)```, is the internal name that Flask uses to resolve the routes.*

*in the ```src/main/templates/base.html```*
```html
   <!DOCTYPE html>
   <html lang="en">
    <!-- HEAD -->
    <head>
    <meta charset="UTF-8">
        <title>
            {% block title %}
            {% endblock %}
        </title>
    </head>
    <!-- BODY -->
    <body>

        <div class="content">
            {% block content %}
            {% endblock %}
        </div>
    </body>
</html>
```
*-->```src/main/templates/main/index.html```*
```html
   {% extends 'base.html' %}
   {% block title %}
        Hello World
   {% endblock %}
   {% block content %}
        <a href="{{ url_for('main_bp.hello_world')">Hello World</a>

   {% endblock %}
```
*--> ```src/main/views.py```*
```python
   from flask import Blueprint, render_template
   
   """
        Defining  a Blueprint (Blueprint configuration)
   """
   main_bp = Blueprint(
       'main_bp', __name__,
       template_folder='templates'
   )

   @main_bp.route('/')
   def hello_world():
        return render_template('main/index.html')
```

