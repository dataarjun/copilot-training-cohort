// implement dra driven test to validate the login functionality of the-internet.herokuapp.com/login
const {Builder, By, Key, until} = require('selenium-webdriver');
const {expect} = require('chai');
const fs = require('fs');

describe ('Data Driven Test', function() {
    this.timeout(50000);
    let driver;

    before(async function() {
        driver = await new Builder().forBrowser('chrome').build();
    });

    it('Test 1: Data Driven Test', async function() {
        await driver.get('https://the-internet.herokuapp.com/login');
        let data = JSON.parse(fs.readFileSync('src/tests/credentials.json'));
        for (let i = 0; i < data.length; i++) {
            await driver.findElement(By.id('username')).sendKeys(data[i].username);
            await driver.findElement(By.id('password')).sendKeys(data[i].password);
            await driver.findElement(By.css('button[type="submit"]')).click();
            let result = await driver.findElement(By.id('flash')).getText();
            expect(result).to.include(data[i].result);
            await driver.get('https://the-internet.herokuapp.com/login');
        }
    });

    after(() => driver.quit());
});