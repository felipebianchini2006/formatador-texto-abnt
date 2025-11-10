#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formatador ABNT Desktop
Aplicativo para formatação automática de documentos conforme normas ABNT
Autor: Claude AI
Versão: 1.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
import os
from datetime import datetime


class FormatadorCitacoes:
    """Classe responsável por converter citações para o padrão ABNT NBR 10520:2023"""

    @staticmethod
    def converter_citacao_maiuscula_para_minuscula(texto):
        """
        Converte citações de SOBRENOME para Sobrenome (inicial maiúscula)
        Exemplos:
            (SILVA, 2022) -> (Silva, 2022)
            FREIRE (2021) -> Freire (2021)
            (SANTOS; OLIVEIRA, 2020) -> (Santos; Oliveira, 2020)
        """

        # Padrão 1: (SOBRENOME, ano) ou (SOBRENOME et al., ano)
        def substituir_parenteses(match):
            conteudo = match.group(1)
            # Processa cada autor separado por ponto e vírgula
            autores = conteudo.split(';')
            autores_formatados = []

            for autor in autores:
                autor = autor.strip()
                # Verifica se tem "et al."
                if 'ET AL' in autor.upper():
                    # Substitui ET AL por et al. (em itálico será feito no Word)
                    autor = re.sub(r'\bET\s+AL\.?', 'et al.', autor, flags=re.IGNORECASE)

                # Converte SOBRENOME para Sobrenome
                partes = autor.split(',')
                if len(partes) >= 1:
                    nome_parte = partes[0].strip()
                    # Converte cada palavra para capitalize
                    palavras = nome_parte.split()
                    palavras_formatadas = []
                    for palavra in palavras:
                        if palavra.upper() not in ['ET', 'AL', 'AL.']:
                            palavras_formatadas.append(palavra.capitalize())
                        else:
                            palavras_formatadas.append(palavra.lower())
                    partes[0] = ' '.join(palavras_formatadas)
                    autor = ', '.join(partes)

                autores_formatados.append(autor)

            return f"({'; '.join(autores_formatados)})"

        # Aplica conversão em citações entre parênteses
        texto = re.sub(r'\(([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ][A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ\s;,]+(?:et al\.)?[,\s]+\d{4}[a-z]?(?:\s*;\s*[A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ][A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ\s]+,\s*\d{4}[a-z]?)*(?:,\s*p\.\s*\d+(?:-\d+)?)?)\)',
                      substituir_parenteses, texto)

        # Padrão 2: SOBRENOME (ano) - autor no início da frase
        def substituir_inicio_frase(match):
            nome = match.group(1)
            resto = match.group(2)

            # Verifica se tem "et al."
            if 'ET AL' in nome.upper():
                nome = re.sub(r'\bET\s+AL\.?', 'et al.', nome, flags=re.IGNORECASE)

            palavras = nome.split()
            palavras_formatadas = []
            for palavra in palavras:
                if palavra.upper() not in ['ET', 'AL', 'AL.']:
                    palavras_formatadas.append(palavra.capitalize())
                else:
                    palavras_formatadas.append(palavra.lower())

            return f"{' '.join(palavras_formatadas)} {resto}"

        texto = re.sub(r'\b([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ]{2,}(?:\s+[A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ]{2,})*(?:\s+et\s+al\.?)?)\s+(\(\d{4}[a-z]?(?:,\s*p\.\s*\d+(?:-\d+)?)?\))',
                      substituir_inicio_frase, texto)

        return texto

    @staticmethod
    def converter_multiplos_autores_para_et_al(texto):
        """
        Converte citações com 4+ autores para et al.
        Exemplo: (Santos; Oliveira; Costa; Lima, 2020) -> (Santos et al., 2020)
        """
        def substituir(match):
            conteudo = match.group(1)
            # Conta quantos autores tem (separados por ponto e vírgula)
            autores = conteudo.split(';')

            # Se tem 4 ou mais autores, mantém apenas o primeiro + et al.
            if len(autores) >= 4:
                primeiro_autor = autores[0].strip()
                # Remove o ano do primeiro autor se existir
                primeiro_autor = re.sub(r',\s*\d{4}.*$', '', primeiro_autor).strip()
                # Pega o ano da citação original
                ano_match = re.search(r',\s*(\d{4}[a-z]?(?:,\s*p\.\s*\d+(?:-\d+)?)?)', conteudo)
                if ano_match:
                    ano = ano_match.group(1)
                    return f"({primeiro_autor} et al., {ano})"

            return match.group(0)

        texto = re.sub(r'\(([A-ZÀ-Ü][a-zà-ü]+(?:\s+[a-zà-ü]+)*(?:;\s*[A-ZÀ-Ü][a-zà-ü]+(?:\s+[a-zà-ü]+)*){3,}[,\s]+\d{4}[a-z]?(?:,\s*p\.\s*\d+(?:-\d+)?)?)\)',
                      substituir, texto)

        return texto

    @staticmethod
    def formatar_citacao_longa(texto):
        """
        Identifica citações longas (>3 linhas) e adiciona marcador para formatação especial
        O marcador será usado posteriormente na geração do Word
        """
        # Por enquanto, retorna o texto como está
        # A formatação real será feita no módulo de geração do Word
        return texto

    @staticmethod
    def formatar_texto(texto):
        """Aplica todas as conversões de citações no texto"""
        # 1. Converte SOBRENOME para Sobrenome
        texto = FormatadorCitacoes.converter_citacao_maiuscula_para_minuscula(texto)

        # 2. Converte múltiplos autores (4+) para et al.
        texto = FormatadorCitacoes.converter_multiplos_autores_para_et_al(texto)

        # 3. Identifica citações longas
        texto = FormatadorCitacoes.formatar_citacao_longa(texto)

        return texto


