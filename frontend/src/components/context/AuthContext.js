import React, { useEffect, useState } from 'react';

export const AuthContext = React.createContext();

const userInfoInitialState = {
  username: '',
  email: '',
  picture: '',
};

function AuthContextProvider({ children }) {
  let prevAuth = false;
  let jwtToken = null;
  let prevUserInfo = userInfoInitialState;

  // only execute on client side
  if (typeof window !== 'undefined') {
    prevAuth = JSON.parse(window.localStorage.getItem('authenticated')) || false;
    jwtToken = window.localStorage.getItem('token') || null;
    prevUserInfo = JSON.parse(window.localStorage.getItem('userInfo'));
  }

  const [authenticated, setAuthenticated] = useState(prevAuth || false);
  const [token, setToken] = useState(jwtToken || null);
  const [userInfo, setUserInfo] = useState(prevUserInfo || userInfoInitialState);

  useEffect(() => {
    window.localStorage.setItem('authenticated', authenticated);
    window.localStorage.setItem('token', token);
    window.localStorage.setItem('userInfo', JSON.stringify(userInfo));
  }, [authenticated, token, userInfo]);

  const defaultContext = {
    authenticated,
    setAuthenticated,
    token,
    setToken,
    userInfo,
    setUserInfo,
  };

  return <AuthContext.Provider value={defaultContext}>{children}</AuthContext.Provider>;
}

export default AuthContextProvider;
