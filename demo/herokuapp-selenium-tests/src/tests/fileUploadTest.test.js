it('should upload a file successfully', async function() {
  // ... existing code ...

  await fileUploadPage.uploadFile(filePath);

  const successMessage = await driver.findElement({ id: 'uploaded-files' }).getText();
  assert.strictEqual(successMessage, 'File Uploaded!');
});