class FormatadorWord:
    """Classe responsável por aplicar formatação ABNT em documentos Word"""

    @staticmethod
    def criar_documento_formatado(texto):
        """
        Cria um documento Word com formatação ABNT completa:
        - Margens: 3cm (superior/esquerda), 2cm (inferior/direita)
        - Fonte: Arial 12
        - Espaçamento: 1,5
        - Alinhamento: Justificado
        """
        doc = Document()

        # Configurar margens (em Inches: 1 inch = 2.54 cm)
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(3 / 2.54)      # 3 cm
            section.bottom_margin = Inches(2 / 2.54)    # 2 cm
            section.left_margin = Inches(3 / 2.54)      # 3 cm
            section.right_margin = Inches(2 / 2.54)     # 2 cm

        # Processar o texto em parágrafos
        paragrafos = texto.split('\n')

        for texto_paragrafo in paragrafos:
            if texto_paragrafo.strip():
                # Detectar se é uma citação longa (heurística simples)
                eh_citacao_longa = FormatadorWord._eh_citacao_longa(texto_paragrafo)

                paragrafo = doc.add_paragraph(texto_paragrafo)

                if eh_citacao_longa:
                    # Formatação para citação longa
                    FormatadorWord._formatar_citacao_longa(paragrafo)
                else:
                    # Formatação padrão
                    FormatadorWord._formatar_paragrafo_padrao(paragrafo)
            else:
                # Parágrafo vazio (linha em branco)
                doc.add_paragraph()

        return doc

    @staticmethod
    def _eh_citacao_longa(texto):
        """
        Heurística para detectar citações longas:
        - Texto entre aspas
        - Mais de 300 caracteres (aproximadamente 3 linhas)
        """
        # Remove espaços para contagem mais precisa
        texto_limpo = texto.strip()

        # Verifica se está entre aspas e tem mais de 300 caracteres
        if (texto_limpo.startswith('"') or texto_limpo.startswith('"')) and len(texto_limpo) > 300:
            return True

        # Verifica se tem indicação de página (comum em citações longas)
        if re.search(r'\([A-ZÀ-Ü][a-zà-ü]+.*?,\s*\d{4},\s*p\.\s*\d+', texto_limpo) and len(texto_limpo) > 300:
            return True

        return False

    @staticmethod
    def _formatar_paragrafo_padrao(paragrafo):
        """Aplica formatação ABNT padrão ao parágrafo"""
        # Alinhamento justificado
        paragrafo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Formato do parágrafo
        paragrafo_format = paragrafo.paragraph_format
        paragrafo_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE  # 1,5
        paragrafo_format.space_after = Pt(0)
        paragrafo_format.space_before = Pt(0)

        # Fonte Arial 12
        for run in paragrafo.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(12)

            # Formatar "et al." em itálico
            if 'et al.' in run.text:
                texto = run.text
                # Divide e reformata
                partes = texto.split('et al.')
                run.text = partes[0]

                for i in range(1, len(partes)):
                    # Adiciona "et al." em itálico
                    run_italic = paragrafo.add_run('et al.')
                    run_italic.italic = True
                    run_italic.font.name = 'Arial'
                    run_italic.font.size = Pt(12)

                    # Adiciona o resto do texto
                    if partes[i]:
                        run_normal = paragrafo.add_run(partes[i])
                        run_normal.font.name = 'Arial'
                        run_normal.font.size = Pt(12)

    @staticmethod
    def _formatar_citacao_longa(paragrafo):
        """Aplica formatação ABNT para citações longas (>3 linhas)"""
        # Alinhamento justificado
        paragrafo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Formato do parágrafo
        paragrafo_format = paragrafo.paragraph_format
        paragrafo_format.line_spacing_rule = WD_LINE_SPACING.SINGLE  # Espaçamento simples
        paragrafo_format.left_indent = Inches(4 / 2.54)  # Recuo de 4 cm
        paragrafo_format.space_after = Pt(0)
        paragrafo_format.space_before = Pt(0)

        # Fonte Arial 10
        for run in paragrafo.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(10)

            # Remove aspas se existirem
            run.text = run.text.strip('"').strip('"').strip('"')

    @staticmethod
    def carregar_documento(caminho_arquivo):
        """Carrega um documento Word e retorna seu texto"""
        try:
            doc = Document(caminho_arquivo)
            texto_completo = []

            for paragrafo in doc.paragraphs:
                texto_completo.append(paragrafo.text)

            return '\n'.join(texto_completo)
        except Exception as e:
            raise Exception(f"Erro ao carregar documento: {str(e)}")

    @staticmethod
    def salvar_documento(doc, caminho_arquivo):
        """Salva o documento Word formatado"""
        try:
            doc.save(caminho_arquivo)
            return True
        except Exception as e:
            raise Exception(f"Erro ao salvar documento: {str(e)}")


