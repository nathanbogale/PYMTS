const mongoose = require('mongoose');
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const admin = require('firebase-admin');
const { getAuth } = require('firebase-admin/auth');
require('dotenv').config();

const {
  PORT = 4000,
  MONGODB_URL,
  PRIVATE_KEY_ID,
  PRIVATE_KEY,
  CLIENT_ID,
} = process.env;

const app = express();

admin.initializeApp({
  credential: admin.credential.cert({
    type: 'service_account',
    project_id: 'financial-hackathon',
    private_key_id: PRIVATE_KEY_ID,
    private_key: PRIVATE_KEY.replace('\n', ''),
    client_email:
      'firebase-adminsdk-jh4h3@financial-hackathon.iam.gserviceaccount.com',
    client_id: CLIENT_ID,
    auth_uri: 'https://accounts.google.com/o/oauth2/auth',
    token_uri: 'https://oauth2.googleapis.com/token',
    auth_provider_x509_cert_url: 'https://www.googleapis.com/oauth2/v1/certs',
    client_x509_cert_url:
      'https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-jh4h3%40financial-hackathon.iam.gserviceaccount.com',
    universe_domain: 'googleapis.com',
  }),
});

// Database Connection //
const connectDB = async () => {
  try {
    const conn = await mongoose.connect(MONGODB_URL);
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.log(error);
    process.exit(1);
  }
};

// Establish Connect //
connectDB();

mongoose.connection
  .on('open', () => console.log('You are connected to mongoose'))
  .on('close', () => console.log('You are disconnected from mongoose'))
  .on('error', (error) => console.log(error));

mongoose.set('strictQuery', true);

// Middleware //
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// Auth Middleware //
app.use(async function (req, res, next) {
  try {
    const token = req.get('Authorization');
    // console.log(token);
    if (token) {
      const user = await getAuth().verifyIdToken(token.replace('Bearer ', ''));
      // console.log(user);
      req.user = user;
    } else {
      req.user = null;
    }
  } catch (error) {
    // perform additional tasks to follow up after and error
    req.user = null;
  }
  next(); // this function invokes the next middleware function
  //in the middleware stack/pipeline/conveyerbelt
});

// Controller //
const sampleController = require('./controllers/sample');
app.use('/test', sampleController);
const infoController = require('./controllers/info');
app.use('/info', infoController);

// Test Route //
app.get('/', (req, res) => {
  res.send('Hello World');
});

// Listener //
app.listen(PORT, () => console.log(`Listening on port ${PORT}`));
