import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Misc.css';

export const Misc = () => {
  const [animals, setAnimals] = useState([]);
  const [selectedSpecies, setSelectedSpecies] = useState('');
  const [selectedAgeRange, setSelectedAgeRange] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchAnimals = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/outros/filter', {
        params: {
          animal_species: selectedSpecies || undefined,
          animal_age_range: selectedAgeRange || undefined,
          animal_adopted:
            selectedAdopted !== ''
              ? selectedAdopted === 'adotado'
                ? true
                : false
              : undefined,
        },
      });

      if (response.data.animals.length > 0) {
        setAnimals(response.data.animals);
      } else {
        setAnimals([]);
      }
    } catch (error) {
      console.error('Erro ao buscar animais:', error);
      setAnimals([]);
    }
  };

  useEffect(() => {
    fetchAnimals();
  }, [selectedSpecies, selectedAgeRange, selectedAdopted]);

  return (
    <div className="outrosPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="speciesFilter">Espécie</label>
          <select
            id="speciesFilter"
            onChange={(e) => setSelectedSpecies(e.target.value)}
          >
            <option value="">Todas</option>
            <option value="iguana">Iguana</option>
            <option value="cobra">Cobra</option>
            <option value="tartaruga">Tartaruga</option>
            <option value="ferret">Furão</option>
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

      <main className="filteredAnimals">
        {animals.length > 0 ? (
          animals.map((animal) => (
            <a key={animal.animal_name} href={`/outros/${animal.animal_name}`}>
              <div>
                <img src={animal.animal_image_url} alt={animal.animal_name} />
                <p>{animal.animal_name}</p>
              </div>
            </a>
          ))
        ) : (
          <p>Nenhum animal encontrado.</p>
        )}
      </main>
    </div>
  );
};
