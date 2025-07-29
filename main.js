const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const remoteMain = require('@electron/remote/main');
remoteMain.initialize();
const fs = require('fs');
const path = require('path');
const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

let mainWindow;
let server;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    autoHideMenuBar: true,
    backgroundColor: '#f5f5f5',
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
      devTools: false
    },
    show: false
  });
  
  mainWindow.once('ready-to-show', () => {
    setTimeout(() => {
      mainWindow.show();
    }, 100);
  });

  mainWindow.loadFile('index.html');
  
  remoteMain.enable(mainWindow.webContents);
}

function startServer() {
  const expressApp = express();
  expressApp.use(cors());
  expressApp.use(express.json());

  // Handle CSV path for both development and production
  let currentCsvPath;
  if (app.isPackaged) {
    currentCsvPath = path.join(process.resourcesPath, 'International_Education_Costs_with_Calculations.csv');
  } else {
    currentCsvPath = path.join(__dirname, 'International_Education_Costs_with_Calculations.csv');
  }
  
  expressApp.post('/update-csv-path', (req, res) => {
    currentCsvPath = req.body.csvPath;
    res.json({ success: true });
  });
  
  expressApp.post('/predict', (req, res) => {
    // First retrain model with current CSV
    const trainData = { csvPath: currentCsvPath };
    const trainPython = spawn('python', [path.join(__dirname, 'train_model.py')], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    trainPython.stdin.write(JSON.stringify(trainData));
    trainPython.stdin.end();
    
    let trainResult = '';
    let trainError = '';
    
    trainPython.stdout.on('data', (data) => {
      trainResult += data.toString();
    });
    
    trainPython.stderr.on('data', (data) => {
      trainError += data.toString();
    });
    
    trainPython.on('close', (trainCode) => {
      if (trainCode !== 0) {
        res.status(500).json({ error: `Training error: ${trainError}` });
        return;
      }
      
      // Now make prediction
      const inputData = { ...req.body, csvPath: currentCsvPath };
      const python = spawn('python', [path.join(__dirname, 'predict.py')], {
        cwd: __dirname,
        stdio: ['pipe', 'pipe', 'pipe']
      });
      
      python.stdin.write(JSON.stringify(inputData));
      python.stdin.end();
      
      let result = '';
      let error = '';
      
      python.stdout.on('data', (data) => {
        result += data.toString();
      });
      
      python.stderr.on('data', (data) => {
        error += data.toString();
      });
      
      python.on('close', (code) => {
        if (code !== 0) {
          res.status(500).json({ error: `Python error: ${error}` });
          return;
        }
        try {
          res.json(JSON.parse(result));
        } catch (e) {
          res.status(500).json({ error: `Parse error: ${e.message}` });
        }
      });
    });
  });

  expressApp.get('/csv', (req, res) => {
    try {
      let csvPath = req.query.path;
      if (!csvPath || csvPath === 'undefined') {
        if (app.isPackaged) {
          csvPath = path.join(process.resourcesPath, 'International_Education_Costs_with_Calculations.csv');
        } else {
          csvPath = path.join(__dirname, 'International_Education_Costs_with_Calculations.csv');
        }
      }
      const csvData = fs.readFileSync(csvPath, 'utf8');
      res.json({ data: csvData, path: csvPath });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  expressApp.post('/csv', (req, res) => {
    try {
      const { data, path: csvPath } = req.body;
      fs.writeFileSync(csvPath, data);
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  expressApp.post('/visualize', (req, res) => {
    const inputData = { ...req.body, csvPath: req.body.csvPath || currentCsvPath };
    const python = spawn('python', [path.join(__dirname, 'visualize.py')], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    python.stdin.write(JSON.stringify(inputData));
    python.stdin.end();
    
    let result = '';
    let error = '';
    
    python.stdout.on('data', (data) => {
      result += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      error += data.toString();
    });
    
    python.on('close', (code) => {
      if (code !== 0) {
        res.status(500).json({ error: `Python error: ${error}` });
        return;
      }
      try {
        res.json(JSON.parse(result));
      } catch (e) {
        res.status(500).json({ error: `Parse error: ${e.message}` });
      }
    });
  });

  server = expressApp.listen(3000);
}

app.whenReady().then(() => {
  app.commandLine.appendSwitch('disable-gpu');
  startServer();
  createWindow();
});

app.on('ready', () => {
  ipcMain.handle('select-csv-file', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openFile'],
      filters: [{ name: 'CSV Files', extensions: ['csv'] }]
    });
    return result.filePaths[0];
  });
});

app.on('window-all-closed', () => {
  if (server) server.close();
  if (process.platform !== 'darwin') app.quit();
});