from flask import Flask, render_template, request

app = Flask(__name__)

# Taxas anuais médias (simulação educativa)
SELIC_ANUAL = 0.105   # 10,5% ao ano
CDI_ANUAL = 0.105     # 100% do CDI ≈ Selic
IPCA_ANUAL = 0.045    # 4,5% ao ano


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    mostrar_ipca_extra = False
    mostrar_cdi = False

    if request.method == "POST":
        tipo = request.form.get("tipo")
        valor_inicial = float(request.form.get("valor_inicial"))
        aporte = float(request.form.get("aporte"))
        anos = int(request.form.get("anos"))

        meses = anos * 12
        total_investido = valor_inicial + (aporte * meses)

        # === DEFINIÇÃO DA TAXA ===
        if tipo == "selic":
            taxa_anual = SELIC_ANUAL
            nome = "Tesouro Selic"

        elif tipo == "ipca":
            mostrar_ipca_extra = True
            ipca_extra = float(request.form.get("ipca_extra"))
            taxa_anual = IPCA_ANUAL + (ipca_extra / 100)
            nome = "Tesouro IPCA+"

        elif tipo == "cdb":
            mostrar_cdi = True
            cdi_percentual = float(request.form.get("cdi_percentual"))
            taxa_anual = CDI_ANUAL * (cdi_percentual / 100)
            nome = "CDB"

        else:
            taxa_anual = 0
            nome = "Investimento"

        # === CONVERSÃO PARA TAXA MENSAL ===
        taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1

        # === SIMULAÇÃO ===
        saldo = valor_inicial
        for _ in range(meses):
            saldo = saldo * (1 + taxa_mensal) + aporte

        rendimento = saldo - total_investido
        percentual = (rendimento / total_investido) * 100 if total_investido > 0 else 0

        # === DECISÃO ===
        if percentual >= 6:
            decisao = "✅ Vale a pena investir"
            exemplo = (
                f"Esse investimento superou a inflação e aumentou seu poder de compra. "
                f"É uma boa opção para {anos} anos pensando em segurança."
            )
        else:
            decisao = "⚠️ Não vale tanto a pena"
            exemplo = (
                f"O rendimento foi baixo para o período. "
                f"Talvez seja melhor comparar com outras opções ou prazos maiores."
            )

        resultado = {
            "total_investido": f"{total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "total_final": f"{saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "percentual": f"{percentual:.2f}",
            "decisao": decisao,
            "exemplo": exemplo,
        }

    return render_template(
        "index.html",
        resultado=resultado,
        mostrar_ipca_extra=mostrar_ipca_extra,
        mostrar_cdi=mostrar_cdi
    )


if __name__ == "__main__":
    app.run(debug=True)