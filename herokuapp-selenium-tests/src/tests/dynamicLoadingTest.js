const { expect } = require('chai');
const { Builder } = require('selenium-webdriver');
const { Options } = require('selenium-webdriver/chrome');
const DynamicLoadingPage = require('../pages/dynamicLoadingPage');

describe('Dynamic Loading Test', function () {
  this.timeout(30000); // Extend timeout for asynchronous operations

  let driver;
  let dynamicLoadingPage;

  before(async function () {
    // Set up the WebDriver
    const chromeOptions = new Options();
    // chromeOptions.addArguments('--headless'); // Comment out or remove this line to run in normal mode
    driver = await new Builder().forBrowser('chrome').setChromeOptions(chromeOptions).build();

    // Initialize the page objects
    dynamicLoadingPage = new DynamicLoadingPage(driver);

    // Navigate to the dynamic loading page
    await dynamicLoadingPage.navigate();
  });

  after(async function () {
    // Quit the WebDriver
    await driver.quit();
  });

  it('should load hidden element', async function () {
    // Click on the "Example 1: Element on page that is hidden" link
    await dynamicLoadingPage.clickExample1Link();

    // Click on the "Start" button
    await dynamicLoadingPage.clickStartButton();

    // Wait for the loading spinner to disappear
    await dynamicLoadingPage.waitForSpinnerToDisappear();

    // Get the text of the loaded element
    const loadedElementText = await dynamicLoadingPage.getLoadedElementText();

    // Verify that the loaded element text is correct
    expect(loadedElementText).to.equal('Hello World!');
  });

  it('should load element after delay', async function () {
    // Navigate back to the main dynamic loading page
    await dynamicLoadingPage.navigate();

    // Click on the "Example 2: Element rendered after the fact" link
    await dynamicLoadingPage.clickExample2Link();

    // Click on the "Start" button
    await dynamicLoadingPage.clickStartButton();

    // Wait for the loading spinner to disappear
    await dynamicLoadingPage.waitForSpinnerToDisappear();

    // Get the text of the loaded element
    const loadedElementText = await dynamicLoadingPage.getLoadedElementText();

    // Verify that the loaded element text is correct
    expect(loadedElementText).to.equal('Hello World!');
  });
});
