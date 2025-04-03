const { Builder, By, until, logging } = require('selenium-webdriver');
const { expect } = require('chai');

describe('JavaScript Error Validation Test', function() {
    this.timeout(30000);  
  let driver;

  beforeEach(async function() {
    driver = await new Builder().forBrowser('chrome').build();
    await driver.manage().logs().get(logging.Type.BROWSER);
    await driver.get('http://the-internet.herokuapp.com/javascript_error');
  });

  it('should not have any JavaScript errors', async function() {
    const logs = await driver.manage().logs().get(logging.Type.BROWSER);
    const jsErrors = logs.filter(log => log.level === logging.Level.SEVERE);
    expect(jsErrors.length).to.be.greaterThan(0);
  });

  afterEach(async function() {
    await driver.quit();
  });
});