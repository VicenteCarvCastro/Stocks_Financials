import React, { useState } from 'react';
import axios from 'axios';

function StockSearch({ onSearch }) { // Recebe a função onSearch como prop
    const [symbol, setSymbol] = useState('');
    const [data, setData] = useState(null);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setData(null);

        if (!symbol) {
            setError('Por favor, insira um ticket de ação.');
            return;
        }

        try {
            const response = await axios.get(`/api/stock/${symbol.toUpperCase()}`);
            setData(response.data);
            onSearch(symbol.toUpperCase()); // Atualiza o ticker no App.js
        } catch (err) {
            setError('Erro ao buscar dados. Verifique o ticket e tente novamente.');
        }
    };

    return (
        <div className="container mt-5">
            <h1>Buscador de Ações</h1>
            <form onSubmit={handleSubmit} className="form-inline my-4">
                <input
                    type="text"
                    className="form-control mr-2"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                    placeholder="Símbolo da ação (ex: AAPL)"
                />
                <button type="submit" className="btn btn-primary">Buscar</button>
            </form>
            {error && <div className="alert alert-danger">{error}</div>}
            {data && (
                <div className="card">
                    <div className="card-body">
                        <h3 className="card-title">{data.longName} ({data.symbol})</h3>
                        <p className="card-text">Preço Atual: {data.currentPrice} {data.currency}</p>
                        <p className="card-text">Capitalização de Mercado: {data.marketCap}</p>
                        <p className="card-text">Abertura de Mercado: {data.regularMarketOpen}</p>
                        <p className="card-text">Alta do Dia: {data.regularMarketDayHigh}</p>
                        <p className="card-text">Baixa do Dia: {data.regularMarketDayLow}</p>
                        <p className="card-text">Volume de Mercado: {data.regularMarketVolume}</p>
                    </div>
                </div>
            )}
        </div>
    );
}

export default StockSearch;
