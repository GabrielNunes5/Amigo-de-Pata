import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Cats.css';

export default function Cats() {
  const [cats, setCats] = useState([]);
  const [selectedColor, setSelectedColor] = useState('');
  const [selectedAge, setSelectedAge] = useState('');

  const fetchCats = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/cats');
      setCats(response.data.cats); 
    } catch (error) {
      console.error('Erro ao buscar gatos:', error);
    }
  };

  useEffect(() => {
    fetchCats();
  }, []);

  const filteredCats = cats.filter((cat) => {
    const colorMatch = selectedColor
      ? cat.cat_color.toLowerCase().includes(selectedColor.toLowerCase())
      : true;

    const ageMatch = selectedAge ? cat.cat_age === selectedAge : true;

    return colorMatch && ageMatch;
  });

  return (
    <div className="catsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="colorFilter">Cor</label>
          <select
            id="colorFilter"
            onChange={(e) => setSelectedColor(e.target.value)}
          >
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
      </aside>
      <main className="filteredCats">
        {filteredCats.length > 0 ? (
          filteredCats.map((cat) => (
            <a key={cat.cat_name} href={`/cats/${cat.cat_name}`}>
              <div>
                <img src={cat.cat_image_url} alt={cat.cat_name} />
                <p>{cat.cat_name}</p>
              </div>
            </a>
          ))
        ) : (
          <p>Nenhum gato encontrado.</p>
        )}
      </main>
    </div>
  );
}
