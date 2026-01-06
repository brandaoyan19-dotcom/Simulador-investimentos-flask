from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        valor_inicial = float(request.form["valor_inicial"])
        aporte_mensal = float(request.form["aporte_mensal"])
        anos = int(request.form["anos"])
        tipo = request.form["tipo"]

        # Taxas médias educacionais
        if tipo == "selic":
            taxa_anual = 0.105
            descricao = "A Selic é a taxa básica da economia. Indicada para segurança."
        elif tipo == "cdi":
            percentual_cdi = float(request.form["percentual_cdi"]) / 100
            taxa_anual = 0.105 * percentual_cdi
            descricao = "O CDI acompanha a Selic e é comum em CDBs."
        elif tipo == "ipca":
            adicional_ipca = float(request.form["ipca_adicional"]) / 100
            taxa_anual = 0.04 + adicional_ipca
            descricao = "O IPCA protege contra a inflação no longo prazo."
        else:
            taxa_anual = 0
            descricao = ""

        taxa_mensal = taxa_anual / 12
        meses = anos * 12

        montante = valor_inicial
        total_investido = valor_inicial + aporte_mensal * meses

        for _ in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte_mensal

        lucro = montante - total_investido
        rendimento_percentual = (lucro / total_investido) * 100

        resultado = {
            "total_investido": round(total_investido, 2),
            "valor_final": round(montante, 2),
            "lucro": round(lucro, 2),
            "rendimento": round(rendimento_percentual, 2),
            "descricao": descricao,
            "vale_a_pena": rendimento_percentual > 100
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)