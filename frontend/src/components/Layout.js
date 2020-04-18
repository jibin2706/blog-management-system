import React from 'react';
import Navigation from './common/Navigation';
import Footer from './common/Footer';

function Layout({ children }) {
  return (
    <>
      <Navigation />
      {children}
      <Footer />
    </>
  );
}

export default Layout;
