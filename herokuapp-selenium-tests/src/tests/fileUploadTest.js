const { Builder, By } = require('selenium-webdriver');
const { expect } = require('chai');
const assert = require('assert');
const path = require('path');

describe('File Upload Test', function() {
  this.timeout(30000);
  let driver;

  before(async function() {
    driver = await new Builder().forBrowser('chrome').build();
    await driver.get('http://the-internet.herokuapp.com/upload');
  });

  it('should upload a file and verify the upload success', async function() {
    // Assuming there's a file named 'example.txt' in the project directory
    const filePath = __dirname + '/example.txt';
    const fileInput = await driver.findElement(By.id('file-upload'));
    const uploadButton = await driver.findElement(By.id('file-submit'));

    await fileInput.sendKeys(filePath);
    await uploadButton.click();
    driver.sleep(15000); // Static wait for manual verification

    // Wait for the file to be uploaded and the success message to appear
    await driver.wait(() => driver.findElement(By.id('uploaded-files')).getText().then(text => text.includes('example.txt')), 10000);
    const uploadedFileName = await driver.findElement(By.id('uploaded-files')).getText();
    assert.strictEqual(uploadedFileName, 'example.txt', 'The uploaded file name should match the expected value.');
  });

  after(async function() {
    await driver.quit();
  });
});