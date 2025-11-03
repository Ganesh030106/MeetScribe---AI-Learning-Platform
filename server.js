import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Helper for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 3000;

// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Helper function to read a file
function getFileContent(fileName) {
  try {
    return fs.readFileSync(path.join(__dirname, fileName), 'utf-8');
  } catch (err) {
    console.error(`Error reading ${fileName}:`, err.message);
    return `// Could not load ${fileName}`;
  }
}

// Main route to render the page
app.get('/', (req, res) => {

  // 1. Define the data for your files
  const fileData = [
    {
      fileName: 'start.js',
      title: 'Basic Text Generation',
      description: 'A simple script to send a single text prompt to the Gemini API and print the response.',
      code: getFileContent('start.js')
    },
    {
      fileName: 'chat.js',
      title: 'Interactive Terminal Chat',
      description: 'Uses `readline` to create a persistent, back-and-forth chat conversation in your terminal.',
      code: getFileContent('chat.js')
    },
    {
      fileName: 'gemini-pro-vision.js',
      title: 'Image Analysis (Vision)',
      description: 'Demonstrates how to send a local image file along with a text prompt for multimodal analysis.',
      code: getFileContent('gemini-pro-vision.js')
    }
  ];

  // 2. Render the EJS template and pass the data
  res.render('index', { files: fileData });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});