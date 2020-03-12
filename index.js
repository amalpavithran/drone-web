const { app, BrowserWindow } = require('electron')
// let forward = document.getElementById('forward');
// let backward = document.getElementById('backward');
// let left = document.getElementById('left');
// let right = document.getElementById('right');
// let rotate = document.getElementById('rotate');

function createWindow () {
  // Create the browser window.
  let win = new BrowserWindow({
    width: 900,
    height: 800,
    webPreferences: {
      nodeIntegration: true
    }
  })

  // and load the index.html of the app.
  win.loadFile('index.html')
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})