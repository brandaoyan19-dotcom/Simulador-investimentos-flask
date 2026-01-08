from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    explicacao = None

    if request.method == "POST":
        valor_inicial = float(request.form.get("valor", 0))
        aporte_mensal = float(request.form.get("aporte", 0))
        anos = int(request.form.get("tempo", 0))
        tipo = request.form.get("tipo")

        meses = anos * 12
        total_investido = valor_inicial + aporte_mensal * meses
        montante = valor_inicial

        if tipo == "cdb":
            percentual_cdi = float(request.form.get("percentual_cdi", 0))
            cdi_anual = 0.10  # 10% ao ano (educativo)
            taxa_anual = cdi_anual * (percentual_cdi / 100)
            taxa_mensal = taxa_anual / 12

            for _ in range(meses):
                montante = montante * (1 + taxa_mensal) + aporte_mensal

            explicacao = (
                f"Este CDB rende {percentual_cdi}% do CDI. "
                f"Quanto maior o percentual, maior o rendimento ao longo do tempo."
            )

        elif tipo == "ipca":
            adicional = float(request.form.get("adicional", 0))
            ipca_anual = 0.04  # 4% ao ano (educativo)
            taxa_anual = ipca_anual + (adicional / 100)
            taxa_mensal = taxa_anual / 12

            for _ in range(meses):
                montante = montante * (1 + taxa_mensal) + aporte_mensal

            explicacao = (
                f"O IPCA+ protege contra a inflação ({ipca_anual*100:.1f}%) "
                f"e ainda paga {adicional}% ao ano acima dela."
            )

        lucro = montante - total_investido

        resultado = (
            f"Total investido: R$ {total_investido:,.2f}<br>"
            f"Valor final: R$ {montante:,.2f}<br>"
            f"Lucro: R$ {lucro:,.2f}"
        )

    return render_template("index.html", resultado=resultado, explicacao=explicacao)

if __name__ == "__main__":
    app.run(debug=True)