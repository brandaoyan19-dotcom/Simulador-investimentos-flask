from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    explicacao = None

    if request.method == "POST":
        tipo = request.form.get("tipo")
        valor = float(request.form.get("valor", 0))
        tempo = int(request.form.get("tempo", 0))

        # CDB
        if tipo == "cdb":
            percentual_cdi = float(request.form.get("percentual_cdi", 0))
            cdi_ano = 13.65 / 100  # CDI médio
            taxa = (percentual_cdi / 100) * cdi_ano
            montante = valor * ((1 + taxa) ** tempo)
            rendimento = montante - valor

            resultado = f"Valor final: R$ {montante:,.2f}"
            explicacao = (
                f"Você investiu R$ {valor:,.2f} em um CDB por {tempo} anos. "
                f"Com {percentual_cdi}% do CDI, seu rendimento foi de "
                f"R$ {rendimento:,.2f}. "
                "CDB costuma ser uma opção segura, principalmente quando "
                "tem cobertura do FGC."
            )

        # IPCA+
        elif tipo == "ipca":
            adicional = float(request.form.get("adicional", 0)) / 100
            ipca_ano = 4 / 100  # IPCA médio
            taxa = ipca_ano + adicional
            montante = valor * ((1 + taxa) ** tempo)
            rendimento = montante - valor

            resultado = f"Valor final: R$ {montante:,.2f}"
            explicacao = (
                f"Você investiu R$ {valor:,.2f} em um título IPCA+ por {tempo} anos. "
                f"Além da inflação, você ganhou {adicional*100:.2f}% ao ano. "
                f"O rendimento total foi de R$ {rendimento:,.2f}. "
                "Esse tipo de investimento protege seu dinheiro da inflação."
            )

    return render_template(
        "index.html",
        resultado=resultado,
        explicacao=explicacao
    )

if __name__ == "__main__":
    app.run(debug=True)