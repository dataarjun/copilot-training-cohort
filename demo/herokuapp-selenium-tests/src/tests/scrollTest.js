// Write a selenium automation test to scroll to the bottom of the page on the-internet.herokuapp.com site.
// The page is located at http://the-internet.herokuapp.com/infinite_scroll.

const { Builder, By, Key } = require('selenium-webdriver');
const { expect } = require('chai');

describe('Scroll Test', function() {
    this.timeout(30000);
    let driver;

    beforeEach(async function() {
        driver = await new Builder().forBrowser('chrome').build();
        await driver.get('http://the-internet.herokuapp.com/infinite_scroll');
    });

    async function scrollToBottom(driver) {
        let lastHeight = await driver.executeScript('return document.body.scrollHeight');
        let scrollCount = 0;
        while (scrollCount < 3) {
            await driver.executeScript('window.scrollTo(0, document.body.scrollHeight)');
            await driver.sleep(2000); // Wait for scroll
            let newHeight = await driver.executeScript('return document.body.scrollHeight');
            if (newHeight === lastHeight) {
                break; // If the scroll position hasn't changed, exit the loop
            }
            lastHeight = newHeight;
            scrollCount++;
        }
    }

    it('should scroll to the bottom of the page', async function() {
        // Use the function to scroll
        await scrollToBottom(driver);

        // Now that we've scrolled, find elements with class 'jscroll-added'
        const elements = await driver.findElements(By.className('jscroll-added'));
        expect(elements.length).to.be.greaterThan(0); // Ensure elements are found
        await driver.sleep(5000); // Additional wait if needed
    });

    afterEach(async function() {
        await driver.quit();
    });
});