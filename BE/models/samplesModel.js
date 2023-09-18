const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const SamplesSchema = new Schema(
  {
    name: { type: String, required: true },
    creditScore: { type: Number, required: true },
    monthlyIncome: { type: Number, required: true },
    monthlyBills: { type: Number, required: true },
    uid: String,
  },
  {
    timestamps: true,
  }
);

const Samples = mongoose.model('Samples', SamplesSchema);

module.exports = Samples;
