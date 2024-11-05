import React, { useState, useEffect } from 'react';
import './Index.css';
import ReactInputMask from 'react-input-mask';

export const LoginModal = ({ isModalOpen, onCloseModal }) => {
  // Variáveis do login
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  // Variáveis do cadastro
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [activeTab, setActiveTab] = useState('login');

  // Validação de senha do usuário
  const validatePassword = (password) => {
    return /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$/.test(password);
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setSignupPassword(value);
    setPasswordError(
      !validatePassword(value) ? 'A senha deve ter no mínimo 7 caracteres, uma letra maiúscula, um número e um caractere especial.' : ''
    );
  };

  const handleConfirmPasswordChange = (e) => {
    const value = e.target.value;
    setConfirmPassword(value);
    setPasswordError(value !== signupPassword ? 'A confirmação da senha deve corresponder.' : '');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    // Fazer login
    if (!rememberMe) {
      setEmail('');
      setPassword('');
    }
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    if (passwordError) return;
    // Cadastrar usuário
    setActiveTab('login');
  };

  const handleOverlayClick = (e) => {
    if (e.target.classList.contains('modal-overlay')) {
      onCloseModal();
    }
  };

  // Lembrar usuário
  useEffect(() => {
    if (rememberMe && email && password) {
      localStorage.setItem('savedLogin', JSON.stringify({ email, password }));
    } else {
      localStorage.removeItem('savedLogin');
    }
  }, [rememberMe, email, password]);

  useEffect(() => {
    if (isModalOpen && rememberMe) {
      const savedLogin = JSON.parse(localStorage.getItem('savedLogin'));
      if (savedLogin) {
        setEmail(savedLogin.email);
        setPassword(savedLogin.password);
      }
    }
  }, [isModalOpen]);

  if (!isModalOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <div className="tabContainer">
          <button className={`tab ${activeTab === 'login' ? 'active' : ''}`} onClick={() => setActiveTab('login')}>
            Login
          </button>
          <button className={`tab ${activeTab === 'signup' ? 'active' : ''}`} onClick={() => setActiveTab('signup')}>
            Cadastre-se
          </button>
        </div>

        {activeTab === 'login' ? (
          <form onSubmit={handleLogin}>
            <h2>Login</h2>
            <div className="formGroup">
              <label>Email: </label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div className="formGroup">
              <label>Senha: </label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
            <div className="formGroup">
              <label>
                <input type="checkbox" checked={rememberMe} onChange={(e) => setRememberMe(e.target.checked)} />
                Lembrar-me
              </label>
            </div>
            <div className="bTnContainer">
              <button type="submit" className="confirmLogin">Entrar</button>
              <button type="button" className="closeBtn" onClick={() => { onCloseModal(); setEmail(''); setPassword(''); }}>
                Fechar
              </button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleSignUp}>
            <h2>Cadastre-se</h2>
            <div className="formGroup">
              <label>Nome: </label>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div className="formGroup">
              <label>Telefone: </label>
              <ReactInputMask mask="(99) 99999-9999" value={phone} onChange={(e) => setPhone(e.target.value)} required>
                {(inputProps) => <input {...inputProps} type="tel" />}
              </ReactInputMask>
            </div>
            <div className="formGroup">
              <label>Data de Nascimento: </label>
              <ReactInputMask mask="99/99/9999" value={birthDate} onChange={(e) => setBirthDate(e.target.value)} required>
                {(inputProps) => <input {...inputProps} type="text" />}
              </ReactInputMask>
            </div>
            <div className="formGroup">
              <label>Senha: </label>
              <input
                type="password"
                value={signupPassword}
                onChange={handlePasswordChange}
                required
              />
              {passwordError && <small className="error">{passwordError}</small>}
            </div>
            <div className="formGroup">
              <label>Confirme a Senha: </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                required
              />
              {confirmPassword !== signupPassword && confirmPassword && (
                <small className="error">A confirmação e a senha devem ser iguais.</small>
              )}
            </div>
            <div className="bTnContainer">
              <button type="submit" className="confirmLogin">Cadastrar</button>
              <button type="button" className="closeBtn" onClick={onCloseModal}>Fechar</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
