import os
import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_AQUI"))  
except Exception as e:
    st.error(f"Erro na configuração da API: {e}. Verifique se sua chave de API está correta.")
    st.stop()


model = genai.GenerativeModel("gemini-2.0-flash")

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'):
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None
    
st.title("Gerador de Receitas ")

st.markdown("Este aplicativo sugere receitas com base nos ingredientes disponíveis, tipo de culinária e restrições alimentares.")


ingredientes = st.text_area(" Ingredientes Principais", placeholder="Ex: frango, macarrão, carne, arroz")

tipo_culinaria = st.selectbox(
    "Tipo de Culinária",
    ["Italiana", "Brasileira", "Asiática", "Americana", "Qualquer uma"]
)


nivel_dificuldade = st.slider(
    " Nível de Dificuldade (1 = Muito Fácil, 5 = Desafiador)",
    min_value=1, max_value=5, value=3
)


possui_restricao = st.checkbox("Possui Restrição Alimentar?")
restricao_str = ""

if possui_restricao:
    restricao = st.text_input("Descreva a restrição (ex: sem glúten, vegetariana, sem lactose):")
    if restricao:
        restricao_str = f"Considere também a seguinte restrição alimentar: {restricao}."


if st.button("Sugestão de Receita"):
    if not ingredientes.strip():
        st.warning("Por favor, insira ao menos um ingrediente.")
    else:
        
        prompt = (
            f"Sugira uma receita {tipo_culinaria.lower()} com nível de dificuldade {nivel_dificuldade} "
            f"(sendo 1 muito fácil e 5 desafiador). "
            f"Deve usar principalmente os seguintes ingredientes: '{ingredientes}'. "
            f"{restricao_str} "
            "Apresente o nome da receita, uma lista de ingredientes adicionais se necessário, e um breve passo a passo."
        )

    st.markdown("---")
    st.markdown("⚙️ **Prompt que será enviado para a IA (para fins de aprendizado):**")
    st.text_area("",prompt, height=250)
    st.markdown("---")

    st.info("Aguarde, a IA está montando a Receita dos sonhos...")
    resposta_ia = gerar_resposta_gemini(prompt)

    if resposta_ia:
            st.markdown("### ✨ Sugestão de Receita da IA:")
            st.markdown(resposta_ia)
    else:
            st.error("Não foi possível gerar o receita. Verifique as mensagens acima ou tente novamente mais tarde.")