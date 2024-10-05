import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from 'react-router-dom';
import '../Header/Header.css';
import SlickSliderComponent from '../Slider/Slider'; 
import './Home.css'
export default function Home() {
  const location = useLocation();

  const isSignUpPage = location.pathname === '/sign-up';

  return (
    <>
    
      <section className="mainSection1">
        <div className="imgDiv">
          <img
            src="https://semeupetfalasse.wordpress.com/wp-content/uploads/2020/10/cachorro-e-gatos-deitados-no-tapete.jpg"
            alt="imagem com um cão e dois gatos"
            className="backImg"
          />
        </div>
      </section>

      <section className="textSection">
        <img
          src="https://img.freepik.com/free-vector/paw-print-heart-red-colours_78370-7614.jpg?ga=GA1.1.1678703634.1718646592&semt=ais_hybrid"
          alt="imagem de um coração"
          className="heartImg"
        />
        <div className="textDiv">
          <h3 className="textTitle">Por que Adotar?</h3>
          <h4 className="textSubTitle">Adotar é um ato de amor!</h4>
          <p className="textP">Lorem ipsum dolor sit amet...</p>
        </div>
      </section>

      <section className="cardSection">
        <div className="cardDogDiv">
          <img
            src="https://img.freepik.com/premium-photo/adorable-fluffy-puppy-sitting-happily-wooden-floor-cozy-indoor-space_1294860-16745.jpg?ga=GA1.1.1678703634.1718646592&semt=ais_hybrid"
            alt="imagem de um cachorro"
          />
          <h4>Guia de adoção para Cães</h4>
          <p>Saiba como cuidar do seu cãozinho</p>
          <button className="cardBtn">Saiba mais...</button>
        </div>
        <div className="cardCatDiv">
          <img
            src="https://img.freepik.com/free-photo/view-beautiful-persian-domestic-cat_23-2151773932.jpg?ga=GA1.1.1678703634.1718646592&semt=ais_hybrid"
            alt="imagem de um gato"
          />
          <h4>Guia de adoção para Gatos</h4>
          <p>Saiba como cuidar do seu gatinho</p>
          <button className="cardBtn">Saiba mais...</button>
        </div>
      </section>
      
      <SlickSliderComponent />
    </>
  );
}
