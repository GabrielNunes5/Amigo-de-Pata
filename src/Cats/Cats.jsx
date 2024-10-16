import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Cats.css';

export default function Cats() {
  const [cats, setCats] = useState([]);
  const [selectedColor, setSelectedColor] = useState(''); 
  const [selectedAge, setSelectedAge] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchCats = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/cats/filter', {
        params: {
          cat_color: selectedColor || undefined,
          cat_age: selectedAge || undefined,
          cat_adopted: selectedAdopted !== '' 
          ? selectedAdopted === 'adotado' 
            ? true 
            : false 
          : undefined,
        },
      });
      setCats(response.data.cats);
    } catch (error) {
      console.error('Erro ao buscar gatos:', error);
    }
  };
  

  useEffect(() => {
    fetchCats();
  }, [selectedColor, selectedAge, selectedAdopted]); 

  const handleColorChange = (e) => {
    const color = e.target.value;
    setSelectedColor(color);
  };

  return (
    <div className="catsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="colorFilter">Cor</label>
          <select
            id="colorFilter"
            onChange={handleColorChange}
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
