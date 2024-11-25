import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Misc.css';

export function Misc() {
  const [animals, setAnimals] = useState([]);
  const [selectedSpecies, setSelectedSpecies] = useState('');
  const [selectedAge, setSelectedAge] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchAnimals = async () => {
    console.log('Parâmetros enviados:', {
      animal_category: 'outros',
      animal_species: selectedSpecies || undefined,
      animal_age: selectedAge || undefined,
      animal_adopted:
        selectedAdopted !== ''
          ? selectedAdopted === 'adotado'
            ? true
            : false
          : undefined,
    });

    try {
      const response = await axios.get('http://127.0.0.1:5000/animals?animal_category=outro', {
        params: {
          animal_category: 'outros',
          animal_species: selectedSpecies || undefined,
          animal_age: selectedAge || undefined,
          animal_adopted:
            selectedAdopted !== ''
              ? selectedAdopted === 'adotado'
                ? true
                : false
              : undefined,
        },
      });
      setAnimals(response.data.animals);
    } catch (error) {
      console.error('Erro ao buscar animais:', error);
    }
  };

  useEffect(() => {
    fetchAnimals();
  }, [selectedSpecies, selectedAge, selectedAdopted]);

  const handleSpeciesChange = (e) => {
    const species = e.target.value;
    setSelectedSpecies(species);
  };

  const getNoAnimalsMessage = () => {
    if (!selectedSpecies && !selectedAge && !selectedAdopted) {
      return 'Nenhum animal encontrado';
    }
    let message = 'Nenhum ';
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
    <div className="miscPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="speciesFilter">Espécie</label>
          <select id="speciesFilter" onChange={handleSpeciesChange}>
            <option value="">Todas</option>
            <option value="iguana">Iguana</option>
            <option value="cobra">Cobra</option>
            <option value="tartaruga">Tartaruga</option>
            <option value="furão">Furão</option>
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
      <main className="filteredAnimals">
        {animals.length > 0 ? (
          animals.map((animal) => (
            <a key={animal.animal_name} href={`/outros/${animal.animal_name}`}>
              <div className="animalCard">
                <img src={animal.animal_image_url} alt={animal.animal_name} />
                <p>{animal.animal_name}</p>
              </div>
            </a>
          ))
        ) : (
          <p>{getNoAnimalsMessage()}</p>
        )}
      </main>
    </div>
  );
}
