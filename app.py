from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = False

    if request.method == "POST":
        valor_inicial = float(request.form.get("valor_inicial"))
        aporte_mensal = float(request.form.get("aporte_mensal"))
        tempo = int(request.form.get("tempo"))
        tipo = request.form.get("tipo")

        # Taxas anuais médias (educacionais)
        selic = 0.10
        ipca = 0.04
        cdi = 0.10

        ipca_adicional = float(request.form.get("ipca_adicional") or 0)
        cdi_percentual = float(request.form.get("cdi_percentual") or 100)

        meses = tempo * 12
        total_investido = valor_inicial + aporte_mensal * meses

        if tipo == "selic":
            taxa = selic

        elif tipo == "ipca":
            taxa = ipca + (ipca_adicional / 100)

        elif tipo == "cdb":
            taxa = cdi * (cdi_percentual / 100)

        montante = valor_inicial
        taxa_mensal = (1 + taxa) ** (1 / 12) - 1

        for _ in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte_mensal

        lucro = montante - total_investido
        percentual = (lucro / total_investido) * 100

        vale_a_pena = "Vale a pena" if percentual >= 6 else "Não vale a pena"
        explicacao = (
            "Boa escolha para o período escolhido."
            if percentual >= 6
            else "Pode render pouco para esse prazo."
        )

        resultado = True

        return render_template(
            "index.html",
            resultado=resultado,
            tipo=tipo,
            tempo=tempo,
            total_investido=round(total_investido, 2),
            montante=round(montante, 2),
            lucro=round(lucro, 2),
            percentual=round(percentual, 2),
            vale_a_pena=vale_a_pena,
            explicacao=explicacao
        )

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)