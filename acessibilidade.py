import streamlit as st

def aplicar_acessibilidade():
    """Aplica melhorias de acessibilidade em todas as páginas"""
    
    # Link para pular navegação
    st.markdown(
        '<a href="#main-content" style="position:absolute;top:-40px;left:0;background:white;color:blue;padding:10px;">'
        'Pular para o conteúdo</a>',
        unsafe_allow_html=True
    )

    # Adiciona um contêiner principal para acessibilidade
    st.markdown('<div role="main" id="main-content">', unsafe_allow_html=True)
