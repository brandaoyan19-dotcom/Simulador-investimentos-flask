from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        tipo = request.form.get("tipo")
        capital = float(request.form.get("capital"))
        aporte = float(request.form.get("aporte"))
        anos = int(request.form.get("anos"))

        selic = 0.105   # 10,5% ao ano (exemplo educativo)
        cdi = 0.10
        ipca = 0.045

        if tipo == "selic":
            taxa = selic
            nome = "Tesouro Selic"

        elif tipo == "cdi":
            perc_cdi = float(request.form.get("perc_cdi")) / 100
            taxa = cdi * perc_cdi
            nome = "CDB atrelado ao CDI"

        elif tipo == "ipca":
            adicional = float(request.form.get("ipca_extra")) / 100
            taxa = ipca + adicional
            nome = "Tesouro IPCA+"

        meses = anos * 12
        montante = capital

        for _ in range(meses):
            montante = montante * (1 + taxa/12) + aporte

        investido = capital + aporte * meses
        rendimento = montante - investido
        percentual = (rendimento / investido) * 100 if investido > 0 else 0

        vale = "VALE A PENA" if rendimento > 0 else "NÃO VALE A PENA"

        resultado = {
            "nome": nome,
            "montante": round(montante, 2),
            "investido": round(investido, 2),
            "rendimento": round(rendimento, 2),
            "percentual": round(percentual, 2),
            "vale": vale
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)