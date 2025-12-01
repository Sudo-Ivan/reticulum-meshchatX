#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');
const os = require('os');

const platform = os.platform();
const venvPython = platform === 'win32' 
  ? path.join('venv', 'Scripts', 'python.exe')
  : path.join('venv', 'bin', 'python');

try {
  execSync(`${venvPython} setup.py build`, { stdio: 'inherit' });
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}

