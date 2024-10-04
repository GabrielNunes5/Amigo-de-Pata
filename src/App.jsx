import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import './App.css';
import Header from './Header/Header';
import Home from './Home/Home'; 
import Register from './Register/Register'; 
import Cats from './Cats/Cats';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function App() {
  const location = useLocation();

  const isRegisterPage = location.pathname === '/register';

  return (
    <>
      <Header showSignUpBtn={!isRegisterPage} /> 
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/cats" element={<Cats />} />
      </Routes>
    </>
  );
}

export default App;
