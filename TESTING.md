## TESTING

### Purpose Of Testing

The purpose of testing is to make sure the application does not have critical errors and works properly, providing a positive experience for the user.

__Functional Testing__

All the options were tested and worked correctly.

## Automated Testing
This project includes a suite of automated tests to ensure the functionality, reliability, and stability of the application. Below is an overview of the testing setup, the process, and the results.
### Django
1. **Running the Tests**
You can run the test suite using the Django management command:
```
python manage.py test
```
2. **Testing Structure**
The tests are located in a dedicated tests folder for each app. Below is an example of the folder structure:
```
app_name/
├── test-cases/
│   ├── test_models.py
│   ├── test_views.py
│   ├── ...
```
3. **Key Test Results**
After running the tests, here are the results obtained from the project:
- Command: `Python manage.py test`
- Output Summary:
**dictionaries**
```
----------------------------------------------------------------------
Ran 65 tests in 7.536s

OK
```
**main**
```
----------------------------------------------------------------------
Ran 9 tests in 0.317s

OK
```
**student_dashboard**
```
----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
```
- Code Coverage:
  - Prerequisites:
  Before getting reports, make sure you have installed all the dependencies by running:
  ```
  pip install coverage
  ```
  - Command:
  ```
  coverage run --source=app_name manage.py test app_name
  coverage report
  ```
  - Results:

  **dictionaries**
  ![coverage - dictionaries](documentation/dictionaries/coverage.png)
  **main**
  ![coverage - main](documentation/main/coverage.png)
  **student_dashboard**
  ![coverage - student_dashboard](documentation/student-dashboard/coverage.png)

### Jest
1. **Prerequisites**
Before running the tests, make sure you have installed all the dependencies by running:
```
npm install
```
2. **Running the Tests**
To run the test suite, use the following command:
```
npm test
```
3. **Key Test Results**
After running the tests, here are the results obtained from the project:
- Command: `npm test`
- Output Summary:
![outcomes - jest](documentation/jest/jest-outcomes.png)

## Validation
### W3C Validator (HTML)
Quality checking was tested by [Markup validator service](https://validator.w3.org/)
All files were checked and did not have errors or warnings.
- the 'Home' page
 ![validator - the 'Home' page](documentation/main/html/home-page.png)
- the 'Contact' page
 ![validator - the 'Contact' page](documentation/main/html/contact-page.png)
- the 'Login' page
 ![validator - the 'Login' page](documentation/users/html/login.png)
- the 'Register' page
 ![validator - the 'Register' page](documentation/users/html/signup.png)
- the 'Logout' page
 ![validator - the 'Logout' page](documentation/users/html/logout.png)

### W3C CSS Validator (CSS)
Quality checking was tested by [CSS validator service](https://jigsaw.w3.org/css-validator/).
All files were checked and did not have errors or warnings.
- style.css
 ![validator - style.css](documentation/css/w3c-validation.png)

### JS Hint
Quality checking was tested by [JS Hint](https://jshint.com/).
All files were checked and did not have errors or warnings.
- dashboard.js
 ![validator - dashboard.js](documentation/jshint/dashboard.png)
- google-map-module.js
 ![validator - google-map-module.js](documentation/jshint/google-map-module.png)
- tests/dashboard-test.js
 ![validator - tests/dashboard-test.js](documentation/jshint/dashboard-test.png)
- tests/google-map-module.js
 ![validator - tests/google-map-module-test.js](documentation/jshint/google-map-module-test.png)

### Validator PEP8 (Python)
Quality checking was tested by [PEP8](https://pep8ci.herokuapp.com/#).
All files were checked and did not have errors or warnings.
Notes: Each Python file contains a newline at the end of the file.

**dictionaries**
- admin.py
 ![validator - admin.py](documentation/dictionaries/pep8/admin.png)
- apps.py
 ![validator - apps.py](documentation/dictionaries/pep8/apps.png)
- forms.py
 ![validator - forms.py](documentation/dictionaries/pep8/forms.png)
- models.py
 ![validator - models.py](documentation/dictionaries/pep8/models.png)
- tests.py
 ![validator - tests.py](documentation/dictionaries/pep8/tests.png)
- test_cases/test-admin.py
 ![validator - test_cases/test-admin.py](documentation/dictionaries/pep8/test-cases-test-admin.png)
- test_cases/test-forms.py
 ![validator - test_cases/test-forms.py](documentation/dictionaries/pep8/test-cases-test-forms.png)
- test_cases/test-models.py
 ![validator - test_cases/test-models.py](documentation/dictionaries/pep8/test-cases-test-models.png)

**main**
- admin.py
 ![validator - admin.py](documentation/main/pep8/admin.png)
- apps.py
 ![validator - apps.py](documentation/main/pep8/apps.png)
- context-processors.py
 ![validator - context-processors.py](documentation/main/pep8/context-processors.png)
- models.py
 ![validator - models.py](documentation/main/pep8/models.png)
- tests.py
 ![validator - tests.py](documentation/main/pep8/tests.png)
- urls.py
 ![validator - urls.py](documentation/main/pep8/urls.png)
- views.py
 ![validator - views.py](documentation/main/pep8/views.png)
- test-cases/test-context-processors.py
 ![validator - test-cases/test-context-processors.py](documentation/main/pep8/test-cases-test-context-processors.png)
- test-cases/test-views.py
 ![validator - test-cases/test-views.py](documentation/main/p8p/test-cases-test-views.png)

**student_dashboard**
- admin.py
 ![validator - admin.py](documentation/student-dashboard/pep8/admin.png)
- apps.py
 ![validator - apps.py](documentation/student-dashboard/pep8/apps.png)
- models.py
 ![validator - models.py](documentation/student-dashboard/pep8/models.png)
- tests.py
 ![validator - tests.py](documentation/student-dashboard/pep8/tests.png)
- urls.py
 ![validator - urls.py](documentation/student-dashboard/pep8/urls.png)
- views.py
 ![validator - views.py](documentation/student-dashboard/pep8/views.png)
