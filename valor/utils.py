from decimal import Decimal

_UNIDADES = ['zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez']


def valor_extenso(value):
    """Convert a 0-10 grade value to Portuguese words, e.g. 7 -> 'sete', 7.5 -> 'sete vírgula cinco'."""
    value = Decimal(value)
    inteiro = int(value)
    decimal = int((value - inteiro) * 10)

    palavra_inteiro = _UNIDADES[inteiro] if 0 <= inteiro <= 10 else str(inteiro)
    if decimal == 0:
        return palavra_inteiro
    palavra_decimal = _UNIDADES[decimal] if 0 <= decimal <= 9 else str(decimal)
    return f"{palavra_inteiro} vírgula {palavra_decimal}"
