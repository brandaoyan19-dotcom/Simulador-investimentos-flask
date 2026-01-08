from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    explicacao = ""

    if request.method == "POST":
        tipo = request.form.get("tipo")
        valor_inicial = float(request.form.get("valor_inicial", 0))
        meses = int(request.form.get("meses", 0))
        aporte = float(request.form.get("aporte_mensal", 0))

        montante = valor_inicial

        if tipo == "selic":
            taxa_anual = 0.13
            taxa_mensal = taxa_anual / 12

            for _ in range(meses):
                montante = montante * (1 + taxa_mensal) + aporte

            explicacao = "Tesouro Selic acompanha a taxa básica de juros."

        elif tipo == "ipca":
            ipca = float(request.form.get("ipca", 0))
            adicional = float(request.form.get("ipca_extra", 0))
            taxa_anual = (ipca + adicional) / 100
            taxa_mensal = taxa_anual / 12

            for _ in range(meses):
                montante = montante * (1 + taxa_mensal) + aporte

            explicacao = "IPCA+ protege contra a inflação e paga um adicional."

        elif tipo == "cdb":
            cdi_percent = float(request.form.get("cdi_percent", 0))
            cdi = 0.13  # CDI aproximado
            taxa_anual = cdi * (cdi_percent / 100)
            taxa_mensal = taxa_anual / 12

            for _ in range(meses):
                montante = montante * (1 + taxa_mensal) + aporte

            explicacao = "CDB rende um percentual do CDI."

        resultado = round(montante, 2)

    return render_template("index.html", resultado=resultado, explicacao=explicacao)

if __name__ == "__main__":
    app.run(debug=True)