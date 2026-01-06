from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        try:
            tipo = request.form.get("tipo")
            valor_inicial = float(request.form.get("valor_inicial"))
            aporte = float(request.form.get("aporte"))
            anos = int(request.form.get("anos"))

            selic = 0.10
            ipca_base = 0.04

            if tipo == "selic":
                taxa = selic

            elif tipo == "cdb":
                cdi_percentual = float(request.form.get("cdi_percentual")) / 100
                taxa = selic * cdi_percentual

            elif tipo == "ipca":
                ipca_extra = float(request.form.get("ipca_extra")) / 100
                taxa = ipca_base + ipca_extra

            meses = anos * 12
            montante = valor_inicial

            for _ in range(meses):
                montante = montante * (1 + taxa / 12) + aporte

            total_investido = valor_inicial + aporte * meses
            lucro = montante - total_investido
            rendimento_pct = (lucro / total_investido) * 100

            if rendimento_pct > 50:
                avaliacao = "Excelente resultado para o longo prazo 📈"
            elif rendimento_pct > 20:
                avaliacao = "Bom rendimento, consistente 👍"
            else:
                avaliacao = "Rendimento baixo, vale comparar opções ⚠️"

            resultado = {
                "final": round(montante, 2),
                "investido": round(total_investido, 2),
                "lucro": round(lucro, 2),
                "percentual": round(rendimento_pct, 2),
                "avaliacao": avaliacao
            }

        except:
            resultado = {"erro": "Preencha os campos corretamente."}

    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)