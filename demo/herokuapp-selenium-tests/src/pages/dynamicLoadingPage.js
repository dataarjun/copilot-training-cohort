const { By, until } = require('selenium-webdriver');

class DynamicLoadingPage {
  constructor(driver) {
    this.driver = driver;
    this.url = 'https://the-internet.herokuapp.com/dynamic_loading';
    this.example1Link = By.css('a[href="/dynamic_loading/1"]');
    this.example2Link = By.css('a[href="/dynamic_loading/2"]');
    this.startButton = By.css('#start button');
    this.loadingSpinner = By.id('loading');
    this.loadedElement = By.id('finish');
  }

  async navigate() {
    await this.driver.get(this.url);
    await this.driver.wait(until.urlIs(this.url), 10000); // Wait until the URL is correct
  }

  async clickExample1Link() {
    const element = await this.driver.wait(until.elementLocated(this.example1Link), 10000);
    await element.click();
  }

  async clickExample2Link() {
    const element = await this.driver.wait(until.elementLocated(this.example2Link), 30000);
    await element.click();
  }

  async clickStartButton() {
    const element = await this.driver.wait(until.elementLocated(this.startButton), 10000);
    await element.click();
  }

  async waitForSpinnerToDisappear() {
    const spinner = await this.driver.findElement(this.loadingSpinner);
    await this.driver.wait(until.elementIsNotVisible(spinner), 10000);
  }

  async getLoadedElementText() {
    const element = await this.driver.wait(until.elementLocated(this.loadedElement), 10000);
    return await element.getText();
  }
}

module.exports = DynamicLoadingPage;
