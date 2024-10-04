import React, { useState } from "react";
import './Register.css';
import Header from '../Header/Header'

export default function Register() {
  const [formData, setFormData] = useState({
    nomeCompleto: '',
    idade: '',
    email: '',
    telefone: '',
    endereco: '',
    tipoDeResidencia: '',
    jardim: false,
    outrosPets: '',
    tipoDePet: '',
    estiloDoPet: '',
    trabalho: '',
    horasTrabalhadas: '',
    mediaSalarial: '',
    motivoDaAdocao: '',
    compromissoDeCuidar: '',
    outrasExperiencias: '',
    infoAdicional: ''
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form Data:', formData);
    // pegar link API/Banco de dados com o gaybriel
  };

  return (
    <>
      <section className="formSection">
        <form onSubmit={handleSubmit} className="formularioAdocao">
          <h2>Cadastro/Formulário de Adoção</h2>

          <label>
            Nome completo:
            <input
              type="text"
              name="nomeCompleto"
              value={formData.nomeCompleto}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Idade:
            <input
              type="number"
              name="idade"
              value={formData.idade}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            E-mail:
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Telefone:
            <input
              type="tel"
              name="telefone"
              value={formData.telefone}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Endereço:
            <input
              type="text"
              name="endereco"
              value={formData.endereco}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Tipo de Residência:
            <select name="tipoDeResidencia" value={formData.tipoDeResidencia} onChange={handleChange} required>
              <option value="">Selecione...</option>
              <option value="casa">Casa</option>
              <option value="apartamento">Apartamento</option>
              <option value="outros">Outro</option>
            </select>
          </label>
          <label>
            Tem quintal?
            <input
              type="checkbox"
              name="jardim"
              checked={formData.jardim}
              onChange={handleChange}
            />
          </label>

          <label>
            Outros Animais:
            <input
              type="text"
              name="outrosPets"
              value={formData.outrosPets}
              onChange={handleChange}
            />
          </label>
          <label>
            Tipo de Pet Desejado:
            <select name="tipoDePet" value={formData.tipoDePet} onChange={handleChange} required>
              <option value="">Selecione...</option>
              <option value="cachorro">Cachorro</option>
              <option value="gato">Gato</option>
              <option value="ave">Ave</option>
              <option value="outros">Outros</option>
            </select>
          </label>
          <label>
            Preferência de Raça ou Características:
            <input
              type="text"
              name="estiloDoPet"
              value={formData.estiloDoPet}
              onChange={handleChange}
            />
          </label>
          <label>
            Atividade Profissional:
            <input
              type="text"
              name="trabalho"
              value={formData.trabalho}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Horário de Trabalho:
            <input
              type="text"
              name="horasTrabalhadas"
              value={formData.horasTrabalhadas}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Média Salarial:
            <input
              type="number"
              name="mediaSalarial"
              value={formData.mediaSalarial}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Motivo da Adoção:
            <textarea
              name="motivoDaAdocao"
              value={formData.motivoDaAdocao}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Compromisso com Cuidados:
            <textarea
              name="compromissoDeCuidar"
              value={formData.compromissoDeCuidar}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Experiência Prévia com Animais:
            <textarea
              name="outrasExperiencias"
              value={formData.outrasExperiencias}
              onChange={handleChange}
            />
          </label>
          <label>
            Outras Considerações:
            <textarea
              name="infoAdicional"
              value={formData.infoAdicional}
              onChange={handleChange}
            />
          </label>

          <button type="submit">Cadastrar</button>
        </form>
      </section>
    </>
  );
}

