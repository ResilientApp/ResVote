import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import About from './pages/About';
import Layout from './pages/Navbar';
import Home from './pages/Home';
import NoPage from './pages/NoPage';
import Login from './pages/Login';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import TransactionForm from './provided_components/TransactionForm';
import Loader from './provided_components/Loader';
import Signup from './pages/Signup';

// function App() {
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [token, setToken] = useState(null);
//   const [isLoadingAfterLogin, setIsLoadingAfterLogin] = useState(false);

//   useEffect(() => {
//     const storedToken = sessionStorage.getItem('token');
//     if (storedToken) {
//       setToken(storedToken);
//       setIsAuthenticated(true);
//     }
//   }, []);

//   const handleLogin = (authToken) => {
//     setIsLoadingAfterLogin(true);
//     setToken(authToken);
//     sessionStorage.setItem('token', authToken);

//     setTimeout(() => {
//       setIsAuthenticated(true);
//       setIsLoadingAfterLogin(false);
//     }, 2000);
//   };

//   const handleLogout = () => {
//     setIsAuthenticated(false);
//     setToken(null);
//     sessionStorage.removeItem('token');
//   };

//   return (
//     <div className="App">
//       {isLoadingAfterLogin && <Loader />}
//       {!isLoadingAfterLogin && isAuthenticated ? (
//         <TransactionForm onLogout={handleLogout} token={token} />
//       ) : (
//         <Login onLogin={handleLogin} />
//       )}
//     </div>
//   );
// }

// export default App;

export default function App(){
  const [user, setUser] = useState(null);
  return(
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>

            <Route index element={<Home />} />

            <Route path="about" element={<About />} />

            <Route path="login" element={<Login />} />

            <Route path="signup" element={<Signup />} />

            <Route path="*" element={<NoPage />} />

          </Route>
        </Routes>
      </BrowserRouter>
  )
}