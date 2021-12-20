import argparse
from Bio import SeqIO
from evolucion_dirigida import EvolucionDirigida

def main():
    # Definimos los parámetros por terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", type=str, required=True, help="Secuencia fasta")
    parser.add_argument("--g", type=int, default=3, help="Número de generaciones")
    parser.add_argument("--p", type=float, default=0.97, help="Percentil a filtrar")
    parser.add_argument("--output", type=str, default=".", help="Ruta a exportar")

    # Obtenemos los parámetros ingresados por la terminal
    args = parser.parse_args()
    fasta = args.fasta.upper()
    g = args.g
    p = args.p
    output = args.output

    #Extraemos la secuencia
    handle = SeqIO.parse(fasta, "fasta")
    for record in handle:
        seq = str(record.seq)

    # Inicializamos la clase EvolucionDirigida
    evolucion_dirigida = EvolucionDirigida(seq=seq, g=g, p=p, output=output)
    evolucion_dirigida.main()

if __name__ == '__main__':
    main()