import request from 'supertest';
import app from '../../app';

/*
it('should return 405 to non-post request to the signup route', () =>{

});
*/

it('should return 422 if the email is not valid', async() =>{
  await await request(app)
  .post('/api/auth/signup')
  .send({something:"something"})
  .expect(422);

  await await request(app)
  .post('/api/auth/signup')
  .send({email: 'Invalid Email'})
  .expect(422);

  /*
  await await request(app)
  .post('/api/auth/signup')
  .send({email: '@test.com'}) //uses the body validator, and the isEmail on the signup page 
  .expect(422);
  */

});