class AplicativoFormatadorABNT:
    """Aplicativo principal com interface Tkinter"""

    def __init__(self, root):
        self.root = root
        self.root.title("📄 Formatador ABNT - Documentos")
        self.root.geometry("1200x700")

        # Variáveis
        self.texto_original = ""
        self.texto_formatado = ""

        # Configurar interface
        self._criar_interface()

    def _criar_interface(self):
        """Cria a interface gráfica completa"""

        # Frame superior - Botões de ação
        frame_botoes = ttk.Frame(self.root, padding="10")
        frame_botoes.pack(fill=tk.X)

        btn_carregar_word = ttk.Button(frame_botoes, text="📂 Carregar Word",
                                       command=self.carregar_word)
        btn_carregar_word.pack(side=tk.LEFT, padx=5)

        btn_inserir_texto = ttk.Button(frame_botoes, text="📝 Inserir Texto",
                                       command=self.inserir_texto)
        btn_inserir_texto.pack(side=tk.LEFT, padx=5)

        btn_formatar = ttk.Button(frame_botoes, text="✨ Formatar ABNT",
                                 command=self.formatar_texto,
                                 style='Accent.TButton')
        btn_formatar.pack(side=tk.LEFT, padx=5)

        btn_salvar = ttk.Button(frame_botoes, text="💾 Salvar Word",
                               command=self.salvar_word)
        btn_salvar.pack(side=tk.LEFT, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="🗑️ Limpar",
                               command=self.limpar_tudo)
        btn_limpar.pack(side=tk.LEFT, padx=5)

        # Separador
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Frame principal - Duas colunas
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Coluna ANTES (Esquerda)
        frame_antes = ttk.LabelFrame(frame_principal, text="📄 ANTES (Original)",
                                     padding="10")
        frame_antes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.texto_antes = scrolledtext.ScrolledText(frame_antes, wrap=tk.WORD,
                                                     font=("Arial", 10),
                                                     height=20)
        self.texto_antes.pack(fill=tk.BOTH, expand=True)

        btn_copiar_antes = ttk.Button(frame_antes, text="📋 Copiar Original",
                                     command=self.copiar_original)
        btn_copiar_antes.pack(pady=(5, 0))

        # Coluna DEPOIS (Direita)
        frame_depois = ttk.LabelFrame(frame_principal, text="✅ DEPOIS (Formatado ABNT)",
                                      padding="10")
        frame_depois.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.texto_depois = scrolledtext.ScrolledText(frame_depois, wrap=tk.WORD,
                                                      font=("Arial", 10),
                                                      height=20)
        self.texto_depois.pack(fill=tk.BOTH, expand=True)

        btn_copiar_depois = ttk.Button(frame_depois, text="📋 Copiar Formatado",
                                      command=self.copiar_formatado)
        btn_copiar_depois.pack(pady=(5, 0))

        # Barra de status
        self.status_bar = ttk.Label(self.root, text="Pronto para formatar documentos",
                                   relief=tk.SUNKEN, anchor=tk.W, padding="5")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def carregar_word(self):
        """Carrega um arquivo Word (.docx)"""
        try:
            caminho = filedialog.askopenfilename(
                title="Selecionar arquivo Word",
                filetypes=[("Documentos Word", "*.docx"), ("Todos os arquivos", "*.*")]
            )

            if caminho:
                self.atualizar_status("Carregando documento...")
                texto = FormatadorWord.carregar_documento(caminho)
                self.texto_original = texto

                # Exibir no campo ANTES
                self.texto_antes.delete(1.0, tk.END)
                self.texto_antes.insert(1.0, texto)

                # Limpar campo DEPOIS
                self.texto_depois.delete(1.0, tk.END)

                self.atualizar_status(f"✅ Documento carregado: {os.path.basename(caminho)}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar documento:\n{str(e)}")
            self.atualizar_status("❌ Erro ao carregar documento")

    def inserir_texto(self):
        """Permite inserir/editar texto diretamente no campo ANTES"""
        # Limpa o campo DEPOIS
        self.texto_depois.delete(1.0, tk.END)

        # Foca no campo ANTES para edição
        self.texto_antes.focus()

        self.atualizar_status("Digite ou cole o texto no campo 'ANTES' e clique em 'Formatar ABNT'")

    def formatar_texto(self):
        """Aplica formatação ABNT ao texto"""
        try:
            # Pega o texto do campo ANTES
            texto_original = self.texto_antes.get(1.0, tk.END).strip()

            if not texto_original:
                messagebox.showwarning("Aviso", "Nenhum texto para formatar!\n\nCarregue um documento ou insira texto primeiro.")
                return

            self.atualizar_status("Formatando texto conforme normas ABNT...")

            # Aplica formatação de citações
            texto_formatado = FormatadorCitacoes.formatar_texto(texto_original)

            self.texto_formatado = texto_formatado

            # Exibir no campo DEPOIS
            self.texto_depois.delete(1.0, tk.END)
            self.texto_depois.insert(1.0, texto_formatado)

            self.atualizar_status("✅ Documento formatado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao formatar texto:\n{str(e)}")
            self.atualizar_status("❌ Erro na formatação")

    def copiar_original(self):
        """Copia o texto original para a área de transferência"""
        texto = self.texto_antes.get(1.0, tk.END).strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.atualizar_status("📋 Texto original copiado!")
        else:
            messagebox.showinfo("Aviso", "Nenhum texto para copiar")

    def copiar_formatado(self):
        """Copia o texto formatado para a área de transferência"""
        texto = self.texto_depois.get(1.0, tk.END).strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.atualizar_status("📋 Texto formatado copiado!")
        else:
            messagebox.showinfo("Aviso", "Nenhum texto formatado para copiar.\n\nClique em 'Formatar ABNT' primeiro.")

    def salvar_word(self):
        """Salva o documento formatado como .docx"""
        try:
            texto = self.texto_depois.get(1.0, tk.END).strip()

            if not texto:
                messagebox.showwarning("Aviso", "Nenhum texto formatado para salvar!\n\nClique em 'Formatar ABNT' primeiro.")
                return

            # Diálogo para escolher onde salvar
            caminho = filedialog.asksaveasfilename(
                title="Salvar documento formatado",
                defaultextension=".docx",
                filetypes=[("Documento Word", "*.docx"), ("Todos os arquivos", "*.*")],
                initialfile=f"documento_abnt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            )

            if caminho:
                self.atualizar_status("Salvando documento formatado...")

                # Criar documento com formatação ABNT completa
                doc = FormatadorWord.criar_documento_formatado(texto)

                # Salvar
                FormatadorWord.salvar_documento(doc, caminho)

                self.atualizar_status(f"✅ Documento salvo: {os.path.basename(caminho)}")
                messagebox.showinfo("Sucesso", f"Documento salvo com sucesso!\n\n{caminho}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar documento:\n{str(e)}")
            self.atualizar_status("❌ Erro ao salvar documento")

    def limpar_tudo(self):
        """Limpa todos os campos"""
        self.texto_antes.delete(1.0, tk.END)
        self.texto_depois.delete(1.0, tk.END)
        self.texto_original = ""
        self.texto_formatado = ""
        self.atualizar_status("Campos limpos. Pronto para novo documento.")

    def atualizar_status(self, mensagem):
        """Atualiza a barra de status"""
        self.status_bar.config(text=mensagem)
        self.root.update_idletasks()


def main():
    """Função principal para executar o aplicativo"""
    root = tk.Tk()
    app = AplicativoFormatadorABNT(root)
    root.mainloop()


if __name__ == "__main__":
    main()
