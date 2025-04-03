const {Builder, By, Key, until} = require('selenium-webdriver');   
const {expect} = require('chai');

describe('Frames Test', function() { 
    this.timeout(50000);
    let driver;

    before(async function() {
        driver = await new Builder().forBrowser('chrome').build();
    });

    it('Test 1: Switch to frame', async function() {
        await driver.get('https://the-internet.herokuapp.com/frames');
        await driver.findElement(By.linkText('iFrame')).click();
        await driver.switchTo().frame(await driver.findElement(By.id('mce_0_ifr')));
        let text = await driver.findElement(By.id('tinymce')).getText();
        expect(text).to.equal('Your content goes here.');
        await driver.switchTo().defaultContent();
    });

    // Write a test for nested frames 
   it('Test 2: Nested Frames', async function() {
        await driver.get('https://the-internet.herokuapp.com/nested_frames');
        await driver.switchTo().frame(await driver.findElement(By.name('frame-top')));
        await driver.switchTo().frame(await driver.findElement(By.name('frame-middle')));
        let text = await driver.findElement(By.id('content')).getText();
        expect(text).to.equal('MIDDLE');
        await driver.switchTo().defaultContent();
    });

    after(() => driver.quit());
});