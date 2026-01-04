from flask import Flask, request, render_template_string

app = Flask(__name__)

# ======================
# TEXTOS EDUCATIVOS
# ======================

EXPLICACOES_INVESTIMENTOS = {
    "selic": "O Tesouro Selic é um investimento muito seguro, indicado para quem pode precisar do dinheiro a qualquer momento. É comum para reserva de emergência.",
    "ipca": "O Tesouro IPCA+ protege seu dinheiro da inflação, garantindo ganho real ao longo do tempo. É indicado para médio e longo prazo.",
    "cdb": "O CDB é um investimento em que você empresta dinheiro ao banco e recebe juros em troca. Pode render mais que a poupança."
}

EXPLICACOES_ADICIONAIS = {
    "ipca_extra": "Esse adicional é o ganho acima da inflação. Exemplo: IPCA + 6% significa que você ganha a inflação do período mais 6% ao ano.",
    "cdi_percentual": "Esse valor indica quanto do CDI o banco paga. Exemplo: 110% do CDI significa um rendimento maior que 100%."
}

EXPLICACAO_APORTE = (
    "O aporte mensal é um valor que você investe todos os meses. "
    "Ele ajuda a aumentar o patrimônio ao longo do tempo e aproveita os juros compostos."
)

EXPLICACAO_RESULTADO = (
    "O crescimento acontece por causa dos juros compostos, onde os juros "
    "passam a render juros ao longo do tempo."
)

# ======================
# HTML
# ======================

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Simulador Educativo de Investimentos</title>
<style>
body {
    font-family: Inter, Arial, sans-serif;
    background: #f5f5f7;
    padding: 20px;
}
.container {
    max-width: 720px;
    margin: auto;
    background: white;
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
h2 { text-align: center; }
label { font-weight: 600; margin-top: 16px; display: block; }
input, select {
    width: 100%; padding: 14px; margin-top: 6px;
    border-radius: 10px; border: 1px solid #ddd;
}
button {
    width: 100%; margin-top: 24px; padding: 14px;
    background: linear-gradient(90deg,#8e44ad,#6c3483);
    color: white; border: none; border-radius: 12px;
    font-size: 18px;
}
.resultado {
    margin-top: 28px; padding: 22px;
    background: #f4ecf7; border-left: 6px solid #8e44ad;
    border-radius: 14px;
}
.alerta { background: #fff6e5; border-left: 6px solid #f39c12; }
.destaque { font-size: 22px; font-weight: bold; }
small { color: #777; }
p { line-height: 1.6; }
</style>
</head>

<body>
<div class="container">

<h2>Simulador Educativo de Investimentos</h2>
<p>Este simulador ajuda você a entender como investir, quanto seu dinheiro pode render e se a escolha vale a pena.</p>

<form method="post">

<label>Valor inicial (R$)</label>
<input type="number" step="0.01" name="valor" required>

<label>Aporte mensal (R$)</label>
<input type="number" step="0.01" name="aporte" value="0">
<small>{{ explicacao_aporte }}</small>

<label>Período (anos)</label>
<input type="number" name="anos" required>

<label>Tipo de investimento</label>
<select name="tipo" id="tipo" onchange="mostrarCampos()" required>
    <option value="">Selecione</option>
    <option value="selic">Tesouro Selic</option>
    <option value="ipca">Tesouro IPCA+</option>
    <option value="cdb">CDB</option>
</select>

<p id="explicacao"></p>

<div id="ipca_extra" style="display:none;">
<label>Adicional do IPCA (%)</label>
<input type="number" step="0.01" name="ipca_extra">
<small>{{ adicionais["ipca_extra"] }}</small>
</div>

<div id="cdi_percentual" style="display:none;">
<label>Percentual do CDI (%)</label>
<input type="number" step="0.01" name="cdi_percentual">
<small>{{ adicionais["cdi_percentual"] }}</small>
</div>

<button type="submit">Simular</button>
</form>

{% if resultado %}
<div class="resultado {% if avaliacao.startswith('Não') %}alerta{% endif %}">
    <p>Total investido: R$ {{ investido }}</p>
    <p class="destaque">Valor final: R$ {{ final }}</p>
    <p>Ganho total: R$ {{ ganho }} ({{ rendimento }}%)</p>
    <p><strong>{{ avaliacao }}</strong></p>
    <p>{{ explicacao_resultado }}</p>
    <p><em>{{ exemplo }}</em></p>
</div>
{% endif %}

</div>

<script>
function mostrarCampos() {
    let tipo = document.getElementById("tipo").value;

    document.getElementById("ipca_extra").style.display = "none";
    document.getElementById("cdi_percentual").style.display = "none";

    let explicacoes = {
        selic: "{{ explicacoes['selic'] }}",
        ipca: "{{ explicacoes['ipca'] }}",
        cdb: "{{ explicacoes['cdb'] }}"
    };

    document.getElementById("explicacao").innerText = explicacoes[tipo] || "";

    if (tipo === "ipca") document.getElementById("ipca_extra").style.display = "block";
    if (tipo === "cdb") document.getElementById("cdi_percentual").style.display = "block";
}
</script>

</body>
</html>
"""

# ======================
# BACKEND
# ======================

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        valor = float(request.form["valor"])
        aporte = float(request.form["aporte"])
        anos = int(request.form["anos"])
        meses = anos * 12
        tipo = request.form["tipo"]

        selic = 0.1375
        ipca = 0.059
        cdi = 0.132

        if tipo == "selic":
            taxa_anual = selic
            exemplo = "Muito usado para reserva de emergência."
        elif tipo == "ipca":
            taxa_anual = ipca + float(request.form.get("ipca_extra", 0)) / 100
            exemplo = "Indicado para aposentadoria ou objetivos de longo prazo."
        else:
            taxa_anual = cdi * (float(request.form.get("cdi_percentual", 100)) / 100)
            exemplo = "Comum para quem busca mais rendimento que a poupança."

        taxa_mensal = (1 + taxa_anual) ** (1/12) - 1

        montante = valor
        for _ in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte

        investido = valor + aporte * meses
        ganho = montante - investido
        rendimento = (ganho / investido) * 100 if investido > 0 else 0

        avaliacao = "Vale a pena ✅" if rendimento > 20 else "Não vale a pena ⚠️"

        return render_template_string(
            HTML,
            resultado=True,
            investido=round(investido, 2),
            final=round(montante, 2),
            ganho=round(ganho, 2),
            rendimento=round(rendimento, 2),
            avaliacao=avaliacao,
            explicacoes=EXPLICACOES_INVESTIMENTOS,
            adicionais=EXPLICACOES_ADICIONAIS,
            explicacao_aporte=EXPLICACAO_APORTE,
            explicacao_resultado=EXPLICACAO_RESULTADO,
            exemplo=exemplo
        )

    return render_template_string(
        HTML,
        resultado=False,
        explicacoes=EXPLICACOES_INVESTIMENTOS,
        adicionais=EXPLICACOES_ADICIONAIS,
        explicacao_aporte=EXPLICACAO_APORTE
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)