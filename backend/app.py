from flask import Flask, jsonify
import yfinance as yf
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas


# Endpoint para dados gerais da ação
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        selected_info = {
            "symbol": stock_info.get("symbol"),
            "longName": stock_info.get("longName"),
            "currentPrice": stock_info.get("currentPrice"),
            "marketCap": stock_info.get("marketCap"),
            "regularMarketOpen": stock_info.get("regularMarketOpen"),
            "regularMarketDayHigh": stock_info.get("regularMarketDayHigh"),
            "regularMarketDayLow": stock_info.get("regularMarketDayLow"),
            "regularMarketVolume": stock_info.get("regularMarketVolume"),
            "currency": stock_info.get("currency")
        }
        return jsonify(selected_info), 200
    except Exception as e:
        print(f"Erro ao buscar dados da ação: {e}")
        return jsonify({"error": str(e)}), 500


# Endpoint para o balanço patrimonial (Balance Sheet)
@app.route('/api/stock/<symbol>/balance-sheet', methods=['GET'])
def get_balance_sheet(symbol):
    try:
        stock = yf.Ticker(symbol)
        balance_sheet = stock.balance_sheet

        if balance_sheet is None or balance_sheet.empty:
            return jsonify({"error": "Dados do balanço patrimonial não disponíveis"}), 404

        balance_sheet.dropna(how='all', inplace=True)
        balance_sheet.dropna(axis=1, how='all', inplace=True)
        balance_sheet.columns = [
            col.strftime('%Y-%m-%d') if isinstance(col, pd.Timestamp) else str(col)
            for col in balance_sheet.columns
        ]
        balance_sheet.reset_index(inplace=True)

        def serialize_value(value):
            try:
                if pd.isna(value):
                    return 'N/A'
                elif isinstance(value, (int, float)):
                    return value
                elif isinstance(value, pd.Timestamp):
                    return value.strftime('%Y-%m-%d')
                elif isinstance(value, pd.Timedelta):
                    return str(value)
                elif isinstance(value, str):
                    return value
                else:
                    return str(value)
            except Exception as e:
                print(f"Erro ao serializar valor: {value} ({e})")
                return 'Invalid'

        for column in balance_sheet.columns:
            balance_sheet[column] = balance_sheet[column].apply(serialize_value)

        balance_sheet_records = balance_sheet.to_dict(orient='records')
        return jsonify(balance_sheet_records), 200

    except Exception as e:
        print(f"Erro ao buscar balanço patrimonial: {e}")
        return jsonify({"error": str(e)}), 500


# Endpoint para o fluxo de caixa (Cash Flow)
@app.route('/api/stock/<symbol>/cash-flow', methods=['GET'])
def get_cash_flow(symbol):
    try:
        print(f"Rota chamada para fluxo de caixa com símbolo: {symbol}")
        stock = yf.Ticker(symbol)
        cash_flow = stock.cashflow
        print(f"Dados brutos de fluxo de caixa: {cash_flow}")

        if cash_flow is None or cash_flow.empty:
            return jsonify({"error": "Dados de fluxo de caixa não disponíveis"}), 404

        cash_flow.dropna(how='all', inplace=True)
        cash_flow.dropna(axis=1, how='all', inplace=True)
        cash_flow.columns = [
            col.strftime('%Y-%m-%d') if isinstance(col, pd.Timestamp) else str(col)
            for col in cash_flow.columns
        ]
        cash_flow.reset_index(inplace=True)

        def serialize_value(value):
            try:
                if pd.isna(value):
                    return 'N/A'
                elif isinstance(value, (int, float)):
                    return value
                elif isinstance(value, pd.Timestamp):
                    return value.strftime('%Y-%m-%d')
                elif isinstance(value, pd.Timedelta):
                    return str(value)
                elif isinstance(value, str):
                    return value
                else:
                    return str(value)
            except Exception as e:
                print(f"Erro ao serializar valor: {value} ({e})")
                return 'Invalid'

        for column in cash_flow.columns:
            cash_flow[column] = cash_flow[column].apply(serialize_value)

        cash_flow_records = cash_flow.to_dict(orient='records')
        return jsonify(cash_flow_records), 200

    except Exception as e:
        print(f"Erro ao buscar fluxo de caixa para {symbol}: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Rotas registradas:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True)
