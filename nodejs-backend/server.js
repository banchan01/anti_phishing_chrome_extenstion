import express from 'express';
import dotenv from 'dotenv';
import { connectToDatabase, addPhishingLink } from './database.js';
import { loadModel, predictPhishing } from './modelPrediction.js';
import getPageRank from './pageRankController.js';
import getGoogleIndex from './googleIndexController.js';

dotenv.config();
const app = express();
app.use(express.json());
const port = process.env.PORT || 3000;

// Connect to database
connectToDatabase().catch(console.error);

// Load model when server starts
loadModel().catch(console.error);

// Log middleware
app.use((req, res, next) => {
    console.log(`Received ${req.method} request for ${req.url}`);
    next();
});

// New endpoint that handles all checks
app.post('/api/check-url', async (req, res) => {
    try {
        const { url } = req.body;
        if (!url) {
            return res.status(400).json({ error: 'URL is required' });
        }

        // Extract URL features
        const features = {
          length_url: Number(url.length),
          length_hostname: Number(url.split('/')[2]?.length || 0),
          ip: Number(url.includes('://') ? 1 : 0),
          nb_dots: Number(url.split('.').length - 1),
          nb_hyphens: Number(url.split('-').length - 1),
          nb_qm: Number(url.split('?').length - 1),
          nb_and: Number(url.split('&').length - 1),
          nb_eq: Number(url.split('=').length - 1),
          nb_underscore: Number(url.split('_').length - 1),
          nb_percent: Number(url.split('%').length - 1),
          nb_slash: Number(url.split('/').length - 1),
          nb_semicolumn: Number(url.split(';').length - 1),
          nb_www: Number(url.includes('www') ? 1 : 0),
          page_rank: 0,  // Initialize with default values
          google_index: 0 // Initialize with default values
        };

        // Get PageRank and Google Index concurrently
        const [pageRankResult, googleIndexResult] = await Promise.all([
            getPageRank(url),
            getGoogleIndex(url)
        ]);

        features.page_rank = pageRankResult.pageRank;
        features.google_index = googleIndexResult.isIndexed;

        // Make prediction using your model
        const prediction = await predictPhishing(features);
        
        // Return complete analysis
        res.json({
          url,
          features,
          is_phishing: prediction.label,
          prediction_score: prediction.probability
      });

    } catch (error) {
        console.error('Error checking URL:', error);
        res.status(500).json({ error: 'Failed to analyze URL' });
    }
});

app.post('/post-phishing-links', addPhishingLink);

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});