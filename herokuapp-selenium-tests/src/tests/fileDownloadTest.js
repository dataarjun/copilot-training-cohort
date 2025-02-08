// Write a selenium automation test to download a file from the internet-app.herokuapp.com site.
// The name of the file is 'some-file.txt'. The file is located at http://the-internet.herokuapp.com/download/some-file.txt.
// The file should be downloaded into /src/tests/downloads directory.

const { Builder, By } = require('selenium-webdriver');
const { expect } = require('chai');
const fs = require('fs');
const path = require('path');
const chrome = require('selenium-webdriver/chrome');

describe('File Download Test', function() {
    this.timeout(30000);
    let driver;

    beforeEach(async function() {
        const chromeOptions = new chrome.Options();
        chromeOptions.setUserPreferences({
            'download.default_directory': path.resolve(__dirname, 'downloads')
        });

        driver = await new Builder().forBrowser('chrome').setChromeOptions(chromeOptions).build();
        await driver.get('http://the-internet.herokuapp.com/download/some-file.txt');
    });

    it('should download a file', async function() {
        const filePath = path.resolve(__dirname, 'downloads', 'some-file.txt');
        await driver.sleep(5000); // Wait for the download to potentially complete
        await waitForFile(filePath); // Wait for the file to exist
        const fileExists = fs.existsSync(filePath);
        expect(fileExists).to.be.true;
    });

    afterEach(async function() {
        await driver.quit();
    });

    // Custom wait function for file existence
async function waitForFile(filePath, timeout = 30000) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        const interval = setInterval(() => {
            if (fs.existsSync(filePath)) {
                clearInterval(interval);
                resolve(true);
            } else if (Date.now() - startTime > timeout) {
                clearInterval(interval);
                reject(new Error('File did not exist within timeout period'));
            }
        }, 500); // Check every 500ms
    });
}
}); 