const express = require('express');
const { MongoClient } = require('mongodb');
require('dotenv').config();

const app = express();
app.use(express.json());

const port = process.env.PORT || 3000;
const uri = process.env.MONGODB_URI;

const client = new MongoClient(uri);

async function connectToDatabase() {
  try {
    await client.connect();
    console.log('Connected to MongoDB');
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
  }
}

connectToDatabase();

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

app.use((req, res, next) => {
    console.log(`Received ${req.method} request for ${req.url}`);
    next();
  });

app.post('/post-phishing-links', async (req, res) => {
    try {
      const { url } = req.body;
      if (!url) {
        return res.status(400).json({ error: 'URL is required' });
      }
  
      const database = client.db('phishing_db');
      const collection = database.collection('phishing_links');
  
      const result = await collection.insertOne({ url, timestamp: new Date() });
      res.status(201).json({ message: 'Phishing link added successfully', id: result.insertedId });
    } catch (error) {
      console.error('Error adding phishing link:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  app.post('/test', (req, res) => {
    res.json({ message: 'Test successful' });
  });

app.get('/get-phishing-links', async (req, res) => {
    console.log('hello')
});