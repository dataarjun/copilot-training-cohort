# herokuapp-selenium-tests

This project contains automated tests for the website [https://the-internet.herokuapp.com](https://the-internet.herokuapp.com). The tests are implemented using Selenium and written in JavaScript.

## Project Structure

```
herokuapp-selenium-tests
├── src
│   ├── tests
│   │   ├── loginTest.js
│   │   ├── dropdownTest.js
│   │   ├── dynamicLoadingTest.js
│   │   └── fileUploadTest.js
│   └── pages
│       ├── loginPage.js
│       ├── dropdownPage.js
│       ├── dynamicLoadingPage.js
│       └── fileUploadPage.js
├── package.json
├── .gitignore
└── README.md
```

## Test Files

### `src/tests/loginTest.js`

This file contains the test cases for the login functionality. It includes separate functions to perform different tests related to login. Each test includes a static wait of 5 seconds for manual verification after performing the operations.

### `src/tests/dropdownTest.js`

This file contains the test cases for the dropdown functionality. It includes separate functions to perform different tests related to dropdown. Each test includes a static wait of 5 seconds for manual verification after performing the operations.

### `src/tests/dynamicLoadingTest.js`

This file contains the test cases for the dynamic loading functionality. It includes separate functions to perform different tests related to dynamic loading. Each test includes a static wait of 5 seconds for manual verification after performing the operations.

### `src/tests/fileUploadTest.js`

This file contains the test cases for the file upload functionality. It includes separate functions to perform different tests related to file upload. Each test includes a static wait of 5 seconds for manual verification after performing the operations.

## Page Files

### `src/pages/loginPage.js`

This file exports a class `LoginPage` which represents the login page of the website. It includes methods to interact with the login page elements.

### `src/pages/dropdownPage.js`

This file exports a class `DropdownPage` which represents the dropdown page of the website. It includes methods to interact with the dropdown page elements.

### `src/pages/dynamicLoadingPage.js`

This file exports a class `DynamicLoadingPage` which represents the dynamic loading page of the website. It includes methods to interact with the dynamic loading page elements.

### `src/pages/fileUploadPage.js`

This file exports a class `FileUploadPage` which represents the file upload page of the website. It includes methods to interact with the file upload page elements.

## Installation

To install the dependencies, run the following command:

```
npm install
```

## Running the Tests

To run the tests, use the following command:

```
npm test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.