#!/bin/bash
# Script de execução do Formatador ABNT v3.0

echo "================================================"
echo "  📄 FORMATADOR ABNT v3.0"
echo "================================================"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo ""
    echo "Instale o Python:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk python3-venv"
    echo "  Fedora: sudo dnf install python3 python3-pip python3-tkinter"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv

    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual."
        echo "Instale: sudo apt install python3-venv"
        exit 1
    fi

    echo "✅ Ambiente virtual criado!"
fi

# Ativa o ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source .venv/bin/activate

# Verifica dependências
echo "🔍 Verificando dependências..."
python -c "import customtkinter, docx, packaging" &> /dev/null

if [ $? -ne 0 ]; then
    echo "📥 Instalando dependências..."
    pip install -q -r requirements.txt

    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências."
        echo ""
        echo "Tente manualmente:"
        echo "  source .venv/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi

    echo "✅ Dependências instaladas!"
fi

echo "✅ Tudo pronto!"
echo ""
echo "🚀 Abrindo Formatador ABNT..."
echo ""

# Executa o aplicativo
python formatador_abnt_moderno.py

# Verifica erro
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao executar o aplicativo."
    echo ""
    echo "💡 Tente:"
    echo "  sudo apt install python3-tk"
    echo "  python3 iniciar.py"
    exit 1
fi
