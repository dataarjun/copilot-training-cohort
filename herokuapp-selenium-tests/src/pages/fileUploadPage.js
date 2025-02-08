const { By, Key } = require('selenium-webdriver');

class FileUploadPage {
  constructor(driver) {
    this.driver = driver;
    this.fileInput = By.id('file-upload');
    this.uploadButton = By.id('file-submit');
    this.uploadedFiles = By.id('uploaded-files');
  }

  async uploadFile(filePath) {
    await this.driver.findElement(this.fileInput).sendKeys(filePath);
    await this.driver.findElement(this.uploadButton).click();
    await this.driver.sleep(5000); // Static wait for manual verification
  }

  async getUploadedFileName() {
    return await this.driver.findElement(this.uploadedFiles).getText();
  }
}

module.exports = FileUploadPage;