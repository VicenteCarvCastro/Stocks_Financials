import yfinance as yf

# Escolha um símbolo de ação (por exemplo, AAPL para Apple, MSFT para Microsoft)
ticker_symbol = 'AAPL'

# Baixar os dados da empresa
empresa = yf.Ticker(ticker_symbol)

info = empresa.info

# Exibir as principais informações
print(f"Nome da Empresa: {info['longName']}")
print(f"Setor: {info['sector']}")
print(f"Indústria: {info['industry']}")

# Obter o histórico de preços
historico = empresa.history(period="1mo")  # últimos 30 dias
#print(historico)

# Obter dados financeiros específicos (por exemplo, balanço patrimonial)
balanco_patrimonial = empresa.balance_sheet
print(balanco_patrimonial)

# Obter informações dos dividendos
dividendos = empresa.dividends
#print(dividendos)

# Obter informações dos eventos futuros, como earnings dates
proximos_eventos = empresa.calendar
#print(proximos_eventos)
