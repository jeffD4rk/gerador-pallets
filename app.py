import streamlit as st
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Configuração da página no celular
st.set_page_config(page_title="Gerador de Pallets", page_icon="📦", layout="centered")

st.title("📦 Sistema de Pallets Oficial")
st.write("Preencha os dados abaixo para gerar o PDF das etiquetas.")

# Campos de digitação na tela do celular
nome_carga = st.text_input("1. NOME DA CARGA:").strip().upper()
onda_carga = st.text_input("2. NÚMERO DA ONDA:").strip().upper()
total_folhas = st.number_input("3. QUANTIDADE DE PALLETS NORMAIS:", min_value=0, value=0, step=1)
total_chocos = st.number_input("4. CHOCOS ADICIONAIS:", min_value=0, value=0, step=1)

if st.button("GERAR DOCUMENTO", type="primary"):
    if not nome_carga or not list(nome_carga):
        st.warning("Por favor, digite o Nome da Carga.")
    elif not list(onda_carga):
        st.warning("Por favor, digite o Número da Onda.")
    elif total_folhas == 0 and total_chocos == 0:
        st.warning("Digite uma quantidade para Pallets Normais ou para Chocos.")
    else:
        # Cria o PDF na memória do celular
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
        largura, altura = landscape(A4)

        # 📦 PARTE 1: PALLETS NORMAIS
        for i in range(total_folhas):
            numero_pagina = i + 1
            pdf.setFont("Helvetica-Bold", 44)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 70, "IDENTIFICAÇÃO DE PALLET")
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, altura - 260, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, altura - 175, "NOME DA CARGA")
            pdf.setFont("Helvetica-Bold", 58)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 238, nome_carga)
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, 160, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, 245, "ONDA:")
            pdf.setFont("Helvetica-Bold", 58)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, 182, onda_carga)
            
            pdf.setFillColor(colors.HexColor("#0F172A"))
            if total_chocos > 0:
                pdf.setFont("Helvetica-Bold", 75)
                texto_contagem = f"{numero_pagina} / {total_folhas} + {total_chocos} CHOCO"
            else:
                pdf.setFont("Helvetica-Bold", 90)
                texto_contagem = f"{numero_pagina} / {total_folhas}"
            pdf.drawCentredString(largura / 2, 45, texto_contagem)
            
            if numero_pagina < total_folhas or total_chocos > 0:
                pdf.showPage()

        # 🍫 PARTE 2: PALLETS DE CHOCOLATE
        for j in range(total_chocos):
            numero_choco = j + 1
            pdf.setFont("Helvetica-Bold", 44)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 70, "IDENTIFICAÇÃO DE PALLET")
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, altura - 260, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, altura - 175, "NOME DA CARGA")
            pdf.setFont("Helvetica-Bold", 58)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, altura - 238, nome_carga)
            
            pdf.setFillColor(colors.HexColor("#F8FAFC"))
            pdf.roundRect(55, 160, largura - 110, 120, 12, stroke=0, fill=1)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.setFillColor(colors.HexColor("#64748B"))
            pdf.drawCentredString(largura / 2, 245, "ONDA:")
            pdf.setFont("Helvetica-Bold", 58)
            pdf.setFillColor(colors.HexColor("#0F172A"))
            pdf.drawCentredString(largura / 2, 182, onda_carga)
            
            pdf.setFillColor(colors.HexColor("#0F172A"))
            if total_folhas > 0:
                pdf.setFont("Helvetica-Bold", 65)
                texto_contagem_choco = f"{total_folhas} PALLETS + {numero_choco} / {total_chocos} CHOCO"
            else:
                pdf.setFont("Helvetica-Bold", 80)
                texto_contagem_choco = f"{numero_choco} / {total_chocos} CHOCO"
            pdf.drawCentredString(largura / 2, 50, texto_contagem_choco)
            
            if numero_choco < total_chocos:
                pdf.showPage()

        pdf.save()
        buffer.seek(0)

        # Cria o botão de download que o celular entende
        st.success("✅ PDF Gerado com sucesso!")
        st.download_button(
            label="📥 BAIXAR E ABRIR PDF",
            data=buffer,
            file_name=f"pallet_{nome_carga}.pdf",
            mime="application/pdf"
        )