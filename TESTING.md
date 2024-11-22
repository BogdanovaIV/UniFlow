## TESTING

### Purpose Of Testing

The purpose of testing is to make sure the application does not have critical errors and works properly, providing a positive experience for the user.

## Functional Testing

Functional testing ensures that all features and functionalities of the application work as expected, regardless of the device or screen size.

| feature | action | expected result | tested | passed | comments |
| --- | --- | --- | --- | --- | --- |
| Navigation bar | | | | | |
| Logo and Logo name | Click the Logo link | The Logo link opens the Home page | Yes | Yes | - |
| The Logo link is hovered over on large devices | Hover over the Logo link | The Logo link changes color | Yes | Yes | - |
| The Home link | Click the Home link | The Home link opens the Home page | Yes | Yes | - |
| The Home link is hovered over on large devices | Hover over the Home link | The Home link changes color | Yes | Yes | - |
| The Contact link | Click the Contact link | The Contact link opens the Contact page | Yes | Yes | - |
| The Contact link is hovered over on large devices | Hover over the Contact link | The Contact link changes color | Yes | Yes | - |
| The Register link | Click the Register link | The Register link opens the Register page | Yes | Yes | - |
| The Register link is hovered over on large devices | Hover over the Register link | The Register link changes color | Yes | Yes | - |
| The Login link | Click the Login link | The Login link opens the Login page | Yes | Yes | - |
| The Login link is hovered over on large devices | Hover over the Login link | The Login link changes color | Yes | Yes | - |
| The Logout link | Click the Logout link | The Logout link opens the Logout page | Yes | Yes | - |
| The Logout link is hovered over on large devices | Hover over the Logout link | The Logout link changes color | Yes | Yes | - |
| The Dashboard link | Click the Dashboard link | The Dashboard link opens the Dashboard page | Yes | Yes | - |
| The Dashboard link is hovered over on large devices | Hover over the Logout link | The Dashboard link changes color | Yes | Yes | - |
| Footer | | | | | |
| The E-mail link | Click the E-mail link | The E-mail link offers to choose an application to send e-mail. | Yes | Yes | - |
| The E-mai link is hovered over on large devices | Hover over the E-mai link | The E-mai link changes color | Yes | Yes | - |
| The Twitter link | Click the Twitter link | The Twitter link opens the Twitter page | Yes | Yes | - |
| The Twitter link is hovered over on large devices | Hover over the Twitter link | The Twitter link changes color | Yes | Yes | - |
| The Facebook link | Click the Facebook link | The Facebook link opens the Facebook page | Yes | Yes | - |
| The Facebook link is hovered over on large devices | Hover over the Facebook link | The Facebook link changes color | Yes | Yes | - |
| The Instagram link | Click the Instagram link | The Instagram link opens the Instagram page | Yes | Yes | - |
| The Instagram link is hovered over on large devices | Hover over the Instagram link | The Instagram link changes color | Yes | Yes | - |
| The Home page | | | | | |
| The content | Go to the Home page | The content is consistent and full | Yes | Yes | - |
| The Home link | Go to the Home page | The Home link has bold font | Yes | Yes | - |
| The Contact page | | | | | |
| The content | Go to the Contact page | The content has a map and contact infotmation | Yes | Yes | - |
| The Contact link | Go to the Contact page | The Contact link has bold font | Yes | Yes | - |
| The map | Go to the Contact page | The map displays a correct location | Yes | Yes | - |
| The Logout page | | | | | |
| The content | Go to the Logout page | The content has confirmation to sign out and an appropriate button. | Yes | Yes | - |
| The Logout link | Go to the Logout page | The Logout link has bold font | Yes | Yes | - |
| The Sign-out button | Click the Sign-out button | The Sign-out button logs out. | Yes | Yes | - |
| The Login page | | | | | |
| The content | Go to the Login page | The content has the 'Sign up' link, the 'Sign in' button, the 'Remember me' checkbox, and the fields: username and password. | Yes | Yes | - |
| The Login link | Go to the Login page | The Login link has bold font | Yes | Yes | - |
| Login process | Fill in the fields: username and password, and click on the Sign-in button | The system authenticates the user and displays messages if something goes wrong. | Yes | Yes | - |
| The Register page | | | | | |
| The content | Go to the Register page | The content has the 'Sign in' link, the 'Sign up' button, and the fields: email, first name, last name, password, and password again. | Yes | Yes | - |
| Register process | Fill in the fields: email, first name, last name, password, and password again and click the Sign-up button | The system checks that all fields are filled, if it is so it creates a new user with "Student" permission in the database and redirect to "Dashboard" page. If it is not, the system displays the message with an error description. | Yes | Yes | - |
| The Register link | Go to the Register page | The Register link has bold font | Yes | Yes | - |

