// implement dra driven test to validate the login functionality of the-internet.herokuapp.com/login
const {Builder, By, Key, until} = require('selenium-webdriver');
const {expect} = require('chai');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

describe ('Data Driven Test with CSV', function() {
    this.timeout(50000);
    let driver;
    let data = [];
    async function readCsv(filePath) {
        return new Promise((resolve, reject) => {
            let data = [];
            fs.createReadStream(filePath)
                .pipe(csv())
                .on('data', (row) => {
                    data.push(row);
                })
                .on('end', () => {
                    resolve(data);
                });
    }); 
}

    before(async function() {
        const filePath = path.join(__dirname, 'credentials.csv');
        data = await readCsv(filePath);
        driver = await new Builder().forBrowser('chrome').build();
    });

    it('Test 1: Data Driven Test', async function() {
        await driver.get('https://the-internet.herokuapp.com/login');
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