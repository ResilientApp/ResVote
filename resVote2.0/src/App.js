import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Login from './components/Login';
import TransactionForm from './components/TransactionForm';
import Loader from './components/Loader';
import ElectionsView from './components/elections';

function App() { // This is the heart of our application (or control center)
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);
  const [isLoadingAfterLogin, setIsLoadingAfterLogin] = useState(false);

  useEffect(() => {
    const storedToken = sessionStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (authToken) => {
    setIsLoadingAfterLogin(true);
    setToken(authToken);
    sessionStorage.setItem('token', authToken);

    setTimeout(() => {
      setIsAuthenticated(true);
      setIsLoadingAfterLogin(false);
    }, 2000);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken(null);
    sessionStorage.removeItem('token');
  };

  return (
    <div className="App">
      {/* Comment below line and uncomment the block to get actual correct code flow */}
      <ElectionsView onLogout={handleLogout} token="123" /> 
      {/* {isLoadingAfterLogin && <Loader />}
      {!isLoadingAfterLogin && isAuthenticated ? ( // If the user has logged in and is authenticated we take them to the Elections View
        <ElectionsView onLogout={handleLogout} token={token}></ElectionsView> // Give a logout handler and an identifier token (pub key?)
        // <TransactionForm onLogout={handleLogout} token={token} />
      ) : (
        <Login onLogin={handleLogin} /> // If they haven't actually logged in yet just show the default login screen apartim made
      )} */}
    </div>
  );
}

export default App;