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

        meses = anos * 12
        total_investido = valor_inicial + aporte_mensal * meses

        if tipo == "selic":
            taxa_anual = 0.11

        elif tipo == "cdb":
            cdi_percentual = float(request.form["cdi_percentual"]) / 100
            taxa_anual = 0.11 * cdi_percentual

        elif tipo == "ipca":
            ipca_extra = float(request.form["ipca_extra"]) / 100
            taxa_anual = 0.04 + ipca_extra

        else:
            taxa_anual = 0

        taxa_mensal = (1 + taxa_anual) ** (1/12) - 1

        saldo = valor_inicial
        for _ in range(meses):
            saldo *= (1 + taxa_mensal)
            saldo += aporte_mensal

        resultado = {
            "total_investido": round(total_investido, 2),
            "saldo_final": round(saldo, 2),
            "lucro": round(saldo - total_investido, 2)
        }

        return render_template(
            "index.html",
            resultado=resultado,
            tipo=tipo
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)