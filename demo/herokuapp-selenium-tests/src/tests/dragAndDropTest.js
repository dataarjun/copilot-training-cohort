// Write a selenium automation test for drag and drop feature on the-internet.herokuapp.com site.
// The drag and drop feature is located at http://the-internet.herokuapp.com/drag_and_drop.

const { Builder, By, Actions } = require('selenium-webdriver');
const { expect } = require('chai');

describe('Drag and Drop Test', function() {
    this.timeout(30000);
    let driver;

    beforeEach(async function() {
        driver = await new Builder().forBrowser('chrome').build();
        await driver.get('http://the-internet.herokuapp.com/drag_and_drop');
    });

    it('should drag and drop element', async function() {
        const source = await driver.findElement(By.id('column-a'));
        const target = await driver.findElement(By.id('column-b'));
        const actions = driver.actions({ async: true });
        await actions.dragAndDrop(source, target).perform();
        const sourceText = await source.getText();
        const targetText = await target.getText();
        expect(sourceText).to.equal('B');
        expect(targetText).to.equal('A');
        await driver.sleep(5000);
    });

    afterEach(async function() {
        await driver.quit();
    });
});