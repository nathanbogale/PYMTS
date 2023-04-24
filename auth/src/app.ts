import express from "express";
import { json } from 'body-parser';
import routes from "./routes";
// import signUpRouter from "./routes/signup";
const { signUpRouter } = routes;

const app = express();

//
app.use(json());

app.use(signUpRouter)

export default app;