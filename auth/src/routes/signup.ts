import express, { Request, Response } from 'express';
import { body, validationResult } from 'express-validator';

const signUpRouter = express.Router();

signUpRouter.post(
  '/api/auth/signup',
  [body('email').isEmail().withMessage('Email must be ina valid format')],
  [body('password').isLength({ min : 8, max : 32}).withMessage('Password must be between 8 and 32 characters')],
  [body('password').matches( /^(.*[a-z].*)$/).withMessage('Password must contain atleast one lowwer case letter')],
  [body('password').matches( /^(.*[A-Z].*)$/).withMessage('Password must contain atleast one upper case letter')],
  [body('password').matches( /^(.*\d.*)$/).withMessage('Password must contain atleast one number case letter')],
  (req: Request, res: Response) => {
    const errors = validationResult(req); // validates if the email has erros

    if (!errors.isEmpty()) {
      res.status(422).send({ errors: errors.array() });
    }

    res.send({});
  }
);

export default signUpRouter;
