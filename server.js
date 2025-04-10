const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  // Serve files from current working directory
  const baseDir = process.cwd();
  let filePath = path.join(baseDir, req.url.replace(/^\//, ''));
  if (req.url === '/' || req.url === '') filePath = path.join(baseDir, 'index.html');
  
  // Security check - prevent directory traversal
  if (!filePath.startsWith(baseDir)) {
    res.writeHead(403);
    return res.end('Forbidden');
  }

  const extname = path.extname(filePath);
  let contentType = 'text/html';
  switch (extname) {
    case '.js':
      contentType = 'text/javascript';
      break;
    case '.css':
      contentType = 'text/css';
      break;
    case '.json':
      contentType = 'application/json';
      break;
    case '.png':
      contentType = 'image/png';
      break;
    case '.jpg':
      contentType = 'image/jpg';
      break;
    case '.csv':
      contentType = 'text/csv';
      res.setHeader('Access-Control-Allow-Origin', '*');
      break;
  }

  console.log(`Request for: ${filePath}`);
  fs.readFile(filePath, (err, content) => {
    if (err) {
      console.error(`Error serving ${filePath}:`, err);
      if (err.code == 'ENOENT') {
        res.writeHead(404);
        res.end(`File not found: ${filePath}`);
      } else {
        res.writeHead(500);
        res.end(`Server error: ${err.message}`);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(8000, () => {
  console.log('Server running at http://localhost:8000/');
});
