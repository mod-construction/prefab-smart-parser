import React, { Component } from 'react';
import { Container } from 'reactstrap';
import { NavMenu } from './NavMenu';

export class Layout extends Component {
  static displayName = Layout.name;

  render() {
    return (
      <div>
        <NavMenu />
        <div tag="main" className={"p-0 m-5"}>
          {this.props.children}
        </div>
      </div>
    );
  }
}
