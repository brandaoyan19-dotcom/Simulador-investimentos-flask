from flask import Flask, render_template, request

app = Flask(__name__)

SELIC_ANUAL = 0.13      # 13% a.a.
IPCA_ANUAL = 0.045     # 4,5% a.a.

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        tipo = request.form.get("tipo")
        valor_inicial = float(request.form.get("valor_inicial", 0))
        aporte_mensal = float(request.form.get("aporte_mensal", 0))
        anos = int(request.form.get("periodo", 0))

        meses = anos * 12
        total_investido = valor_inicial + (aporte_mensal * meses)

        rendimento = 0
        taxa_anual_usada = 0
        explicacao = ""
        vale_a_pena = ""

        if tipo == "selic":
            taxa_anual_usada = SELIC_ANUAL
            taxa_mensal = (1 + taxa_anual_usada) ** (1/12) - 1
            rendimento = total_investido * ((1 + taxa_mensal) ** meses - 1)

            explicacao = (
                "O Tesouro Selic acompanha a taxa básica de juros da economia. "
                "É indicado para curto prazo e reserva de emergência."
            )
            vale_a_pena = "Vale a pena se você busca segurança e liquidez."

        elif tipo == "ipca":
            ipca_extra = float(request.form.get("ipca_extra", 0))
            taxa_anual_usada = IPCA_ANUAL + (ipca_extra / 100)
            taxa_mensal = (1 + taxa_anual_usada) ** (1/12) - 1
            rendimento = total_investido * ((1 + taxa_mensal) ** meses - 1)

            explicacao = (
                f"O Tesouro IPCA+ protege contra a inflação (IPCA ≈ {IPCA_ANUAL*100:.1f}% a.a.) "
                f"e ainda paga um ganho real de {ipca_extra:.1f}% ao ano."
            )
            vale_a_pena = "Vale a pena principalmente para objetivos de longo prazo."

        elif tipo == "cdb":
            cdi_percent = float(request.form.get("cdi_percent", 0))
            taxa_anual_usada = SELIC_ANUAL * (cdi_percent / 100)
            taxa_mensal = (1 + taxa_anual_usada) ** (1/12) - 1
            rendimento = total_investido * ((1 + taxa_mensal) ** meses - 1)

            explicacao = (
                f"O CDB rende {cdi_percent:.0f}% do CDI. "
                f"Como o CDI acompanha a Selic (~{SELIC_ANUAL*100:.1f}% a.a.), "
                f"seu investimento rendeu cerca de {taxa_anual_usada*100:.1f}% ao ano."
            )
            vale_a_pena = "Vale a pena se o banco for confiável e o percentual do CDI for alto."

        valor_final = total_investido + rendimento
        percentual_ganho = (rendimento / total_investido) * 100 if total_investido > 0 else 0

        resultado = {
            "total_investido": round(total_investido, 2),
            "rendimento": round(rendimento, 2),
            "valor_final": round(valor_final, 2),
            "percentual_ganho": round(percentual_ganho, 2),
            "explicacao": explicacao,
            "vale_a_pena": vale_a_pena
        }

    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)