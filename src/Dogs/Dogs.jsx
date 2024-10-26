import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dogs.css';

export default function Dogs() {
  const [dogs, setDogs] = useState([]);
  const [breedOptions, setBreedOptions] = useState([]);
  const [selectedBreed, setSelectedBreed] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const [selectedAge, setSelectedAge] = useState('');

  const API_KEY = 'live_VfUt9O4MJIJhjEbVaoRQ0Zr1HbJVnrdeaFBEnkmy7zsmnWgIYd0RBHCelDmZv7KZ';

  // Função para buscar as raças com base no nome digitado
  const fetchBreedOptions = async (breedName) => {
    try {
      const breedListUrl = `https://api.thedogapi.com/v1/breeds/search?q=${breedName}`;
      const breedResponse = await axios.get(breedListUrl, {
        headers: {
          'x-api-key': API_KEY,
        },
      });

      setBreedOptions(breedResponse.data);
    } catch (error) {
      console.error('Erro ao buscar raças:', error);
    }
  };

  // Função para buscar os cães com base no breed_id
  const fetchDogs = async (breedId) => {
    try {
      const url = `https://api.thedogapi.com/v1/images/search`;

      const response = await axios.get(url, {
        headers: {
          'x-api-key': API_KEY,
        },
        params: {
          breed_id: breedId || undefined,
          limit: 10,
        },
      });

      setDogs(response.data);
    } catch (error) {
      console.error('Erro ao buscar cães:', error);
    }
  };

  // UseEffect para buscar os cães sempre que a raça for selecionada
  useEffect(() => {
    if (selectedBreed) {
      fetchDogs(selectedBreed);
    } else {
      fetchDogs(); // Buscar cães sem filtro se não houver raça selecionada
    }
  }, [selectedBreed]);

  // Atualiza as opções de raças conforme o usuário digita
  const handleBreedChange = (e) => {
    const breedName = e.target.value;
    if (breedName) {
      fetchBreedOptions(breedName);
    } else {
      setBreedOptions([]);
    }
  };

  // Atualiza a raça selecionada com base no ID da raça
  const handleBreedSelect = (breedId) => {
    setSelectedBreed(breedId);
    setBreedOptions([]); // Limpa as sugestões após a seleção
  };

  return (
    <div className="dogsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="breedFilter">Raça</label>
          <input
            type="text"
            id="breedFilter"
            onChange={handleBreedChange}
            placeholder="Digite a raça"
          />
          {breedOptions.length > 0 && (
            <ul className="breedOptions">
              {breedOptions.map((breed) => (
                <li key={breed.id} onClick={() => handleBreedSelect(breed.id)}>
                  {breed.name}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Filtros de cor e idade (opcionais) */}
        <div>
          <label htmlFor="colorFilter">Cor</label>
          <select id="colorFilter" onChange={(e) => setSelectedColor(e.target.value)}>
            <option value="">Todas</option>
            <option value="preto">Preto</option>
            <option value="branco">Branco</option>
            <option value="marrom">Marrom</option>
            <option value="cinza">Cinza</option>
          </select>
        </div>

        <div>
          <label htmlFor="ageFilter">Idade</label>
          <select id="ageFilter" onChange={(e) => setSelectedAge(e.target.value)}>
            <option value="">Todas</option>
            <option value="filhote">Filhote</option>
            <option value="adulto">Adulto</option>
            <option value="idoso">Idoso</option>
          </select>
        </div>
      </aside>

      <main className="filteredDogs">
        {dogs.length > 0 ? (
          dogs.map((dog) => (
            <a key={dog.id} href={`/dogs/${dog.id}`}>
              <div className="dogCard">
                <img src={dog.url || 'https://via.placeholder.com/150'} alt={dog.breeds[0]?.name || 'Cão'} />
                <p>{dog.breeds[0]?.name || 'Raça desconhecida'}</p>
              </div>
            </a>
          ))
        ) : (
          <p>Nenhum cão encontrado.</p>
        )}
      </main>
    </div>
  );
}
