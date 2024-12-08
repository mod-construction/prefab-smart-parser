import React, {Component} from 'react';
import {Collapse, Navbar, NavbarBrand, NavbarToggler, NavItem, NavLink} from 'reactstrap';
import {Link} from 'react-router-dom';
import './NavMenu.css';

export class NavMenu extends Component {
    static displayName = NavMenu.name;

    constructor(props) {
        super(props);

        this.toggleNavbar = this.toggleNavbar.bind(this);
        this.state = {
            collapsed: true
        };
    }

    toggleNavbar() {
        this.setState({
            collapsed: !this.state.collapsed
        });
    }

    render() {
        return (
            <header>
                <Navbar className="navbar-expand-sm navbar-toggleable-sm mx-auto ng-white border-bottom box-shadow mb-3"
                        container light>
                    <NavbarBrand tag={Link} to="/dashboard" className={"w-100"}>
                        <img
                            width={200}
                            height={60}
                            src={`${process.env.PUBLIC_URL}/logo10.png`}
                            alt="Logo"
                            className={" align-content-center logo"}
                        /></NavbarBrand>
                    <NavbarToggler onClick={this.toggleNavbar} className="mr-2" />
                    {/*<Collapse className="d-sm-inline-flex flex-sm-row-reverse" isOpen={!this.state.collapsed} navbar>*/}
                    {/*    <ul className="navbar-nav flex-grow">*/}
                    {/*        /!* Navbar items *!/*/}
                    {/*    </ul>*/}
                    {/*</Collapse>*/}
                </Navbar>
            </header>
        );
    }
}
