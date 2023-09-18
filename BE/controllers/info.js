const express = require('express');
const info = express.Router();
const Info = require('../models/infoModel');
const isAuthenticated = require('../utils/isAuth');

info.get('/', isAuthenticated, async (req, res) => {
  try {
    // console.log('hi')
    if (req.user) {
      res.json(await Info.find({ uid: req.user.uid }));
    } else {
      res.json(await Info.find({ uid: null }));
    }
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Failed to get data' });
  }
});

info.post('/', isAuthenticated, async (req, res) => {
  try {
    req.body.uid = req.user.uid;
    const newInfo = await Info.create(req.body);
    res.json(newInfo);
  } catch (error) {
    console.log(error);
    res.status(400).json(error);
  }
});

info.put('/', async (req, res) => {
  try {
    const filter = { uid: req.body.uid }; // Filter based on uid
    const update = { $set: req.body }; // Update with the entire req.body content
    const options = { new: true };

    const updatedInfo = await Info.findOneAndUpdate(filter, update, options);
    res.json(updatedInfo);
  } catch (error) {
    res.status(400).json(error);
  }
});

info.delete('/:id', isAuthenticated, async (req, res) => {
  try {
    res.json(await Info.findByIdAndRemove(req.params.id));
  } catch (error) {
    res.status(400).json(error);
  }
});

info.get('/:id', async (req, res) => {
  try {
    const userUid = req.params.id; // Get the UID from the URL parameter
    const userInfo = await Info.findOne({ uid: userUid });

    if (userInfo) {
      res.json({ exists: true }); // Send true response if user data exists
    } else {
      res.json({}); // Send false response if user data doesn't exist
    }
  } catch (error) {
    console.log(error);
    res.status(400).json(error);
  }
});

module.exports = info;
