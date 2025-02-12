const { By } = require('selenium-webdriver');

class DropdownPage {
  constructor(driver) {
    this.driver = driver;
    this.url = 'https://the-internet.herokuapp.com/dropdown';
    this.dropdown = By.id('dropdown');
  }

  async navigateToDropdownPage() {
    await this.driver.get(this.url);
  }

  async selectOptionByValue(value) {
    const dropdownElement = await this.driver.findElement(this.dropdown);
    await dropdownElement.click();
    await this.driver.sleep(5000); // Static wait for manual verification
    await dropdownElement.findElement(By.css(`option[value="${value}"]`)).click();
    await this.driver.sleep(5000); // Static wait for manual verification
  }

  async selectOptionByText(text) {
    const dropdownElement = await this.driver.findElement(this.dropdown);
    await dropdownElement.click();
    await this.driver.sleep(5000); // Static wait for manual verification
    await dropdownElement.findElement(By.xpath(`//option[text()="${text}"]`)).click();
    await this.driver.sleep(5000); // Static wait for manual verification
  }

  async getSelectedOption() {
    const dropdownElement = await this.driver.findElement(this.dropdown);
    const selectedOptionElement = await dropdownElement.findElement(By.css('option:checked'));
    return await selectedOptionElement.getText();
  }
}

module.exports = DropdownPage;
