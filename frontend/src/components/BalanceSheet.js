import React, { useEffect, useState } from 'react';
import axios from 'axios';

function BalanceSheet({ ticker }) {
  const [balanceSheet, setBalanceSheet] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    // Faz a requisição para o endpoint de Balance Sheet no backend
    axios.get(`http://127.0.0.1:5000/api/stock/${ticker}/balance-sheet`)
      .then(response => {
        setBalanceSheet(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Erro ao buscar balanço patrimonial:', error);
        setError(
          error.response && error.response.data && error.response.data.error
            ? error.response.data.error
            : 'Erro desconhecido'
        );
        setLoading(false);
      });
  }, [ticker]);

  return (
    <div>
      <h1>Balance Sheet para {ticker}</h1>
      {loading && <p>Carregando...</p>}
      {error && <p>Erro ao carregar dados: {error}</p>}
      {balanceSheet.length > 0 && (
        <table border="1">
          <thead>
            <tr>
              {Object.keys(balanceSheet[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {balanceSheet.map((row, idx) => (
              <tr key={idx}>
                {Object.values(row).map((val, idx2) => (
                  <td key={idx2}>{val !== null ? val.toString() : 'N/A'}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default BalanceSheet;
