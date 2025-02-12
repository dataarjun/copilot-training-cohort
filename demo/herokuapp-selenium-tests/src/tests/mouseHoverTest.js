// Define a test case to perform mouse hover operations on the internet-herokuapp page.
const { Builder, By, Actions } = require('selenium-webdriver');
const { expect } = require('chai');

describe('Mouse Hover Test', function() {
  this.timeout(30000);
  let driver;

  before(async function() {
    driver = await new Builder().forBrowser('chrome').build();
  });

  after(async function() {
    await driver.quit();
  });

  it('should hover over the first image', async function() {
    await driver.get('https://the-internet.herokuapp.com/hovers');

    // Find the first image element
    const firstImage = await driver.findElement(By.css('.figure:nth-of-type(1)'));

    // Create an Actions object
    const actions = driver.actions({ async: true });

    // Perform a mouse hover over the first image
    await actions.move({ origin: firstImage }).perform();

    // Wait for 5 seconds for manual verification
    await driver.sleep(5000);

    const figcaption = await driver.findElement(By.css('.figcaption')).isDisplayed();
    expect(figcaption).to.be.true;

  });
});