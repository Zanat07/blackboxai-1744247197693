# Project Setup Guide

## Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)

## Installation
1. Clone this repository
2. Navigate to the project directory:
   ```bash
   cd /project/sandbox/user-workspace
   ```
3. Install dependencies (if any):
   ```bash
   npm install
   ```

## Running the Application
1. Start the server:
   ```bash
   node server.js
   ```
2. The server will start on port 8000
3. Open your web browser and visit:
   ```
   http://localhost:8000
   ```

## Project Structure
- `server.js` - Main Node.js server file
- `index.html` - Frontend entry point
- `data.json` - Sample data file
- Other CSV files contain additional data

## Troubleshooting
- If you get `EADDRINUSE` error (port 8000 in use):
  ```bash
  lsof -i :8000
  kill [PID]
  ```
- Make sure all required files are present in the directory

## Features
- Serves static files (HTML, CSS, JS)
- Handles JSON and CSV data
- Basic security against directory traversal
