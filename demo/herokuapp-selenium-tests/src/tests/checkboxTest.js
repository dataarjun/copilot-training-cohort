// Define a test case to perform select/deselect operations on checkboxes using the internet-herokuapp page.
const { Builder } = require('selenium-webdriver');
const {expect} = require('chai');

describe('Checkbox Test', function() {
  this.timeout(30000);
  let driver;

  before(async function() {
    driver = await new Builder().forBrowser('chrome').build();
  });

  after(async function() {
    await driver.quit();
  });

  it('should select and deselect checkboxes', async function() {
    await driver.get('https://the-internet.herokuapp.com/checkboxes');

    // Find the checkboxes
    const checkboxes = await driver.findElements({css: 'input[type="checkbox"]'});

    // Verify that the first checkbox is unchecked
    expect(await checkboxes[0].isSelected()).to.be.false;

    // Verify that the second checkbox is checked
    expect(await checkboxes[1].isSelected()).to.be.true;

    // check the first checkbbox if it is not checked
    if (!await checkboxes[0].isSelected()) {
      await checkboxes[0].click();
    }

    // Verify that the first checkbox is checked
    expect(await checkboxes[0].isSelected()).to.be.true;

    // Uncheck the second checkbox if it's already checked
    if (await checkboxes[1].isSelected()) {
      await checkboxes[1].click();
    }

    // Verify that the second checkbox is unchecked
    expect(await checkboxes[1].isSelected()).to.be.false;

    // Wait for 5 seconds for manual verification
    await driver.sleep(5000); 
  });
});