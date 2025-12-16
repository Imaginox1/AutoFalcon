// main.js
const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path');
const { Builder, By, until } = require('selenium-webdriver');
const edge = require('selenium-webdriver/edge');

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  const win = new BrowserWindow({
    width: 600,
    height: 480,
    minWidth: 400,
    minHeight: 300,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    backgroundColor: '#f8f3ed',
    show: false,
    autoHideMenuBar: true,
    icon: path.join(__dirname, 'falcon.icns') // <-- proper multi-size .ico
  });

  win.loadFile('index.html');

  win.once('ready-to-show', () => {
    win.show();
  });

  // Handle per-monitor DPI changes
  screen.on('display-metrics-changed', () => {
    win.webContents.send('display-metrics-changed');
  });

  win.on('move', () => {
    win.webContents.send('window-moved');
  });

  return win;
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// Selenium login handler
ipcMain.handle('perform-login', async (event, { emailLocalPart, password }) => {
  const email = `${emailLocalPart}@fbcs.school`;

  let driver;
  try {
    // Point directly to msedgedriver in app folder
    const arch = process.arch; // 'arm64' for Apple Silicon, 'x64' for Intel
    const driverName = arch === 'arm64' ? 'msedgedriver-arm64' : 'msedgedriver-x64';
    const driverPath = path.join(process.resourcesPath, driverName);
    const service = new edge.ServiceBuilder(driverPath);

    driver = await new Builder()
      .forBrowser('MicrosoftEdge')
      .setEdgeService(service)
      .build();

    await driver.get('https://faithkids.myschoolapp.com/app/?fromHash=login#login');
    await driver.manage().window().maximize();

    await driver.wait(until.elementLocated(By.id('Username')), 10000);
    await driver.findElement(By.id('Username')).sendKeys(email);
    await driver.findElement(By.id('nextBtn')).click();

    await driver.wait(until.elementLocated(By.css('button.sky-btn.sky-btn-primary.sky-btn-block.spa-auth-btn-primary')), 10000);
    await driver.findElement(By.css('button.sky-btn.sky-btn-primary.sky-btn-block.spa-auth-btn-primary')).click();

    await driver.wait(until.elementLocated(By.id('identifierId')), 10000);
    await driver.findElement(By.id('identifierId')).sendKeys(email);
    await driver.findElement(By.id('identifierNext')).click();

    await driver.wait(until.elementLocated(By.name('Passwd')), 10000);
    await driver.findElement(By.name('Passwd')).sendKeys(password);
    await driver.findElement(By.id('passwordNext')).click();

    setTimeout(async () => {
      try { await driver.quit(); } catch (e) {}
    }, 600000000);

    return { success: true, message: 'Login Successful!' };
  } catch (err) {
    try { if (driver) await driver.quit(); } catch (e) {}
    return { success: false, message: 'Login Failed. Please check your email and password.' };
  }
});