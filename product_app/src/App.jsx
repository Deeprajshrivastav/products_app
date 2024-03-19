import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import LoginPage from "./components/Login";
import Layout from "./components/Layout";
import Splash from "./components/Splash";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
         
        <Routes>
        <Route
            path="/"
            element={
              <Layout>
                <Splash/>
              </Layout>
            }
          />
        <Route
            path="/login"
            element={
              <Layout>
                <LoginPage /> 
              </Layout>
            }
          />
           
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
