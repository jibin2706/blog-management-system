import React, { useContext } from 'react';
import Link from 'next/link';
import clsx from 'clsx';
import { AuthContext } from '../context/AuthContext';
import css from './Navigation.module.css';

function Navigation() {
  const { authenticated, setAuthenticated, setToken } = useContext(AuthContext);

  const logout = () => {
    setAuthenticated(false);
    setToken(null);
  };

  return (
    <header className={clsx(css.header)}>
      <h1 className={clsx(css.title)}>Blogging</h1>
      <nav className={clsx(css.nav)}>
        <Link href="/">
          <a className={clsx(css.navLink)}>Home</a>
        </Link>
        <Link href="/contact">
          <a className={clsx(css.navLink)}>Contact</a>
        </Link>
        <Link href="/write">
          <a className={clsx(css.navLink)}>Write for us</a>
        </Link>
        {authenticated === true ? (
          <span className={clsx(css.navLink)} onClick={logout}>
            Logout
          </span>
        ) : (
          <Link href="/login">
            <a className={clsx(css.navLink)}>Login</a>
          </Link>
        )}
      </nav>
    </header>
  );
}

export default Navigation;
