from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        investimento_inicial = float(request.form["investimento_inicial"])
        aporte_mensal = float(request.form["aporte_mensal"])
        anos = int(request.form["anos"])
        tipo = request.form["tipo"]

        meses = anos * 12
        total_investido = investimento_inicial + (aporte_mensal * meses)

        # Taxas base anuais
        selic = 0.10
        ipca = 0.045

        if tipo == "selic":
            taxa_anual = selic

        elif tipo == "ipca":
            adicional = float(request.form["ipca_adicional"]) / 100
            taxa_anual = ipca + adicional

        elif tipo == "cdb":
            percentual_cdi = float(request.form["cdi_percentual"]) / 100
            taxa_anual = selic * percentual_cdi

        taxa_mensal = (1 + taxa_anual) ** (1/12) - 1

        montante = investimento_inicial
        for _ in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte_mensal

        rendimento = montante - total_investido
        percentual = (rendimento / total_investido) * 100 if total_investido > 0 else 0

        vale_a_pena = percentual >= 5

        resultado = {
            "total_investido": f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "montante": f"R$ {montante:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "percentual": f"{percentual:.2f}%",
            "veredito": "É uma boa opção para esse objetivo" if vale_a_pena else "Pode não ser a melhor opção agora",
            "explicacao": "O investimento superou a inflação e entregou um crescimento consistente."
            if vale_a_pena else
            "O rendimento foi baixo para o período e objetivo escolhido.",
            "frase_final": "Entender o comportamento do investimento ajuda a tomar decisões mais seguras no futuro."
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)