import React, { useState } from 'react';
import './App.css';
import StockSearch from './components/StockSearch';
import BalanceSheet from './components/BalanceSheet';
import CashFlow from './components/CashFlow';

function App() {
  const [ticker, setTicker] = useState(''); // Inicializa com "AAPL"

  return (
    <div className="App">
      <StockSearch onSearch={(symbol) => setTicker(symbol)} />
      <BalanceSheet ticker={ticker} />
      <CashFlow ticker={ticker} />
    </div>
  );
}

export default App;
