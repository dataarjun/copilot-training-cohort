// Write a selenium automation test to validate the data in a table on the-internet.herokuapp.com site.
// The table is located at http://the-internet.herokuapp.com/tables.
// Create two test cases one validating the presence of a specific text in a table and 
// Another test case to ensure that the table is not empty.

const { Builder, By } = require('selenium-webdriver'); 
const { expect } = require('chai');

describe('Table Data Validation Test', function() {
    this.timeout(30000);
    let driver;

    beforeEach(async function() {
        driver = await new Builder().forBrowser('chrome').build();
        await driver.get('http://the-internet.herokuapp.com/tables');
    });

    it('should validate the presence of a specific text in a table', async function() {
        const table = await driver.findElement(By.id('table1'));
        const rows = await table.findElements(By.css('tbody tr'));
        for (let row of rows) {
            const cells = await row.findElements(By.css('td'));
            const lastName = await cells[0].getText();
            expect(lastName).to.be.oneOf(['Smith', 'Bach', 'Doe', 'Conway' ]);
        }
    });

    it('should validate that the table is not empty', async function() {
        const table = await driver.findElement(By.id('table1'));
        const rows = await table.findElements(By.css('tbody tr'));
        expect(rows.length).to.be.greaterThan(0);
    });
});