# local_library
![django](https://img.shields.io/github/pipenv/locked/dependency-version/asifo1/TourDay/django)<br>
Local library webapp written in Django (project implementation of MDN), using allauth authentication system. 

## Usage
By visiting the homepage you can register both as a library customer and as a member of the staff:

### As library customer
- **All Books**: all the books avaible in the library, order by title;
- **All Authors**: all authors whose books are in the library, order by title;
- **My Borrowed**: all books that the user currently has on loan;

### As librarian
Same functions as library customer, plus:
- **All borrowed**: all the books currently on loan;
- **Create Author**: allow to add new author to database;
- **Create Book**: allow to add new book to database;
- **Admin Panel**: as librarian, you are allow to visit and interact with django's admin panel;

### Installation
1. Install [python3](https://www.python.org/downloads/), [pip3](https://pip.pypa.io/en/stable/installing/)
2. Install virtualenv
3. Create and active virtualenv
4. Install dependencies from requirements.txt `pip3 install -r requirements.txt`
5. Run Server `python3 manage.py runserver`
6. Check `127.0.0.1:8000`

