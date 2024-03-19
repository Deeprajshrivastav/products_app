import React from "react";
import { Col, Button } from "reactstrap";
import "./CSS/splash.css";
const Splash = () => {
  return (
    <>
      <Col>
        <div className="p-text mx-5 mt-4">
          <span>FIND CLOTHES</span>
          <br />
          <span>THAT MATCHES</span>
          <br />
          <span>YOUR STYLES</span>
        </div>
        <div className="mx-5 mt-2 subtext">
          <span>
            Browse through our diverse range of meticulously crafted garments,
            designed <br />
            to bring out your individuality and cater to your sense of style.
          </span>
        </div>
      </Col>

      <Col className="d-flex mt-3 mx-5 justify-content-left">
        <Button type="submit" className="shopnow">
          Shop Now
        </Button>
      </Col>
    </>
  );
};

export default Splash;