## Performance Testing
To ensure the application is optimized and performs efficiently, we use **[Lighthouse](https://developers.google.com/web/tools/lighthouse)** for performance testing. 

Lighthouse is an open-source, automated tool for improving the quality of web pages. It provides insights and metrics across several categories, including:

1. **Performance**: Evaluates load times, speed indices, and how quickly key content is displayed.
2. **Accessibility**: Checks the site's compliance with accessibility standards.
3. **Best Practices**: Analyzes adherence to modern web development practices.
4. **SEO**: Assesses the website's ability to rank on search engines.
5. **Progressive Web App (PWA)**: Verifies the features and reliability of a PWA (if applicable).
- the 'Home' page
  ![Lighthouse - the 'Home' page](documentation/light-house/home.png)
- the 'Contact' page
  ![Lighthouse - the 'Contact' page](documentation/light-house/contact.png)
- the 'Login' page
  ![Lighthouse - the 'Login' page](documentation/light-house/login.png)
- the 'Register' page
  ![Lighthouse - the 'Register' page](documentation/light-house/signup.png)
- the 'Logout' page
  ![Lighthouse - the 'Logout' page](documentation/light-house/logout.png)
- the 'Dashboard' page for students
  ![Lighthouse - the 'Dashboard' page for students](documentation/light-house/student-dashboard.png)
- the 'Dashboard' page for tutors - button 'Schedule'
  ![Lighthouse - the 'Dashboard' page for tutors - button 'Schedule'](documentation/light-house/tutor-dashboard-shedule.png)
- the 'Add shedule' page
  ![Lighthouse - the 'Dashboard' page for tutors - button 'Schedule'](documentation/light-house/add-schedule.png)
- the 'Edit shedule' page
  ![Lighthouse - the 'Dashboard' page for tutors - button 'Schedule'](documentation/light-house/edit-schedule.png)
- the 'Dashboard' page for tutors - button 'Schedule template'
  ![Lighthouse - the 'Dashboard' page for tutors - button 'Schedule'](documentation/light-house/tutor-schedule-template.png)
- the 'Add shedule template' page
  ![Lighthouse - the 'Dashboard' page for tutors - button 'Schedule'](documentation/light-house/add-shedule-template.png)
- the 'Edit shedule template' page
  ![Lighthouse - the 'Dashboard' page for tutors - button 'Schedule'](documentation/light-house/edit-schedule-template.png)
- the '403-error' page
  ![Lighthouse - the '403-error' page](documentation/light-house/403.png)
- the '404-error' page
  ![Lighthouse - the '403-error' page](documentation/light-house/404.png)

## User Interface Testing

Ensuring a consistent and responsive user interface across different screen sizes is crucial for an optimal user experience. Here are the steps and considerations for UI testing:

### Displaying on Different Screens
The application was tested on various screen sizes and devices to ensure responsiveness and usability:
1. **Desktop Screens**: Verify layout and design on common resolutions like 1920x1080 and 1366x768.
2. **Tablet Screens**: Check functionality and layout for resolutions such as 768x1024 (portrait) and 1024x768 (landscape).
3. **Mobile Screens**: Test responsiveness on small screens like 360x640 and 375x667.
- the 'Home' page
  ![Responsiveness - the 'Home' page](documentation/responsiveness/home.png)
- the 'Contact' page
  ![Responsiveness - the 'Contact' page](documentation/responsiveness/contact.png)
- the 'Login' page
  ![Responsiveness - the 'Login' page](documentation/responsiveness/login.png)
- the 'Register' page
  ![Responsiveness - the 'Register' page](documentation/responsiveness/signup.png)
- the 'Logout' page
  ![v - the 'Logout' page](documentation/responsiveness/logout.png)
- the 'Dashboard' page for students
  ![Responsiveness - the 'Dashboard' page for students](documentation/responsiveness/student-dashboard.png)
- the 'Dashboard' page for tutors - button 'Schedule'
  ![Responsiveness - the 'Dashboard' page for tutors - button 'Schedule'](documentation/responsiveness/tutor-schedule.png)
- the 'Add shedule' page
  ![Responsiveness - the 'Dashboard' page for tutors - button 'Schedule'](documentation/responsiveness/add-schedule.png)
- the 'Edit shedule' page
  ![Responsiveness - the 'Dashboard' page for tutors - button 'Schedule'](documentation/responsiveness/edit-schedule.png)
- the 'Dashboard' page for tutors - button 'Schedule template'
  ![Responsiveness - the 'Dashboard' page for tutors - button 'Schedule'](documentation/responsiveness/tutor-schedule-template.png)
- the 'Add shedule template' page
  ![Responsiveness - the 'Dashboard' page for tutors - button 'Schedule'](documentation/responsiveness/add-schedule-template.png)
- the 'Edit shedule template' page
  ![Responsiveness - the 'Dashboard' page for tutors - button 'Schedule'](documentation/responsiveness/edit-schedule-template.png)
- the '403-error' page
  ![Responsiveness - the '403-error' page](documentation/responsiveness/403.png)
- the '404-error' page
  ![Responsiveness - the '403-error' page](documentation/responsiveness/404.png)

### Testing on Different Browsers
The following browsers are commonly tested to ensure broad compatibility:
**Google Chrome**: Latest version and recent updates.
- the 'Home' page
  ![Google Chrome - the 'Home' page](documentation/google/home.png)
- the 'Contact' page
  ![Google Chrome - the 'Contact' page](documentation/google/contact.png)
- the 'Login' page
  ![Google Chrome - the 'Login' page](documentation/google/login.png)
- the 'Register' page
  ![Google Chrome - the 'Register' page](documentation/google/signup.png)
- the 'Logout' page
  ![Google Chrome - the 'Logout' page](documentation/google/logout.png)
- the 'Dashboard' page for students
  ![Google Chrome - the 'Dashboard' page for students](documentation/google/student-dashboard.png)
- the 'Dashboard' page for tutors - button 'Schedule'
  ![Google Chrome - the 'Dashboard' page for tutors - button 'Schedule'](documentation/google/tutor-schedule.png)
- the 'Add shedule' page
  ![Google Chrome - the 'Dashboard' page for tutors - button 'Schedule'](documentation/google/add-schedule.png)
- the 'Edit shedule' page
  ![Google Chrome - the 'Dashboard' page for tutors - button 'Schedule'](documentation/google/edit-schedule.png)
- the 'Dashboard' page for tutors - button 'Schedule template'
  ![Google Chrome - the 'Dashboard' page for tutors - button 'Schedule'](documentation/google/tutor-schedule-template.png)
- the 'Add shedule template' page
  ![Google Chrome - the 'Dashboard' page for tutors - button 'Schedule'](documentation/google/add-schedule-template.png)
- the 'Edit shedule template' page
  ![Google Chrome - the 'Dashboard' page for tutors - button 'Schedule'](documentation/google/edit-schedule-template.png)
- the '403-error' page
  ![Google Chrome - the '403-error' page](documentation/google/403.png)
- the '404-error' page
  ![Google Chrome - the '403-error' page](documentation/google/404.png)

**Mozilla Firefox**: Standard version and ESR (Extended Support Release).
- the 'Home' page
  ![Mozilla Firefox - the 'Home' page](documentation/firefox/home.png)
- the 'Contact' page
  ![Mozilla Firefox - the 'Contact' page](documentation/firefox/contact.png)
- the 'Login' page
  ![Mozilla Firefox - the 'Login' page](documentation/firefox/login.png)
- the 'Register' page
  ![Mozilla Firefox - the 'Register' page](documentation/firefox/signup.png)
- the 'Logout' page
  ![Mozilla Firefox - the 'Logout' page](documentation/firefox/logout.png)
- the 'Dashboard' page for students
  ![Mozilla Firefox - the 'Dashboard' page for students](documentation/firefox/student-dashboard.png)
- the 'Dashboard' page for tutors - button 'Schedule'
  ![Mozilla Firefox - the 'Dashboard' page for tutors - button 'Schedule'](documentation/firefox/tutor-schedule.png)
- the 'Add shedule' page
  ![Mozilla Firefox - the 'Dashboard' page for tutors - button 'Schedule'](documentation/firefox/add-schedule.png)
- the 'Edit shedule' page
  ![Mozilla Firefox - the 'Dashboard' page for tutors - button 'Schedule'](documentation/firefox/edit-schedule.png)
- the 'Dashboard' page for tutors - button 'Schedule template'
  ![Mozilla Firefox - the 'Dashboard' page for tutors - button 'Schedule'](documentation/firefox/tutor-schedule-template.png)
- the 'Add shedule template' page
  ![Mozilla Firefox - the 'Dashboard' page for tutors - button 'Schedule'](documentation/firefox/add-schedule-template.png)
- the 'Edit shedule template' page
  ![Mozilla Firefox - the 'Dashboard' page for tutors - button 'Schedule'](documentation/firefox/edit-schedule-template.png)
- the '403-error' page
  ![Mozilla Firefox - the '403-error' page](documentation/firefox/403.png)
- the '404-error' page
  ![Mozilla Firefox - the '403-error' page](documentation/firefox/404.png)

**Microsoft Edge**: Chromium-based versions.
- the 'Home' page
  ![Microsoft Edge - the 'Home' page](documentation/edge/home.png)
- the 'Contact' page
  ![Microsoft Edge - the 'Contact' page](documentation/edge/contact.png)
- the 'Login' page
  ![Microsoft Edge - the 'Login' page](documentation/edge/login.png)
- the 'Register' page
  ![Microsoft Edge - the 'Register' page](documentation/edge/signup.png)
- the 'Logout' page
  ![Microsoft Edge - the 'Logout' page](documentation/edge/logout.png)
- the 'Dashboard' page for students
  ![Microsoft Edge - the 'Dashboard' page for students](documentation/edge/student-dashboard.png)
- the 'Dashboard' page for tutors - button 'Schedule'
  ![Microsoft Edge - the 'Dashboard' page for tutors - button 'Schedule'](documentation/edge/tutor-schedule.png)
- the 'Add shedule' page
  ![Microsoft Edge - the 'Dashboard' page for tutors - button 'Schedule'](documentation/edge/add-schedule.png)
- the 'Edit shedule' page
  ![Microsoft Edge - the 'Dashboard' page for tutors - button 'Schedule'](documentation/edge/edit-schedule.png)
- the 'Dashboard' page for tutors - button 'Schedule template'
  ![Microsoft Edge - the 'Dashboard' page for tutors - button 'Schedule'](documentation/edge/tutor-schedule-template.png)
- the 'Add shedule template' page
  ![Microsoft Edge - the 'Dashboard' page for tutors - button 'Schedule'](documentation/edge/add-schedule-template.png)
- the 'Edit shedule template' page
  ![Microsoft Edge - the 'Dashboard' page for tutors - button 'Schedule'](documentation/edge/edit-schedule-template.png)
- the '403-error' page
  ![Microsoft Edge - the '403-error' page](documentation/edge/403.png)
- the '404-error' page
  ![Microsoft Edge - the '403-error' page](documentation/edge/404.png)

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
**tutor_dashboard**
```
----------------------------------------------------------------------
Ran 68 tests in 21.649s

OK
```
**users**
```
----------------------------------------------------------------------
Ran 14 tests in 3.807s

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

  **dictionaries**
    ![coverage - dictionaries](documentation/dictionaries/coverage.png)
  **main**
    ![coverage - main](documentation/main/coverage.png)
  **student_dashboard**
    ![coverage - student_dashboard](documentation/student-dashboard/coverage.png)
  **tutor_dashboard**
    ![coverage - tutor_dashboard](documentation/tutor-dashboard/coverage.png)
  **users**
    ![coverage - users](documentation/users/coverage.png)

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
All files were checked and did not have errors.
These warnings do not indicate issues that would degrade the user experience or functionality of the application. The `aria-label` attributes were added deliberately to enhance accessibility for screen readers. The use of `aria-label` conforms to accessibility best practices by providing explicit descriptions when needed. The warnings do not affect the semantic correctness or performance of the application.
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
- the 'Dashboard' page for students
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 125`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.
  2. Possible misuse of `aria-label`
    `Location: Line ...` the number of those warnings depends on the number of student's marks.
     ```
     <span class="badge text-bg-primary rounded-pill position-absolute end-0" aria-label="Your mark: 80 for Anatomy">
     ```
      This warning appears because the `aria-label` provides descriptive information that could also be visually apparent. However, it is intentionally included to ensure the information is accessible for users of screen readers, even if the visual context is unavailable.
  ![validator - the 'Dashboard' page for students](documentation/student-dashboard/html/dashboard.png)
- the 'Dashboard' page for tutors - button 'Schedule'
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 109`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.
  2. Possible misuse of `aria-label`
    `Location: Line ...` the number of those warnings depends on the number of student's marks.
     ```
     <span class="badge text-bg-primary rounded-pill position-absolute end-0" aria-label="Number of marks for this subject">
     ```
      This warning appears because the `aria-label` provides descriptive information that could also be visually apparent. However, it is intentionally included to ensure the information is accessible for users of screen readers, even if the visual context is unavailable.

  ![validator - the 'Dashboard' page for tutors - button 'Schedule'](documentation/tutor-dashboard/html/dashboard-schedule.png)

- the 'Add shedule' page
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 94`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.

  ![validator - the 'Dashboard' page for tutors - button 'Schedule'](documentation/tutor-dashboard/html/add-schedule.png)

- the 'Edit shedule' page
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 94`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.

  ![validator - the 'Dashboard' page for tutors - button 'Schedule'](documentation/tutor-dashboard/html/edit-schedule.png)

- the 'Dashboard' page for tutors - button 'Schedule template'
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 109`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.
  ![validator - the 'Dashboard' page for tutors - button 'Schedule'](documentation/tutor-dashboard/html/dashboard-schedule-template.png)

- the 'Add shedule template' page
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 94`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.
  ![validator - the 'Dashboard' page for tutors - button 'Schedule'](documentation/tutor-dashboard/html/dashboard-schedule-template.png)
  
- the 'Edit shedule template' page
  **Warnings**
  1. Possible misuse of `aria-label`
     `Location: Line 94`
     ```
     <span data-bs-toggle="tooltip" aria-label="Open instructions modal for dashboard usage tips" data-bs-original-title="Open instructions modal for dashboard usage tips">
     ```
      This warning is triggered because the `aria-label` duplicates the information provided by `data-bs-original-title`. However, the use of aria-label here is intentional to ensure accessibility for users relying on assistive technologies, as some screen readers may not fully interpret Bootstrap tooltips.
  ![validator - the 'Dashboard' page for tutors - button 'Schedule'](documentation/tutor-dashboard/html/edit-shedule-template.png)

- the '403-error' page
  ![validator - the '403-error' page](documentation/uni-flow/html/403.png)

- the '404-error' page
  ![validator - the '403-error' page](documentation/uni-flow/html/404.png)

- the '500-error' page
  ![validator - the '403-error' page](documentation/uni-flow/html/500.png)

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

**tutor_dashboard**
- admin.py
  ![validator - admin.py](documentation/tutor-dashboard/pep8/admin.png)
- apps.py
  ![validator - apps.py](documentation/tutor-dashboard/pep8/apps.png)
- models.py
  ![validator - models.py](documentation/tutor-dashboard/pep8/models.png)
- tests.py
  ![validator - tests.py](documentation/tutor-dashboard/pep8/tests.png)
- urls.py
  ![validator - urls.py](documentation/tutor-dashboard/pep8/urls.png)
- test_cases/test_view_schedule_template.py
  ![validator - test_cases/test_view_schedule_template.py](documentation/tutor-dashboard/pep8/test-view-schedule-template.png)
- test_cases/test_view_schedule.py
  ![validator - test_cases/test_view_schedule.py](documentation/tutor-dashboard/pep8/test-view-schedule.png)
- test_cases/test_view_student_mark.py
  ![validator - test_cases/test_view_student_mark.py](documentation/tutor-dashboard/pep8/test-view-student-mark.png)
- views/init.py
  ![validator - views/init.py](documentation/tutor-dashboard/pep8/views-init.png)
- views/schedule_template_views.py
  ![validator - views/schedule_template_views.py](documentation/tutor-dashboard/pep8/schedule-template-views.png)
- views/schedule_views.py
  ![validator - views/schedule_views.py](documentation/tutor-dashboard/pep8/schedule-views.png)
- views/student_mark_views.py
  ![validator - views/student_views.py](documentation/tutor-dashboard/pep8/student-mark-views.png)

**users**
- admin.py
  ![validator - admin.py](documentation/users/pep8/admin.png)
- apps.py
  ![validator - apps.py](documentation/users/pep8/apps.png)
- context_processors.py
  ![validator - context_processors.py](documentation/users/pep8/context-processors.png)
- forms.py
  ![validator - forms.py](documentation/users/pep8/forms.png)
- models.py
  ![validator - models.py](documentation/users/pep8/models.png)
- signals.py
  ![validator - signals.py](documentation/users/pep8/signals.png)  
- tests.py
  ![validator - tests.py](documentation/users/pep8/tests.png)
- urls.py
  ![validator - urls.py](documentation/users/pep8/urls.png)
- views.py
  ![validator - views.py](documentation/users/pep8/views.png)
- test_cases/test_context_processors.py
  ![validator - test_cases/test_context_processors.py](documentation/users/pep8/test-context-processors.png)
- test_cases/test_forms.py
  ![validator - test_cases/test_forms.py](documentation/users/pep8/test-forms.png)
- test_cases/test_models.py
  ![validator - test_cases/test_models.py](documentation/users/pep8/test-models.png)
- test_cases/test_signals.py
  ![validator - test_cases/test_signals.py](documentation/users/pep8/test-signals.png)
- test_cases/test_views.py
  ![validator - test_cases/test_views.py](documentation/users/pep8/test-views.png)

## Bugs

__Solved Bugs__

 - When the user does not fill in 'date' field in the selection and then clicks on the "Fill" button, the system displays an error.
  Solution: Add the condition which checks it.
  ```
  <input type="hidden" name="date" {% if form.date.value %} value="{{ form.date.value }}" {% endif %}>
  <input type="hidden" name="study_group" {% if form.study_group.value %} value="{{ form.study_group.value }}" {% endif %}>
  ```
   Solution: Use window.innerHeight - lengthShip as the edge of the screen
 - The system did not display correct current year in the footer.
  Solution: Use global context to display it.
  ```
   TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.user_groups',
                'main.context_processors.current_year',
            ],
        },
    },
   ]
  ```
 - When the user does not fill in the selection and then click on a cell to add new schedule template or schedule, the system opened the 'Add schedule' page.
  Solution: Checking the selection and do nothing if the selection is not selected.

  ```
  <a href="{% if selection_valid %}{% url 'tutor:add_schedule' %}?date={{ weekday_info.date_str }}&study_group={{ form.study_group.value }}&order_number={{ order }}{% else %}#{% endif %}" class="text-decoration-none text-reset" aria-label="Add new schedule for date {{ weekday_info.date }} and study group {{ form.study_group.value }}">
  ``` 
   
__Unsolved Bugs__

 - None.

__Mistakes__

 - Using different formats of 'Commit' comments.
 - Some grammar and spelling mistakes.