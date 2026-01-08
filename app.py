from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    explicacao = None

    if request.method == "POST":
        tipo = request.form.get("tipo")
        valor_inicial = float(request.form.get("valor_inicial", 0))
        aporte_mensal = float(request.form.get("aporte_mensal", 0))
        meses = int(request.form.get("periodo", 0))

        total_investido = valor_inicial + (aporte_mensal * meses)

        # Taxas anuais médias (educacionais)
        SELIC_ANUAL = 0.13
        IPCA_ANUAL = 0.045

        rendimento = 0

        if tipo == "selic":
            taxa_mensal = (1 + SELIC_ANUAL) ** (1/12) - 1
            rendimento = total_investido * ((1 + taxa_mensal) ** meses - 1)
            explicacao = "O Tesouro Selic acompanha a taxa básica de juros da economia."

        elif tipo == "ipca":
            ipca_extra = request.form.get("ipca_extra")
            if ipca_extra:
                taxa_anual = IPCA_ANUAL + (float(ipca_extra) / 100)
                taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
                rendimento = total_investido * ((1 + taxa_mensal) ** meses - 1)
                explicacao = "O Tesouro IPCA+ protege contra a inflação e oferece ganho real."

        elif tipo == "cdb":
            cdi_percent = request.form.get("cdi_percent")
            if cdi_percent:
                CDI_ANUAL = SELIC_ANUAL * (float(cdi_percent) / 100)
                taxa_mensal = (1 + CDI_ANUAL) ** (1/12) - 1
                rendimento = total_investido * ((1 + taxa_mensal) ** meses - 1)
                explicacao = "O CDB rende um percentual do CDI, ligado à Selic."

        resultado = {
            "total_investido": round(total_investido, 2),
            "valor_final": round(total_investido + rendimento, 2),
            "rendimento": round(rendimento, 2)
        }

    return render_template("index.html", resultado=resultado, explicacao=explicacao)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)