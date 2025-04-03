// src/pages/loginPage.js

const { By, until } = require('selenium-webdriver');

class LoginPage {
  constructor(driver) {
    this.driver = driver;
    this.usernameInput = driver.findElement(By.id('username'));
    this.passwordInput = driver.findElement(By.id('password'));
    this.loginButton = driver.findElement(By.css('button[type="submit"]'));
    this.errorMessage = driver.findElement(By.id('flash'));
  }

  async enterUsername(username) {
    await this.usernameInput.sendKeys(username);
  }

  async enterPassword(password) {
    await this.passwordInput.sendKeys(password);
  }

  async clickLoginButton() {
    await this.loginButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.getText();
  }
}

module.exports = LoginPage;
