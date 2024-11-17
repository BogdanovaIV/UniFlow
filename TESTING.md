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
- Code Coverage:
  - Command:
  ```
  coverage run --source=app_name manage.py test app_name
  coverage report
  ```
  - Results:
  
  **Dictionaries**
  ![coverage - dictionaries](documentation/dictionaries/coverage.png)


## Validation

### Validator P8P (Python)
Quality checking was tested by [PEP8](https://pep8ci.herokuapp.com/#).
All files were checked and did not have errors or warnings.
Notes: Each Python file contains  a newline at the end of the file
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
 ![validator - models.py](documentation/dictionaries/p8p/tests.png)
- test_cases/test-admin.py
 ![validator - models.py](documentation/dictionaries/p8p/test-cases-test-admin.png)
- test_cases/test-forms.py
 ![validator - models.py](documentation/dictionaries/p8p/test-cases-test-forms.png)
- test_cases/test-models.py
 ![validator - models.py](documentation/dictionaries/p8p/test-cases-test-models.png)