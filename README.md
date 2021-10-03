#### Video Demo:  <https://youtu.be/xjKgcatV7Sw>
#### Description: Cocktail-me is a web application using Flask and SQL where users can control their stock of ingrediends and check possible cocktails recipes according to selected ingredient in users list.

#### The application runs using the folowing resources
  ### Static
  - drinkico.png: the icon used in HTML templates
  - styles.css: file containing app formating style sheet

  ### Templates
  - index: main page with shows the ingredients inventory list, also where is possible to add or remove itens
  - layout: structures of page layout that is used in others pages loaded by jinja (title, main and footer)
  - login: request page for login user or register new users
  - cocktailmaker: page where user can select an ingredient an check for recipes
  - recipe: used as template for posting selected recipe from cocktailmaker page

  ### Cocktail-me.db: this is the SQL database with below Schema:
  - cocktails: table containing all recipes and stories of cocktails available in the application
  - drinks: list with possible drinks, beverages and ingredients which users can select in lists
  - inventory: table that controls users transactions of adding and removing ingredients, making possible the table of each user ingredients stock
  - users: table which control users data and passwords hash to verify users login

  ### application.py
  - main python script with a serie of function:
    - index()
      - this function is responsible for the first entrance of user, it may check if user has been identified and proceed for index page if True, if user is not know it will involk the login page to be shown.
      - in index page it will query the SQL database to:
        - inform the list of drinks/ingredients availabe to be add
        - inform the list of current items add to the list so it will be shown as a table and available to be remove from list

    - login()
      - responsible for login or register a new user. it will check field information with database for login or, in case of new register, it will check the availability of username in users database

    - logout()
      - function release information of actual user so it wil request a new login

    - cocktailmaker()
      - the page query the SQL for two basic operation:
        - provide the list of items in users list
        - check possibles recipes using the ingredient selected
      - it also present the table of possible drinks/cocktails recipes in a table, which user can click on it's name an access the full recipe

    - recipe()
      - Generated only by the page cocktailmaker, it will load the value of recipe selected by the user to generate the page containing the recipe and curiosity of the cocktail.

  ### helpers.py
  - python script append containing:
    - login_required()
      - function for request user login identification to let user see others templates and app function
    - checkchars(var)
      - this function is used in loggin and register (also on it's password and confirmation) fields to garantee the non-usage of critical characteres that may cause vulnerability to application and free access to database information

  ### requirements.txt
  - text file containing the mainly libraries need