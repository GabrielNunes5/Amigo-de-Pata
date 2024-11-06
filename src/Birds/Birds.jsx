import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Birds.css';

export const Birds = () => {
  const [birds, setBirds] = useState([]);
  const [selectedSpecies, setSelectedSpecies] = useState('');
  const [selectedAgeRange, setSelectedAgeRange] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchBirds = async () => {
    setBirds([]);
    try {
      const response = await axios.get('http://127.0.0.1:5000/birds/filter', {
        params: {
          bird_specie: selectedSpecies || undefined,
          bird_age: selectedAgeRange || undefined, 
          bird_adopted: selectedAdopted === 'adotado' ? true : selectedAdopted === 'nao_adotado' ? false : undefined,
        },
      });
      setBirds(response.data.birds);
    } catch (error) {
      console.error('Erro ao buscar pássaros:', error);
    }
  };

  useEffect(() => {
    fetchBirds();
  }, [selectedSpecies, selectedAgeRange, selectedAdopted]);

  const handleSpeciesChange = (e) => {
    setSelectedSpecies(e.target.value);
  };

  const getNoBirdsMessage = () => {
    if (!selectedSpecies && !selectedAgeRange && selectedAdopted === '') {
      return 'Nenhum pássaro encontrado';
    }
    let message = 'Nenhum ';
    if (selectedSpecies) message += selectedSpecies;
    if (selectedAgeRange) message += ` ${selectedAgeRange}`;
    if (selectedAdopted) message += ` ${selectedAdopted === 'adotado' ? 'adotado' : 'não adotado'}`;
    return `${message} encontrado.`;
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
          <label htmlFor="ageRangeFilter">Faixa Etária</label>
          <select
            id="ageRangeFilter"
            onChange={(e) => setSelectedAgeRange(e.target.value)}
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
            <a key={bird.bird_specie} href={`/birds/${bird.bird_specie}`}>
              <div>
                <img src={bird.bird_image_url} alt={bird.bird_specie} />
                <p>{bird.bird_specie}</p>
              </div>
            </a>
          ))
        ) : (
          <p>{getNoBirdsMessage()}</p>
        )}
      </main>
    </div>
  );
};
