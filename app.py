from flask import Flask, render_template, request

app = Flask(__name__)

# Taxas anuais médias (educacionais)
SELIC = 0.105   # 10,5% a.a
IPCA = 0.045    # 4,5% a.a

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        valor_inicial = float(request.form["valor_inicial"])
        aporte = float(request.form["aporte"])
        anos = int(request.form["anos"])
        tipo = request.form["tipo"]

        total_investido = valor_inicial + aporte * 12 * anos

        if tipo == "selic":
            taxa = SELIC
            explicacao = "Tesouro Selic acompanha a taxa básica da economia."

        elif tipo == "ipca":
            adicional = float(request.form["ipca_extra"]) / 100
            taxa = IPCA + adicional
            explicacao = "Tesouro IPCA+ protege contra a inflação e gera ganho real."

        elif tipo == "cdb":
            percentual_cdi = float(request.form["cdi"]) / 100
            taxa = SELIC * percentual_cdi
            explicacao = "CDB rende um percentual do CDI, que acompanha a Selic."

        montante = valor_inicial
        for _ in range(anos * 12):
            montante = montante * (1 + taxa / 12) + aporte

        rendimento = montante - total_investido
        percentual = (rendimento / total_investido) * 100 if total_investido > 0 else 0

        vale = "Vale a pena" if percentual > 0 else "Não vale a pena"

        resultado = {
            "total": round(total_investido, 2),
            "final": round(montante, 2),
            "rendimento": round(rendimento, 2),
            "percentual": round(percentual, 2),
            "vale": vale,
            "explicacao": explicacao
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)