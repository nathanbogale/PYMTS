import request from 'supertest';
import app from '../app';

it('Reponds with a satatus of 200', () => {
  request(app)
  .get('/')
  .expect(200)
});
