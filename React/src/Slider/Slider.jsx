import React from 'react';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import './Slider.css';

export default function SlickSliderComponent() {
  const settings = {
    dots: true,
    infinite: false,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: false,
    arrows: true, 
  };

  return (
    <div className='slider-container'>
      <div style={{ width: "100%", margin: "auto", position: 'relative' }}>
        <Slider {...settings}>
          <div>
            <img src="https://cczcampos.com.br/wp-content/uploads/2021/10/Adocao-Materia.jpg" alt="cachorrinho para adoção" />
          </div>
          <div>
            <img src="https://blog-static.petlove.com.br/wp-content/uploads/2021/08/gato-filhote-gaiola-petlove.jpg" alt="gatinho para adoção" />
          </div>
          <div>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqbVZ0Msbqv5sslIDBCd8cFRBJ6wD3E8jklg&s" alt="ferret para adoção" />
          </div>
        </Slider>
      </div>
    </div>
  );
}
