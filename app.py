from flask import Flask, render_template, request

app = Flask(__name__)

SELIC_ANUAL = 0.13  # 13% a.a. (exemplo educativo)
IPCA_ANUAL = 0.045  # 4,5% a.a. (exemplo educativo)

def formatar(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        valor_inicial = float(request.form["valor_inicial"])
        aporte_mensal = float(request.form["aporte_mensal"])
        anos = int(request.form["anos"])
        tipo = request.form["tipo"]

        meses = anos * 12
        investido = valor_inicial + aporte_mensal * meses

        if tipo == "selic":
            taxa_mensal = SELIC_ANUAL / 12
            explicacao = "O Tesouro Selic é indicado para quem busca segurança e liquidez."
        elif tipo == "ipca":
            adicional = float(request.form["ipca_adicional"]) / 100
            taxa_mensal = (IPCA_ANUAL + adicional) / 12
            explicacao = "O Tesouro IPCA+ protege o poder de compra no longo prazo."
        elif tipo == "cdb":
            cdi = float(request.form["cdi_percentual"]) / 100
            taxa_mensal = (SELIC_ANUAL * cdi) / 12
            explicacao = "O CDB rende conforme o percentual do CDI contratado."
        else:
            taxa_mensal = 0
            explicacao = ""

        total = valor_inicial
        for _ in range(meses):
            total = total * (1 + taxa_mensal) + aporte_mensal

        rendimento = total - investido
        percentual = (rendimento / investido) * 100 if investido > 0 else 0

        if tipo == "ipca" and anos < 3:
            veredito = "Para prazos curtos, esse investimento geralmente não vale a pena."
            classe = "no"
        else:
            veredito = "Para esse prazo, o investimento tende a valer a pena."
            classe = "ok"

        resultado = {
            "investido": formatar(investido),
            "final": formatar(total),
            "rendimento": formatar(rendimento),
            "percentual": f"{percentual:.2f}",
            "explicacao": explicacao,
            "veredito": veredito,
            "classe": classe
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)