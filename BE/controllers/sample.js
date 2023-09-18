const express = require('express');
const sampleRouter = express.Router();
const Samples = require('../models/samplesModel');
const isAuthenticated = require('../utils/isAuth');

// Seed Route

// const seed = require('../data/sampleSeed.js');
// sampleRouter.get('/seed', async (req, res) => {
//   try {
//     await Samples.deleteMany({});
//     const data = await Samples.create(seed);
//     res.redirect('/');
//   } catch (error) {
//     console.log(error);
//     res.status(500).json({ error: 'Faild to seed data' });
//   }
// });

// Index Route

sampleRouter.get('/', isAuthenticated, async (req, res) => {
  try {
    if (req.user) {
      res.json(await Samples.find({ uid: req.user.uid }));
    } else {
      res.json(await Samples.find({ uid: null }));
    }
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Faild to get data' });
  }
});

// Create Route

sampleRouter.post('/', isAuthenticated, async (req, res) => {
  try {
    // take authenticated user id and attach to request body
    // send the user id to the database when object is created
    req.body.uid = req.user.uid;
    // send all sample data
    const newSample = await Samples.create(req.body);
    res.json(newSample);
  } catch (error) {
    console.log(error);
    res.status(400).json(error);
  }
});

// Update Route

sampleRouter.put('/:id', isAuthenticated, async (req, res) => {
  try {
    const updatedSample = await Samples.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );
    res.json(updatedSample);
  } catch (error) {
    console.log(error);
    res.status(400).json(error);
  }
});

// Delete Route

sampleRouter.delete('/:id', isAuthenticated, async (req, res) => {
  try {
    const deletedSample = await Samples.findByIdAndRemove(req.params.id);
    res.json(deletedSample);
  } catch (error) {
    console.log(error);
    res.status(400).json(error);
  }
});

// Show Route

sampleRouter.get('/:id', isAuthenticated, async (req, res) => {
  try {
    const sample = await Samples.findById(req.params.id);
    res.json(sample);
  } catch (error) {
    console.log(error);
    res.status(400).json(error);
  }
});

module.exports = sampleRouter;
