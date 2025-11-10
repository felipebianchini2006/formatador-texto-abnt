#!/bin/bash
# Script de execução do Formatador ABNT para Linux/Mac
# Este script verifica se as dependências estão instaladas e executa o aplicativo

echo "========================================"
echo "  FORMATADOR ABNT - Desktop"
echo "========================================"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo ""
    echo "Por favor, instale Python 3.7 ou superior:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "  Fedora: sudo dnf install python3 python3-pip python3-tkinter"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

echo "[OK] Python encontrado: $(python3 --version)"
echo ""

# Verifica se as dependências estão instaladas
echo "Verificando dependências..."
python3 -c "import docx" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Instalando dependências necessárias..."
    echo ""

    # Tenta instalar com pip3
    pip3 install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao instalar dependências!"
        echo ""
        echo "Tente instalar manualmente:"
        echo "  pip3 install python-docx"
        echo ""
        exit 1
    fi

    echo ""
    echo "[OK] Dependências instaladas com sucesso!"
else
    echo "[OK] Dependências já instaladas"
fi

echo ""
echo "Iniciando Formatador ABNT..."
echo ""

# Executa o aplicativo
python3 formatador_abnt.py

# Verifica se houve erro na execução
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERRO] Ocorreu um erro ao executar o aplicativo"
    echo ""
    exit 1
fi
