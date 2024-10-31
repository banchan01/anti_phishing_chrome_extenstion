import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config();

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

async function connectToDatabase() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
        return client;
    } catch (error) {
        console.error('Error connecting to MongoDB:', error);
        throw error;
    }
}

async function addPhishingLink(req, res) {
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
}

export { connectToDatabase, addPhishingLink };