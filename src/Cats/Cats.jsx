import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Cats.css';

export default function Cats() {
  const [cats, setCats] = useState([]);
  const [selectedColor, setSelectedColor] = useState('');
  const [selectedAge, setSelectedAge] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchCats = async () => {
    console.log('Parâmetros enviados:', {
      animal_category: 'gato',
      animal_color: selectedColor || undefined,
      animal_age: selectedAge || undefined,
      animal_adopted:
        selectedAdopted !== ''
          ? selectedAdopted === 'adotado'
            ? true
            : false
          : undefined,
    });

    try {
      const response = await axios.get('http://127.0.0.1:5000/animals?animal_category=gato', {
        params: {
          animal_category: 'gato',
          animal_color: selectedColor || undefined,
          animal_age: selectedAge || undefined,
          animal_adopted:
            selectedAdopted !== ''
              ? selectedAdopted === 'adotado'
                ? true
                : false
              : undefined,
        },
      });
      setCats(response.data.animals); 
    } catch (error) {
      console.error('Erro ao buscar gatos:', error);
    }
  };

  useEffect(() => {
    fetchCats();
  }, [selectedColor, selectedAge, selectedAdopted]);

  const handleColorChange = (e) => {
    setSelectedColor(e.target.value);
  };

  const getNoCatsMessage = () => {
    if (!selectedColor && !selectedAge && !selectedAdopted) {
      return 'Nenhum gato encontrado';
    }
    let message = 'Nenhum gato ';
    if (selectedColor) {
      message += `${selectedColor}`;
    } else if (selectedAge) {
      message += `${selectedAge}`;
    } else if (selectedAdopted) {
      message += `${selectedAdopted === 'adotado' ? 'adotado' : 'não adotado'}`;
    }
    message += ' encontrado.';
    return message;
  };

  return (
    <div className="catsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="colorFilter">Cor</label>
          <select id="colorFilter" onChange={handleColorChange}>
            <option value="">Todas</option>
            <option value="preto">Preto</option>
            <option value="branco">Branco</option>
            <option value="laranja">Laranja</option>
            <option value="cinza">Cinza</option>
            <option value="tigrado">Tigrado</option>
          </select>
        </div>
        <div>
          <label htmlFor="ageFilter">Idade</label>
          <select
            id="ageFilter"
            onChange={(e) => setSelectedAge(e.target.value)}
          >
            <option value="">Todas</option>
            <option value="filhote">Filhote</option>
            <option value="adulto">Adulto</option>
            <option value="idoso">Idoso</option>
          </select>
        </div>
        <div>
          <label htmlFor="adoptedFilter">Status de Adoção</label>
          <select
            id="adoptedFilter"
            onChange={(e) => setSelectedAdopted(e.target.value)}
          >
            <option value="">Todos</option>
            <option value="adotado">Adotado</option>
            <option value="nao_adotado">Não Adotado</option>
          </select>
        </div>
      </aside>
      <main className="filteredCats">
        {cats.length > 0 ? (
          cats.map((cat) => (
            <a key={cat.animal_name} href={`/cats/${cat.animal_name}`}>
              <div className="catCard">
                <img src={cat.animal_image_url} alt={cat.animal_name} />
                <p>{cat.animal_name}</p>
              </div>
            </a>
          ))
        ) : (
          <p>{getNoCatsMessage()}</p>
        )}
      </main>
    </div>
  );
}
