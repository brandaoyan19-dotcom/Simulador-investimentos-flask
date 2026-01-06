from flask import Flask, render_template, request

app = Flask(__name__)

# Taxas anuais aproximadas (educacionais)
SELIC = 0.1065   # 10,65% a.a.
CDI = 0.1065
IPCA = 0.045     # 4,5% a.a.

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        try:
            valor_inicial = float(request.form["valor_inicial"])
            aporte_mensal = float(request.form["aporte_mensal"])
            anos = int(request.form["anos"])
            tipo = request.form["tipo"]

            total_investido = valor_inicial + aporte_mensal * 12 * anos

            if tipo == "selic":
                taxa = SELIC
                explicacao = "O Tesouro Selic acompanha a taxa básica de juros da economia."

            elif tipo == "ipca":
                ipca_extra = float(request.form["ipca_extra"]) / 100
                taxa = IPCA + ipca_extra
                explicacao = "O Tesouro IPCA+ protege seu dinheiro da inflação e ainda paga um ganho real."

            elif tipo == "cdb":
                cdi_percentual = float(request.form["cdb_percentual"]) / 100
                taxa = CDI * cdi_percentual
                explicacao = "CDBs costumam render um percentual do CDI, que anda próximo da Selic."

            montante = valor_inicial

            for _ in range(anos * 12):
                montante *= (1 + taxa / 12)
                montante += aporte_mensal

            lucro = montante - total_investido
            percentual = (lucro / total_investido) * 100

            avaliacao = "Vale a pena ✅" if percentual > 5 else "Pode não valer a pena ❌"

            resultado = {
                "investido": f"{total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "final": f"{montante:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "lucro": f"{lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "percentual": f"{percentual:.2f}",
                "avaliacao": avaliacao,
                "explicacao": explicacao
            }

        except Exception as e:
            resultado = {"erro": str(e)}

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)