from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        investimento_inicial = float(request.form["inicial"])
        aporte_mensal = float(request.form["aporte"])
        anos = int(request.form["anos"])
        tipo = request.form["tipo"]

        meses = anos * 12
        total_investido = investimento_inicial + aporte_mensal * meses

        # Taxas anuais (simulação educacional)
        selic = 0.1065
        ipca = 0.045

        if tipo == "selic":
            taxa_anual = selic
            descricao = "Tesouro Selic acompanha a taxa básica de juros da economia."

        elif tipo == "ipca":
            adicional = float(request.form["ipca_extra"]) / 100
            taxa_anual = ipca + adicional
            descricao = "Tesouro IPCA+ protege seu dinheiro da inflação e adiciona ganho real."

        elif tipo == "cdb":
            percentual_cdi = float(request.form["cdi_percentual"]) / 100
            taxa_anual = selic * percentual_cdi
            descricao = "CDB rende com base no CDI, que acompanha a Selic."

        saldo = investimento_inicial
        for _ in range(meses):
            saldo *= (1 + taxa_anual / 12)
            saldo += aporte_mensal

        rendimento = saldo - total_investido
        percentual = (rendimento / total_investido) * 100 if total_investido > 0 else 0

        vale = "Vale a pena" if rendimento > 0 else "Não vale a pena"

        resultado = {
            "saldo": round(saldo, 2),
            "investido": round(total_investido, 2),
            "rendimento": round(rendimento, 2),
            "percentual": round(percentual, 2),
            "descricao": descricao,
            "vale": vale
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)