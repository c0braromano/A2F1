# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 20:05:15 2022

@author: roman
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors



def build_pdf(tab_maquinas):
    from reportlab.pdfgen import canvas

    def tabelas(data, widlist):
        t = Table(data, colWidths=widlist, rowHeights=[10]*len(data))
    
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ])
        t.setStyle(style)
        return t
    
    canvas = canvas.Canvas('relatorio.pdf', pagesize=letter)
    canvas.setTitle('JK Control Report')

    canvas.setFillColorRGB(0, 0, 0)
    canvas.rect(35, 685, 540, 20, fill=True)
    canvas.rect(5, 605, 290, 15, fill=True)
    canvas.rect(318, 605, 290, 15, fill=True)
    canvas.rect(5, 345, 290, 15, fill=True)
    canvas.rect(318, 345, 290, 15, fill=True)
    
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont('Courier-Bold', 16)
    canvas.drawString(220, 689, 'Descrição Máquinas')
    canvas.setFont('Courier-Bold', 12)
    canvas.drawString(50, 609, 'Produção diária por máquina')
    canvas.drawString(370, 609, 'Produção Total por máquina')
    canvas.drawString(55, 349, 'Paradas diárias por máquina')
    canvas.drawString(375, 349, 'Paradas Totais por máquina')

    
    table_maq = tabelas(tab_maquinas, [80, 140, 100, 50, 70, 100])
    
    table_maq.wrapOn(canvas, 1, 1)
    table_maq.drawOn(canvas, 35, 650)
    
    logo_jk = 'images/jk_control.png'
    prod_diaria_maq = 'plots/Produção diária por máquina.png'
    prod_total_maq = 'plots/Produção total por máquina.png'
    parada_diaria = 'plots/Paradas diárias por máquina.png'
    parada_total = 'plots/Paradas totais por máquina.png'
    
    canvas.drawImage(logo_jk, 0, 712, 620, 80)
    canvas.drawImage(prod_diaria_maq, 0, 360, 300, 240)
    canvas.drawImage(prod_total_maq, 300, 360, 300, 240)
    canvas.drawImage(parada_diaria, 0, 80, 300, 240)
    canvas.drawImage(parada_total, 300, 80, 300, 240)
    

    
    
    
    canvas.save()

if __name__ == '__main__':
    build_pdf()