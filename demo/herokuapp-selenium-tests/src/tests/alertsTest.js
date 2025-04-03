// Write a test cases for alert, confirm and prompt alerts using the-internet.herokuapp.com/javascript_alerts
const {Builder, By, Key, until} = require('selenium-webdriver');
const {expect} = require('chai');
describe('Alerts Test', function() {
    this.timeout(50000);
    let driver;
    before(async function() {
        driver = await new Builder().forBrowser('chrome').build();
    });
    it('Test 1: Alert', async function() {
        await driver.get('https://the-internet.herokuapp.com/javascript_alerts');
        await driver.findElement(By.css('button[onclick="jsAlert()"]')).click();
        await driver.switchTo().alert().accept();
        let result = await driver.findElement(By.id('result')).getText();
        expect(result).to.equal('You successfully clicked an alert');
    });
    it('Test 2: Confirm', async function() {
        await driver.get('https://the-internet.herokuapp.com/javascript_alerts');
        await driver.findElement(By.xpath("//button[text()='Click for JS Confirm']")).click();
        await driver.switchTo().alert().dismiss();
        let result = await driver.findElement(By.id('result')).getText();
        expect(result).to.equal('You clicked: Cancel');
    });
    it('Test 3: Prompt', async function() {
        await driver.get('https://the-internet.herokuapp.com/javascript_alerts');
        await driver.findElement(By.xpath("//button[text()='Click for JS Prompt']")).click();
        await driver.switchTo().alert().sendKeys('Hello, World!');
        await driver.switchTo().alert().accept();
        let result = await driver.findElement(By.id('result')).getText();
        expect(result).to.equal('You entered: Hello, World!');
    });
    after(() => driver.quit());
});