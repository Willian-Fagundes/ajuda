from flask import Flask, jsonify
import pandas as pd


app = Flask(__name__)

# Rota de teste para verificar se a aplicação está rodando
@app.route('/')
def ola_mundo():
    return 'Seja bem-vindo, a aplicação está no ar'

# Rota para pegar os produtos do CSV
@app.route('/pegarprodutos')
def pegarprodutos():
    dados = pd.read_csv('0_bases_originais\Placa_de_Video.csv', sep=',')
    
    dados_json = dados.to_dict(orient='records')
    return jsonify(dados_json)

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
