const { Builder } = require('selenium-webdriver');
const { expect } = require('chai');
const LoginPage = require('../pages/loginPage');

describe('Login functionality tests', function() {
  this.timeout(30000); // Extend timeout for asynchronous operations

  let driver;

  before(async function() {
    // Setup code before any tests run. Initialize the WebDriver instance here.
    driver = await new Builder().forBrowser('chrome').build();
  });

  after(async function() {
    // Teardown code after all tests run. Quit the WebDriver instance here.
    await driver.quit();
  });

  it('should log in successfully with valid credentials', async function() {
    const loginPage = new LoginPage(driver);

    await driver.get('https://the-internet.herokuapp.com/login');

    await loginPage.enterUsername('tomsmith');
    await loginPage.enterPassword('SuperSecretPassword!');
    await loginPage.clickLoginButton();

    // Wait for 5 seconds for manual verification
    await driver.sleep(5000);

    // Example assertion (you'll need to replace this with actual validation logic)
    // This is just a placeholder to demonstrate how you might assert that the login was successful
    const currentUrl = await driver.getCurrentUrl();
    expect(currentUrl).to.include('/secure');
  });

  // Add more test cases here using additional `it` blocks
});
