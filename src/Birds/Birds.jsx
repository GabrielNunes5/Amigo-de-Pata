import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Birds.css';

export function Birds() {
  const [birds, setBirds] = useState([]);
  const [selectedSpecies, setSelectedSpecies] = useState('');
  const [selectedAge, setSelectedAge] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchBirds = async () => {
    console.log('Parâmetros enviados:', {
      animal_category: 'pássaro',
      bird_species: selectedSpecies || undefined,
      bird_age: selectedAge || undefined,
      bird_adopted:
        selectedAdopted !== ''
          ? selectedAdopted === 'adotado'
            ? true
            : false
          : undefined,
    });

    try {
      const response = await axios.get('http://127.0.0.1:5000/animals?animal_category=passaro', {
        params: {
          animal_category: 'pássaro',
          bird_species: selectedSpecies || undefined,
          bird_age: selectedAge || undefined,
          bird_adopted:
            selectedAdopted !== ''
              ? selectedAdopted === 'adotado'
                ? true
                : false
              : undefined,
        },
      });
      setBirds(response.data.animals);
    } catch (error) {
      console.error('Erro ao buscar pássaros:', error);
    }
  };

  useEffect(() => {
    fetchBirds();
  }, [selectedSpecies, selectedAge, selectedAdopted]);

  const handleSpeciesChange = (e) => {
    const species = e.target.value;
    setSelectedSpecies(species);
  };

  const getNoBirdsMessage = () => {
    if (!selectedSpecies && !selectedAge && !selectedAdopted) {
      return 'Nenhum pássaro encontrado';
    }
    let message = 'Nenhum pássaro ';
    if (selectedSpecies) {
      message += `${selectedSpecies}`;
    } else if (selectedAge) {
      message += `${selectedAge}`;
    } else if (selectedAdopted) {
      message += `${selectedAdopted === 'adotado' ? 'adotado' : 'não adotado'}`;
    }
    message += ' encontrado.';
    return message;
  };

  return (
    <div className="birdsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="speciesFilter">Espécie</label>
          <select id="speciesFilter" onChange={handleSpeciesChange}>
            <option value="">Todas</option>
            <option value="canario">Canário</option>
            <option value="papagaio">Papagaio</option>
            <option value="periquito">Periquito</option>
            <option value="calopsita">Calopsita</option>
          </select>
        </div>
        <div>
          <label htmlFor="ageFilter">Idade</label>
          <select
            id="ageFilter"
            onChange={(e) => setSelectedAge(e.target.value)}
          >
            <option value="">Todas</option>
            <option value="jovem">Jovem</option>
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
      <main className="filteredBirds">
        {birds.length > 0 ? (
          birds.map((bird) => (
            <a key={bird.animal_name} href={`/birds/${bird.animal_name}`}>
              <div className="birdCard">
                <img src={bird.animal_image_url} alt={bird.animal_name} />
                <p>{bird.animal_name}</p>
              </div>
            </a>
          ))
        ) : (
          <p>{getNoBirdsMessage()}</p>
        )}
      </main>
    </div>
  );
}
