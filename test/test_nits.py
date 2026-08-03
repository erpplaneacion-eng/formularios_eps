"""Valida el digito de verificacion de cada NIT en NITS_EMPRESAS.

Un digito de mas o un typo produce PDFs oficiales con NIT invalido.
Ejecutar: python test/test_nits.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'formularios'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formularios.settings')

import django
django.setup()

from formatos_eps.pdf_generator import NITS_EMPRESAS

PESOS = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]


def digito_verificacion(nit):
    suma = sum(int(d) * PESOS[i] for i, d in enumerate(reversed(nit)))
    resto = suma % 11
    return 0 if resto < 2 else 11 - resto


def main():
    errores = []
    for empresa, completo in NITS_EMPRESAS.items():
        base, _, dv = completo.replace('.', '').partition('-')
        if not base.isdigit() or len(base) != 9:
            errores.append(f"{empresa}: '{completo}' no tiene 9 digitos base")
        elif str(digito_verificacion(base)) != dv:
            errores.append(
                f"{empresa}: '{completo}' DV incorrecto (esperado {digito_verificacion(base)})"
            )

    assert not errores, "NITs invalidos:\n  " + "\n  ".join(errores)
    print(f"OK: {len(NITS_EMPRESAS)} NITs validos")


if __name__ == '__main__':
    main()
