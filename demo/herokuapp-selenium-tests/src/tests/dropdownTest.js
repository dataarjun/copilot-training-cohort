const { Builder } = require('selenium-webdriver');
const assert = require('assert');
const DropdownPage = require('../pages/dropdownPage');

describe('Dropdown Test', function() {
  this.timeout(30000); // Extend timeout for asynchronous operations
  let driver;
  let dropdownPage;

  before(async function() {
    this.timeout(10000); // Extend timeout for this hook to 10 seconds
    driver = await new Builder().forBrowser('chrome').build();
    dropdownPage = new DropdownPage(driver);
  });

  after(async function() {
    await driver.quit();
  });

  it('should select option 1 from the dropdown', async function() {
    await dropdownPage.navigateToDropdownPage();
    await dropdownPage.selectOptionByValue('1');
    await driver.sleep(5000); // Static wait for manual verification
    const selectedOption = await dropdownPage.getSelectedOption();
    assert.strictEqual(selectedOption, 'Option 1');
  });

  it('should select option 2 from the dropdown', async function() {
    await dropdownPage.navigateToDropdownPage();
    await dropdownPage.selectOptionByValue('2');
    await driver.sleep(5000); // Static wait for manual verification
    const selectedOption = await dropdownPage.getSelectedOption();
    assert.strictEqual(selectedOption, 'Option 2');
  });
});
