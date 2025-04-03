// Write a test case to take a screenshot of the-internet.herokuapp.com home page 
const {Builder, By, Key, until} = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');

describe('Screenshot Test', function() {
    this.timeout(50000);
    let driver;

    before(async function() {
        driver = await new Builder().forBrowser('chrome').build();
    });

    it('Test 1: Take a screenshot', async function() {
        await driver.get('https://the-internet.herokuapp.com/');
        let screenshot = await driver.takeScreenshot();
        fs.writeFileSync(path.join(__dirname, 'screenshot.png'), screenshot, 'base64');
    });

    after(() => driver.quit());
});