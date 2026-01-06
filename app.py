from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None

    if request.method == "POST":
        try:
            tipo = request.form.get("tipo")
            valor_inicial = float(request.form.get("valor_inicial", 0))
            aporte = float(request.form.get("aporte", 0))
            anos = int(request.form.get("anos", 0))

            # Taxas base (exemplo educacional)
            selic = 0.10
            ipca_base = 0.04

            if tipo == "selic":
                taxa = selic

            elif tipo == "cdb":
                cdi_percentual = float(request.form.get("cdi_percentual", 0)) / 100
                taxa = selic * cdi_percentual

            elif tipo == "ipca":
                ipca_extra = float(request.form.get("ipca_extra", 0)) / 100
                taxa = ipca_base + ipca_extra

            else:
                raise ValueError("Tipo de investimento inválido")

            meses = anos * 12
            montante = valor_inicial

            for _ in range(meses):
                montante = montante * (1 + taxa / 12) + aporte

            resultado = round(montante, 2)

        except Exception as e:
            erro = "Preencha os campos corretamente."

    return render_template("index.html", resultado=resultado, erro=erro)


if __name__ == "__main__":
    app.run(debug=True)