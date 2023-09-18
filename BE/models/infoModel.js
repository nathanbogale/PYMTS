const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const InfoSchema = new Schema(
  {
    Age: { type: String },
    NumberOfDependents: { type: String },
    MonthlyIncome: { type: String },
    MonthlyExpenses: { type: String },
    Accounts: { type: String },
    RevolvingUtilization: { type: String },
    RealEstateLoans: { type: String },
    ThirtyFiftyNinePastDue: { type: String },
    SixtyEightyNinePastDue: { type: String },
    NinetyDaysLate: { type: String },
    Score: { type: String },
    uid: String,
  },
  {
    timestamps: true,
  }
);

const Info = mongoose.model('Info', InfoSchema);

module.exports = Info;
