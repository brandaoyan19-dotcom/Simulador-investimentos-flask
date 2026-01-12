from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        investimento_inicial = float(request.form.get("valor_inicial", 0))
        aporte_mensal = float(request.form.get("aporte_mensal", 0))
        anos = int(request.form.get("anos", 0))
        tipo = request.form.get("tipo_investimento")

        meses = anos * 12
        total_investido = investimento_inicial + (aporte_mensal * meses)

        # Taxas base (educacional)
        selic = 0.10
        ipca = 0.045

        taxa_anual = 0
        descricao = ""

        if tipo == "selic":
            taxa_anual = selic
            descricao = "Tesouro Selic acompanha a taxa básica de juros da economia."

        elif tipo == "ipca":
            adicional = float(request.form.get("adicional_ipca", 0)) / 100
            taxa_anual = ipca + adicional
            descricao = "Tesouro IPCA+ protege seu dinheiro da inflação e adiciona ganho real."

        elif tipo == "cdb":
            percentual_cdi = float(request.form.get("percentual_cdi", 0)) / 100
            taxa_anual = selic * percentual_cdi
            descricao = "CDB rende com base no CDI, que acompanha a Selic."

        # Proteção extra (evita crash)
        if taxa_anual <= 0:
            return render_template("index.html", resultado=None)

        taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
        montante = investimento_inicial

        for _ in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte_mensal

        rendimento = montante - total_investido
        percentual = (rendimento / total_investido) * 100 if total_investido > 0 else 0
        vale_a_pena = percentual >= 5

        resultado = {
            "total_investido": f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "montante": f"R$ {montante:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "rendimento": f"R$ {rendimento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "percentual": f"{percentual:.2f}%",
            "descricao": descricao,
            "veredito": "É uma boa opção para esse objetivo" if vale_a_pena else "Pode não ser a melhor opção agora",
            "explicacao": "O investimento superou a inflação e entregou um crescimento consistente."
            if vale_a_pena else
            "O rendimento foi baixo para o período e objetivo escolhido.",
            "frase_final": "Entender o comportamento do investimento ajuda a tomar decisões mais seguras no futuro."
        }

    return render_template("index.html", resultado=resultado)