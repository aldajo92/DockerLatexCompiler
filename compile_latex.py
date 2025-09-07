#!/usr/bin/env python3
"""
Automatizador para compilación de documentos LaTeX
Uso: python compile_latex.py [directorio]
Ejemplo: python compile_latex.py clase01
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import time

class LaTeXCompiler:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        
    def find_main_tex(self, target_dir):
        """Busca el archivo main.tex en el directorio especificado"""
        tex_path = self.base_dir / target_dir / "main.tex"
        if tex_path.exists():
            return tex_path
        
        # Si no encuentra main.tex, busca cualquier archivo .tex
        tex_files = list((self.base_dir / target_dir).glob("*.tex"))
        if tex_files:
            print(f"⚠️  No se encontró main.tex, usando {tex_files[0].name}")
            return tex_files[0]
        
        return None
    
    def clean_aux_files(self, tex_file):
        """Limpia archivos auxiliares de compilaciones previas"""
        base_name = tex_file.stem
        aux_extensions = ['.aux', '.log', '.out', '.toc', '.fdb_latexmk', '.fls', '.synctex.gz']
        
        for ext in aux_extensions:
            aux_file = tex_file.parent / f"{base_name}{ext}"
            if aux_file.exists():
                aux_file.unlink()
                print(f"🧹 Eliminado: {aux_file.name}")
    
    def compile_latex(self, tex_file, clean_first=True, clean_after=True):
        """Compila el archivo LaTeX"""
        if clean_first:
            self.clean_aux_files(tex_file)
        
        print(f"📄 Compilando: {tex_file}")
        
        # Cambiar al directorio del archivo
        original_dir = Path.cwd()
        os.chdir(tex_file.parent)
        
        try:
            # Ejecutar pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file.name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Verificar si se generó el PDF
            pdf_file = tex_file.with_suffix('.pdf')
            
            if result.returncode == 0 and pdf_file.exists():
                print(f"✅ Compilación exitosa: {pdf_file}")
                print(f"📊 Tamaño del PDF: {pdf_file.stat().st_size:,} bytes")
                
                # Mostrar warnings si los hay
                if "Overfull" in result.stdout or "Underfull" in result.stdout:
                    print("⚠️  Hay algunos warnings de formato (no críticos)")
                
                # Limpiar archivos auxiliares después de compilación exitosa
                if clean_after:
                    self.clean_aux_files(tex_file)
                
                return True
            else:
                print(f"❌ Error en la compilación:")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    # Mostrar solo las líneas con errores
                    error_lines = [line for line in result.stdout.split('\n') 
                                 if '!' in line or 'Error' in line or 'Undefined' in line]
                    for line in error_lines[:5]:  # Mostrar máximo 5 errores
                        print(f"  {line}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout: La compilación tomó más de 60 segundos")
            return False
        except FileNotFoundError:
            print("❌ Error: pdflatex no está instalado o no está en el PATH")
            return False
        finally:
            os.chdir(original_dir)
    
    def watch_and_compile(self, tex_file, clean_after=True):
        """Modo watch: recompila automáticamente cuando el archivo cambia"""
        print(f"👀 Modo watch activado para {tex_file}")
        print("Presiona Ctrl+C para salir")
        
        last_modified = tex_file.stat().st_mtime
        
        try:
            while True:
                current_modified = tex_file.stat().st_mtime
                if current_modified > last_modified:
                    print(f"\n🔄 Archivo modificado, recompilando...")
                    self.compile_latex(tex_file, clean_first=False, clean_after=clean_after)
                    last_modified = current_modified
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Modo watch terminado")

def main():
    parser = argparse.ArgumentParser(description='Compilador automático de LaTeX')
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directorio que contiene el archivo LaTeX (default: directorio actual)')
    parser.add_argument('--clean', '-c', action='store_true',
                       help='Limpiar archivos auxiliares antes de compilar')
    parser.add_argument('--no-clean-after', action='store_true',
                       help='No limpiar archivos auxiliares después de compilar (por defecto sí se limpian)')
    parser.add_argument('--watch', '-w', action='store_true',
                       help='Modo watch: recompila automáticamente cuando el archivo cambia')
    
    args = parser.parse_args()
    
    compiler = LaTeXCompiler()
    
    # Buscar archivo LaTeX
    tex_file = compiler.find_main_tex(args.directory)
    
    if not tex_file:
        print(f"❌ No se encontró ningún archivo .tex en '{args.directory}'")
        sys.exit(1)
    
    if args.watch:
        # Compilar una vez primero
        compiler.compile_latex(tex_file, clean_first=args.clean, clean_after=not args.no_clean_after)
        # Luego entrar en modo watch
        compiler.watch_and_compile(tex_file, clean_after=not args.no_clean_after)
    else:
        # Compilación única
        success = compiler.compile_latex(tex_file, clean_first=args.clean, clean_after=not args.no_clean_after)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
