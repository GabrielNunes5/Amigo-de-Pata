import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function Details() {
  const { animalId } = useParams();
  const [animalDetails, setAnimalDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnimalDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/animals/name/${animalId}`);
        if (!response.ok) {
          throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        const data = await response.json();
        setAnimalDetails(data.animal); // Adaptar conforme o retorno do backend
      } catch (error) {
        console.error('Error fetching animal details:', error);
        setError('Erro ao buscar detalhes do animal. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };

    if (animalId) {
      fetchAnimalDetails();
    }
  }, [animalId]);

  if (loading) {
    return <p>Carregando...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!animalDetails) {
    return <p>Animal não encontrado.</p>;
  }

  return (
    <div className="animal-details">
      <h2>Detalhes de {animalDetails.name || 'Animal'}</h2>
      {animalDetails.image_url ? (
        <img
          src={animalDetails.image_url}
          alt={`Imagem de ${animalDetails.name || 'Animal'}`}
        />
      ) : (
        <p>Imagem não disponível.</p>
      )}

      <div className="details-info">
        <p><strong>Idade:</strong> {animalDetails.age || 'Desconhecida'}</p>
        <p><strong>Cor:</strong> {animalDetails.color || 'Desconhecida'}</p>
        <p><strong>Adotado:</strong> {animalDetails.adopted ? 'Sim' : 'Não'}</p>
        <p><strong>Sexo:</strong> {animalDetails.sex || 'Não especificado'}</p>
        <p><strong>Vacinas:</strong> {animalDetails.vaccines || 'Não especificado'}</p>
        <p><strong>Necessidades especiais:</strong> {animalDetails.special_conditions ? 'Sim' : 'Não'}</p>
        <p><strong>Castrado:</strong> {animalDetails.neutered ? 'Sim' : 'Não'}</p>
      </div>
    </div>
  );
}

export default Details;
