import express, {Request,Response} from 'express';
import { body, validationResult } from 'express-validator';

const signUpRouter = express.Router();

signUpRouter.post('/api/auth/signup', [
  body('email').isEmail().withMessage('Email must be ina valid format')
], (req: Request, res: Response) => {
  const errors = validationResult(req);  //validates if the email has erros 

  if(!errors.isEmpty()){
    res.status(422).send({});
  }
  
  res.send({});

});

export default signUpRouter;
