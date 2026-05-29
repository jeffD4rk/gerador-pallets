import streamlit as st
import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Configuração da página
st.set_page_config(page_title="Gerador de Pallets", page_icon="📦", layout="centered")

# CSS para deixar os botões mais bonitos
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    iframe {
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Gerador de Pallets")

# Campos de entrada
nome_carga = st.text_input("Nome da Carga:").strip().upper()
onda_carga = st.text_input("Número da Onda:").strip().upper()

col1, col2 = st.columns(2)
with col1:
    total_folhas = st.number_input("Pallets Normais:", min_value=0, step=1)
with col2:
    total_chocos = st.number_input("Chocos:", min_value=0, step=1)

# Inicializa o estado para guardar o PDF
if 'pdf_processado' not in st.session_state:
    st.session_state.pdf_processado = None

if st.button("🚀 GERAR ETIQUETAS", type="primary"):
    if not nome_carga or not onda_carga:
        st.error("Preencha Carga e Onda!")
    elif total_folhas == 0 and total_chocos == 0:
        st.error("Informe a quantidade!")
    else:
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
        largura, altura = landscape(A4)

        # Lógica de Geração (Pallets Normais)
        for i in range(total_folhas):
            numero_pagina = i + 1
            pdf.setFont("Helvetica-Bold", 44)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 70, "IDENTIFICAÇÃO DE PALLET")
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, altura - 260, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20); pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, altura - 175, "NOME DA CARGA")
            pdf.setFont("Helvetica-Bold", 58); pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 238, nome_carga)
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, 160, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20); pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, 245, "ONDA:")
            pdf.setFont("Helvetica-Bold", 58); pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, 182, onda_carga)
            
            pdf.setFillColor(colors.HexColor("#0F172A"))
            if total_chocos > 0:
                pdf.setFont("Helvetica-Bold", 60)
                texto = f"{numero_pagina} / {total_folhas} + {total_chocos} CHOCO"
            else:
                pdf.setFont("Helvetica-Bold", 90)
                texto = f"{numero_pagina} / {total_folhas}"
            pdf.drawCentredString(largura / 2, 45, texto)
            if numero_pagina < total_folhas or total_chocos > 0: pdf.showPage()

        # Lógica de Geração (Chocos)
        for j in range(total_chocos):
            numero_choco = j + 1
            pdf.setFont("Helvetica-Bold", 44)
            pdf.drawCentredString(largura / 2, altura - 70, "IDENTIFICAÇÃO DE PALLET")
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, altura - 260, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20); pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, altura - 175, "NOME DA CARGA")
            pdf.setFont("Helvetica-Bold", 58); pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 238, nome_carga)
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, 160, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20); pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, 245, "ONDA:")
            pdf.setFont("Helvetica-Bold", 58); pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, 182, onda_carga)
            
            pdf.setFillColor(colors.HexColor("#0F172A"))
            if total_folhas > 0:
                pdf.setFont("Helvetica-Bold", 55)
                texto_choco = f"{total_folhas} PALLETS + {numero_choco} / {total_chocos} CHOCO"
            else:
                pdf.setFont("Helvetica-Bold", 75)
                texto_choco = f"{numero_choco} / {total_chocos} CHOCO"
            pdf.drawCentredString(largura / 2, 50, texto_choco)
            if numero_choco < total_chocos: pdf.showPage()

        pdf.save()
        st.session_state.pdf_processado = buffer.getvalue()
        st.success("Pronto! Escolha uma opção abaixo:")

# Se o PDF já foi gerado, mostra as opções bonitas
if st.session_state.pdf_processado:
    # Botão de Download/Imprimir
    st.download_button(
        label="📥 BAIXAR PARA IMPRIMIR",
        data=st.session_state.pdf_processado,
        file_name=f"pallet_{nome_carga}.pdf",
        mime="application/pdf"
    )

    # Botão de Pré-visualização usando um Expander (mais limpo)
    with st.expander("👁️ CLIQUE PARA VER AS IDENTIFICAÇÕES"):
        base64_pdf = base64.b64encode(st.session_state.pdf_processado).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
