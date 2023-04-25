import request from 'supertest';
import app from '../../app';
import { SIGNUP_ROUTE } from '../signup';

/**
* valud email condition:
    - standard email formats from 'express-valudator' package: considered valid if the validator says so
**/
describe('test validity of email input', () => {
  let password = '';

  //executed before other get executed
  beforeAll(() => {
    password = 'Validpassword1';
  });

  it('should return 422 if the email is not provided', async () => {
    await request(app).post(SIGNUP_ROUTE).send({ password }).expect(422);
  });
  it('should return 422 if the email is not valid', async () => {
    await request(app).post(SIGNUP_ROUTE).send({ password }).expect(422);

    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email: 'test@test.com' })
      .expect(422);
  });

  it('should return 200 if the password is not provided', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email: 'test@test.com', password })
      .expect(200);
  });
});

/**
* valud password condition:
    - atleast 8 chars
    - atmost 32 cahrs
    - atleast one small one large cap
    - atleast one number 
**/

describe('test validity of password input', () => {
  let email = '';

  beforeAll(() => {
    email = 'test@test.com';
  });

  it('should return 422 if the password is not provided', async () => {
    await request(app).post(SIGNUP_ROUTE).send({ email }).expect(422);
  });
  it('should return 422 if the password contains less than 8 characters', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email, password: 'Valid12' })
      .expect(422);
  });
  it('should return 422 if the password contains more than 32 characters', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({
        email,
        password: 'Valid12Valid12Valid12Valid12Valid12Valid12Valid12',
      })
      .expect(422);
  });
  it('should return 422 if the password does not contain one lowercase', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email, password: 'VALID12VALID12' })
      .expect(422);
  });
  it('should return 422 if the password does not contain one uppercase', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email, password: 'valid12valid12' })
      .expect(422);
  });
  it('should return 422 if the password does not contain a number', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email, password: 'Validvalid' })
      .expect(422);
  });
  it('should return 200 if the password is valid', async () => {
    const normalizedEmail = 'test@test.com';
    const response = await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email, password: 'Validavali12' })
      .expect(200);

    expect(response.body.email).toEqual(normalizedEmail);
  });
});

describe('test sanitization of email input', () => {
  it('should contain uppercase letters in the email', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({ email: 'test@TEST.COM', password: 'Valid123' })
      .expect(200); //valid but unsanitized email
  });
});

describe('test sanitization of password input', () => {
  it('should not contain unscapped characters', async () => {
    await request(app)
      .post(SIGNUP_ROUTE)
      .send({
        email: 'test@test.com',
        password: 'Valid123', //if added something like < it will fail
      })
      .expect(200);
  });
});
