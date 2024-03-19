import React, { useState } from "react";
import {
  Navbar,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Collapse,
  NavbarToggler,
  Form,
  Input,
  Dropdown,
  DropdownItem,
  DropdownToggle,
  DropdownMenu,
} from "reactstrap";
import SearchIcon from "@mui/icons-material/Search";
import "./CSS/navbar.css";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import { Link } from "react-router-dom";

const ResponsiveNavbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleNavbar = () => {
    setIsOpen(!isOpen);
  };
  const toggle = () => setDropdownOpen(!dropdownOpen);

  return (
    <Navbar light expand="md" className="navbar">
      <NavbarBrand className="logo" href="/">
        SHOP.CO
      </NavbarBrand>
      <NavbarToggler onClick={toggleNavbar} />
      <Collapse isOpen={isOpen} navbar>
        <Nav className="mr-auto  " navbar>
          <Dropdown nav isOpen={dropdownOpen} toggle={toggle}>
            <DropdownToggle nav caret>
              Shop
            </DropdownToggle>
            <DropdownMenu>
              <DropdownItem>Men</DropdownItem>
              <DropdownItem>Women</DropdownItem>
              <DropdownItem>Child</DropdownItem>
            </DropdownMenu>
          </Dropdown>
          <NavItem>
            <NavLink href="#">On Sale</NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="#">New Arrival</NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="#">Brands</NavLink>
          </NavItem>
        </Nav>
        <Form inline className="search-form mx-3">
          <div className="search-input">
            <Input type="text" placeholder="Search for Product" className=" " />
            <SearchIcon className="search-icon" />
          </div>
        </Form>
        <ShoppingCartIcon className="mx-2" />
        <Link to="/login" className="ml-md-2 mx-2">
          <AccountCircleIcon style={{ fontSize: "32px" }} />
        </Link>
      </Collapse>
    </Navbar>
  );
};

export default ResponsiveNavbar;
