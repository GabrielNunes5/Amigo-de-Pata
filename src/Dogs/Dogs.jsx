import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dogs.css';

export default function Dogs() {
  const [dogs, setDogs] = useState([]);
  const [selectedColor, setSelectedColor] = useState('');
  const [selectedAge, setSelectedAge] = useState('');
  const [selectedAdopted, setSelectedAdopted] = useState('');

  const fetchDogs = async () => {
    setDogs([])
    try {
      const response = await axios.get('http://127.0.0.1:5000/dogs/filter', {
        params: {
          dog_color: selectedColor || undefined,
          dog_age: selectedAge || undefined,
          dog_adopted:
            selectedAdopted !== ''
              ? selectedAdopted === 'adotado'
                ? true
                : false
              : undefined,
        },
      });
      setDogs(response.data.dogs);
    } catch (error) {
      console.error('Erro ao buscar cachorros:', error);
    }
  };

  useEffect(() => {
    fetchDogs();
  }, [selectedColor, selectedAge, selectedAdopted]);

  const handleColorChange = (e) => {
    const color = e.target.value;
    setSelectedColor(color);
  };

  const getNoDogsMessage = ()=>{
    if(!selectedColor && !selectedAge && !selectedAdopted){
      return 'Nenhum cachorro encontrado'
    }
    let message = 'Nenhum cachorro '
    if(selectedColor){
      message += `${selectedColor}`
    }else if(selectedAge){
      message += `${selectedAge}`
    }else if(selectedAdopted){
      message += `${selectedAdopted ==='adotado' ? 'adotado' : 'não adotado'}`
    }
    message += ' encontrado.'
    return message
  }

  return (
    <div className="dogsPage">
      <aside className="filterAside">
        <div>
          <label htmlFor="colorFilter">Cor</label>
          <select id="colorFilter" onChange={handleColorChange}>
            <option value="">Todas</option>
            <option value="preto">Preto</option>
            <option value="branco">Branco</option>
            <option value="caramelo">Caramelo</option>
            <option value="colorido">Multi cores</option>
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

      <main className="filteredDogs">
        {dogs.length > 0 ? (
          dogs.map((dog) => (
            <a key={dog.dog_name} href={`/dogs/${dog.dog_name}`}>
              <div className="dogCard">
                <img src={dog.dog_image_url} alt={dog.dog_name} />
                <p>{dog.dog_name}</p>
              </div>
            </a>
          ))
        ) : (
          <p>{getNoDogsMessage()}</p>
        )}
      </main>
    </div>
  );
}
