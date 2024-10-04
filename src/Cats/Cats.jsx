import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Cats.css';

export default function Cats() {
  const [breeds, setBreeds] = useState([]);
  const [cats, setCats] = useState([]);
  const [selectedBreed, setSelectedBreed] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const [selectedAge, setSelectedAge] = useState('');

  const fetchCats = async (breedId = '') => {
    try {
      const response = await axios.get(
        'https://api.thecatapi.com/v1/images/search',
        {
          params: {
            limit: 50,
            size: 'med',
            breed_ids: breedId,
          },
        },
      );
      setCats(response.data);
    } catch (error) {
      console.error('Erro ao buscar gatos:', error);
    }
  };

  useEffect(() => {
    const fetchBreeds = async () => {
      try {
        const response = await axios.get('https://api.thecatapi.com/v1/breeds');
        setBreeds(response.data);
      } catch (error) {
        console.error('Erro ao buscar raças: ', error);
      }
    };

    fetchBreeds();
    fetchCats();
  }, []);

  //useEffect mudando os bichano a depender da raça filtrada =p
  useEffect(() => {
    fetchCats(selectedBreed);
  }, [selectedBreed]);

  const detectColor = (catUrl) => {
    if (catUrl.includes('black')) return 'black';
    if (catUrl.includes('white')) return 'white';
    if (catUrl.includes('orange')) return 'orange';
    if (catUrl.includes('brown')) return 'brown';
    return '';
  };

  const filteredCats = cats.filter((cat) => {
    const colorMatch = selectedColor
      ? detectColor(cat.url) === selectedColor
      : true;

    const ageMatch = selectedAge ? cat.age === selectedAge : true;

    return colorMatch && ageMatch;
  });

  return (
    <div className="catsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="breedFilter">Raça</label>
          <select
            id="breedFilter"
            onChange={(e) => setSelectedBreed(e.target.value)}
          >
            <option value="">Todas</option>
            {breeds.map((breed) => (
              <option key={breed.id} value={breed.id}>
                {breed.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="colorFilter">Cor</label>
          <select
            id="colorFilter"
            onChange={(e) => setSelectedColor(e.target.value)}
          >
            <option value="">Todas</option>
            <option value="black">Preto</option>
            <option value="white">Branco</option>
            <option value="orange">Laranja</option>
            <option value="brown">Marrom</option>
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
            <a key={cat.id} href={`/cats/${cat.id}`}>
              <div>
                <img src={cat.url} alt="Gato" />
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
