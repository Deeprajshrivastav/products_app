import React from "react";
import ResponsiveNavbar from "./Navbar";

function Layout({ children }) {
  return (
    <div style={{ display: "flex" }}>
     
      <div style={{ display: "flex", flexDirection: "column", flex: 1 }}>
        <ResponsiveNavbar />
        <main style={{ flex: 1, padding: "20px" }}>{children}</main>
      </div>
    </div>
  );
}

export default Layout;