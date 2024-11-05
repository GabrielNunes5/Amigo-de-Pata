import { Link, useLocation } from 'react-router-dom';
import './Header.css';
import { useEffect, useState, useRef } from 'react';
import logo from '../assets/logo.png';
import logo1 from '../assets/logo1.png';

export const Header = ({ showSignUpBtn = true, onOpenLoginModal }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const dropDownRef = useRef(null);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropDownRef.current && !dropDownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  return (
    <header className="initPageHeader">
      <div className="menuDiv">
        <Link to={'/'}>
          <img src={location.pathname === '/' ? logo : logo1} alt="webSiteLogo" className="logo" />
        </Link>

        <Link to={'/'}>
          <button className="signInBtn">Home</button>
        </Link>
        <div className="dropdown-container" ref={dropDownRef}>
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
        <button className="signInBtn login" onClick={() => {
          console.log("Botão de Login clicado"); // Mensagem de depuração
          onOpenLoginModal();
        }}>
          Login
        </button>
        {showSignUpBtn && (
          <Link to={'/register'}>
            <button className="signInBtn">Cadastre-se</button>
          </Link>
        )}
      </div>
    </header>
  );
};

export default Header;
