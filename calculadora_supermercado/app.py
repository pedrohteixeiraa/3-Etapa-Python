import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Calculadora", page_icon="🛒", layout="centered")

st.title("🛒 Calculadora de Compras de Supermercado")
st.write("Selecione os itens, veja o total da compra e calcule o troco.")

# 2. Base de dados (dicionário de preços)
precos_itens = {
    "Arroz (5kg)": 25.90,
    "Feijão (1kg)": 8.50,
    "Leite (1L)": 4.90,
    "Café (500g)": 14.20,
    "Açúcar (1kg)": 4.30,
    "Óleo de Soja (900ml)": 6.80,
    "Pão de Forma": 7.50,
    "Macarrão (500g)": 4.60,
    "Farinha de Trigo (1kg)": 5.40,
    "Ovos (dúzia)": 12.00,
    "Manteiga (200g)": 11.90,
    "Queijo Mussarela (kg)": 42.00,
    "Frango (kg)": 14.90,
    "Carne Moída (kg)": 36.50,
    "Banana (kg)": 6.20,
    "Tomate (kg)": 7.80,
    "Batata (kg)": 5.90,
    "Sabão em Pó (1kg)": 13.50,
    "Papel Higiênico (12 un)": 18.90,
    "Refrigerante (2L)": 9.50,
}


# 3. Funções
def calcular_preco_total(itens_selecionados):
    """Soma o preço dos itens selecionados."""
    total = sum(precos_itens[item] for item in itens_selecionados)
    return total


def calcular_troco(valor_pago, total_compra):
    """Retorna o troco (valor pago - total), arredondado em centavos."""
    return round(valor_pago - total_compra, 2)


def decompor_troco(troco):
    """Decompõe o troco em cédulas e moedas (usa centavos para evitar erro de ponto flutuante)."""
    centavos = round(troco * 100)
    denominacoes = [
        (20000, "Nota de R$ 200"), (10000, "Nota de R$ 100"), (5000, "Nota de R$ 50"),
        (2000, "Nota de R$ 20"), (1000, "Nota de R$ 10"), (500, "Nota de R$ 5"),
        (200, "Nota de R$ 2"), (100, "Moeda de R$ 1"), (50, "Moeda de R$ 0,50"),
        (25, "Moeda de R$ 0,25"), (10, "Moeda de R$ 0,10"), (5, "Moeda de R$ 0,05"),
    ]
    resultado = []
    for valor, nome in denominacoes:
        qtd, centavos = divmod(centavos, valor)
        if qtd:
            resultado.append((qtd, nome))
    return resultado


# 4. Seleção dos itens
itens_selecionados = st.multiselect(
    label="Selecione os itens do supermercado:",
    options=list(precos_itens.keys()),
)

# 5. Exibição dos detalhes e cálculo do total
total_compra = 0.0
if itens_selecionados:
    st.subheader("Itens Selecionados:")
    for item in itens_selecionados:
        st.write(f"- {item}: R$ {precos_itens[item]:.2f}")

    total_compra = calcular_preco_total(itens_selecionados)

    st.divider()
    st.metric(label="Total da Compra", value=f"R$ {total_compra:.2f}")
else:
    st.info("Nenhum item selecionado. Marque os produtos acima para ver o valor total.")

# 6. Calculadora de troco
st.divider()
st.subheader("💵 Pagamento e Troco")

col1, col2 = st.columns(2)
with col1:
    valor_pago = st.number_input("Dinheiro entregue (R$):", min_value=0.0, value=0.0, step=1.0, format="%.2f")
with col2:
    st.write("")  # alinhamento visual com o campo ao lado
    st.write("")
    botao_calcular = st.button("Calcular Troco", type="primary", use_container_width=True)

if botao_calcular:
    if not itens_selecionados:
        st.info("Selecione ao menos um item antes de calcular o troco.")
    elif valor_pago >= total_compra:
        troco = calcular_troco(valor_pago, total_compra)
        if troco == 0:
            st.success("✅ Pagamento exato! Não há troco a devolver.")
        else:
            st.success(f"✅ Troco a devolver: R$ {troco:.2f}")
            with st.expander("Como entregar o troco (menor nº de cédulas/moedas)"):
                for qtd, nome in decompor_troco(troco):
                    st.write(f"- {qtd}x {nome}")
    else:
        falta = calcular_troco(total_compra, valor_pago)
        st.error(f"❌ Valor pago insuficiente! Faltam R$ {falta:.2f}.")
