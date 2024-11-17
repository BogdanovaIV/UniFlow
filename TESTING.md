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
**Dictionaries**
```
----------------------------------------------------------------------
Ran 65 tests in 7.536s

OK
```
**Main**
```
----------------------------------------------------------------------
Ran 9 tests in 0.317s

OK
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

  **Dictionaries**
  ![coverage - dictionaries](documentation/dictionaries/coverage.png)
  **Main**
  ![coverage - main](documentation/main/coverage.png)

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

### Validator P8P (Python)
Quality checking was tested by [PEP8](https://pep8ci.herokuapp.com/#).
All files were checked and did not have errors or warnings.
Notes: Each Python file contains a newline at the end of the file.

**Dictionaries**
- admin.py
 ![validator - admin.py](documentation/dictionaries/p8p/admin.png)
- apps.py
 ![validator - apps.py](documentation/dictionaries/p8p/apps.png)
- forms.py
 ![validator - forms.py](documentation/dictionaries/p8p/forms.png)
- models.py
 ![validator - models.py](documentation/dictionaries/p8p/models.png)
- tests.py
 ![validator - tests.py](documentation/dictionaries/p8p/tests.png)
- test_cases/test-admin.py
 ![validator - test_cases/test-admin.py](documentation/dictionaries/p8p/test-cases-test-admin.png)
- test_cases/test-forms.py
 ![validator - test_cases/test-forms.py](documentation/dictionaries/p8p/test-cases-test-forms.png)
- test_cases/test-models.py
 ![validator - test_cases/test-models.py](documentation/dictionaries/p8p/test-cases-test-models.png)

**Main**
- admin.py
 ![validator - admin.py](documentation/main/p8p/admin.png)
- apps.py
 ![validator - apps.py](documentation/main/p8p/apps.png)
- context-processors.py
 ![validator - context-processors.py](documentation/main/p8p/context-processors.png)
- models.py
 ![validator - models.py](documentation/main/p8p/models.png)
- test.py
 ![validator - tests.py](documentation/main/p8p/tests.png)
- urls.py
 ![validator - urls.py](documentation/main/p8p/urls.png)
- views.py
 ![validator - views.py](documentation/main/p8p/views.png)
- test-cases/test-context-processors.py
 ![validator - views.py](documentation/main/p8p/test-cases-test-context-processors.png)
- test-cases/test-views.py
 ![validator - views.py](documentation/main/p8p/test-cases-test-views.png)