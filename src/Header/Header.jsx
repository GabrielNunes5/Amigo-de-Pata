import { Link, useLocation } from 'react-router-dom';
import './Header.css';
import { useEffect, useState } from 'react';
import logo from '../assets/logo.png';
import logo1 from '../assets/logo1.png'

export const Header = ({ showSignUpBtn = true }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    if (isOpen) {
      setIsOpen(false);
    }
  }, [location]);

  return (
    <header className="initPageHeader">
      <div className="menuDiv">
        <Link to={'/'}>
        <img src={location.pathname === '/' ? logo : logo1} alt="webSiteLogo" className="logo" />
        </Link>

        <Link to={'/'}>
          <button className="signInBtn">Home</button>
        </Link>
        <div className="dropdown-container">
          <button onClick={toggleDropdown} className="signInBtn">
            Nossos Pets
          </button>

          {isOpen && (
            <div className="dropdown-content">
              <div className="dropdown-row">
                <Link to={'/Dogs'}>
                  <div className="dropdown-option">
                    <img
                      src="https://img.icons8.com/ios-filled/50/000000/dog.png"
                      alt="dog icon"
                    />
                    <span>Cachorríneos</span>
                  </div>
                </Link>
                <Link to={'/cats'}>
                  <div className="dropdown-option">
                    <img
                      src="https://img.icons8.com/ios-filled/50/000000/cat.png"
                      alt="cat icon"
                    />
                    <span>Gatíneos</span>
                  </div>
                </Link>
              </div>

              <div className="dropdown-row">
                <Link to={'/birds'}>
                  <div className="dropdown-option">
                    <img
                      src="https://img.icons8.com/ios-filled/50/000000/bird.png"
                      alt="bird icon"
                    />
                    <span>Passaríneos</span>
                  </div>
                </Link>
                <Link to={'/others'}>
                  <div className="dropdown-option">
                    <img
                      src="https://img.icons8.com/ios-filled/50/000000/lizard.png"
                      alt="lizard icon"
                    />
                    <span>Outros bichíneos</span>
                  </div>
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="login">
        <Link to={'/login'}>
          <button className="signInBtn login">Login</button>
        </Link>
        <Link to={'/register'}>
          <button className="signInBtn">Cadastre-se</button>
        </Link>
      </div>
    </header>
  );
};

export default Header;
