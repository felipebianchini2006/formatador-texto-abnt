#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização simplificado para o Formatador ABNT v3.0
Verifica e instala dependências automaticamente
"""

import sys
import subprocess
import os

def print_banner():
    print("=" * 60)
    print("  📄 FORMATADOR ABNT ACADÊMICO v3.0")
    print("=" * 60)
    print()

def check_and_install_dependencies():
    """Verifica e instala dependências necessárias"""
    dependencies = {
        'customtkinter': 'customtkinter',
        'docx': 'python-docx',
        'PIL': 'Pillow',
        'packaging': 'packaging'
    }

    missing = []

    print("🔍 Verificando dependências...")

    for module, package in dependencies.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"📥 Instalando dependências: {', '.join(missing)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--quiet'
            ] + missing)
            print("✅ Dependências instaladas com sucesso!")
        except subprocess.CalledProcessError:
            print("❌ ERRO: Não foi possível instalar as dependências.")
            print()
            print("💡 Tente manualmente:")
            print(f"   pip install {' '.join(missing)}")
            print()
            return False
    else:
        print("✅ Todas as dependências já estão instaladas!")

    print()
    return True

def check_tkinter():
    """Verifica se tkinter está instalado"""
    try:
        import tkinter
        return True
    except ImportError:
        print("❌ ERRO: tkinter não encontrado!")
        print()
        print("💡 Instale o tkinter:")
        print("   Ubuntu/Debian: sudo apt install python3-tk")
        print("   Fedora: sudo dnf install python3-tkinter")
        print()
        return False

def main():
    print_banner()

    # Verifica tkinter
    if not check_tkinter():
        sys.exit(1)

    # Verifica e instala dependências
    if not check_and_install_dependencies():
        sys.exit(1)

    print("🚀 Iniciando Formatador ABNT v3.0...")
    print()

    # Importa e executa o aplicativo
    try:
        # Adiciona o diretório atual ao path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Importa o aplicativo
        from formatador_abnt_moderno import main as app_main

        # Executa
        app_main()

    except ImportError as e:
        print(f"❌ ERRO ao importar o aplicativo: {e}")
        print()
        print("💡 Verifique se o arquivo 'formatador_abnt_moderno.py' existe.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERRO ao executar o aplicativo: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
