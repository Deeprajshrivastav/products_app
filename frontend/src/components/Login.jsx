import React, { useState } from "react";
import {
  Row,
  Col,
  Card,
  CardBody,
  CardTitle,
  Form,
  FormGroup,
  Label,
  Input,
  Button,
} from "reactstrap";
import "./CSS/login.css";
const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submitLogin = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify(
        `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
      ),
    };

    const response = await fetch("http://localhost:8000/login", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("Invalid Password");
    } else {
      console.log("Password: ", data.access_token);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitLogin();
  };

  return (
    <div className="container mt-4">
      <Card className="formcard  d-flex justify-content-center mt-4">
        <CardBody>
          <CardTitle tag="h5" className="text-center">
            Login
          </CardTitle>
          <Form onSubmit={handleSubmit}>
            <FormGroup className="mt-4">
              <Label for="email">Email Address</Label>
              <Input
                type="text"
                id="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </FormGroup>
            <FormGroup className="mt-4">
              <Label for="password">Password</Label>
              <Input
                type="password"
                id="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </FormGroup>
            <FormGroup row>
              <Col className="d-flex mt-3 justify-content-center">
                <Button type="submit" className=" w-50 submit">
                  Sign In
                </Button>
              </Col>
            </FormGroup> 
          </Form>
        </CardBody>
      </Card>
    </div>
  );
};

export default Login;
