class BIO_Processor:
    
    base = (16, 4, 1)
    nucleotides = {
        "A": 0, "G": 1, "C": 2, "T": 3
    }

    # can be use to transform from codon to protein 
    codon_table = {
        # Fenilalanina
        "TTT": "F", "TTC": "F",
        # Leucina
        "TTA": "L", "TTG": "L",
        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
        # Isoleucina
        "ATT": "I", "ATC": "I", "ATA": "I",
        # Metionina (Start)
        "ATG": "M",
        # Valina
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        # Serina
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
        "AGT": "S", "AGC": "S",
        # Prolina
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        # Treonina
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        # Alanina
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        # Tirosina
        "TAT": "Y", "TAC": "Y",
        # Histidina
        "CAT": "H", "CAC": "H",
        # Glutamina
        "CAA": "Q", "CAG": "Q",
        # Asparagina
        "AAT": "N", "AAC": "N",
        # Lisina
        "AAA": "K", "AAG": "K",
        # Ácido Aspártico
        "GAT": "D", "GAC": "D",
        # Ácido Glutâmico
        "GAA": "E", "GAG": "E",
        # Cisteína
        "TGT": "C", "TGC": "C",
        # Triptofano
        "TGG": "W",
        # Arginina
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "AGA": "R", "AGG": "R",
        # Glicina
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        # Codons de parada
        "TAA": "*", "TAG": "*", "TGA": "*"
    }

    @staticmethod
    def nucleotide_list_to_protein(nucleotide_list: list[str]) -> str:
        try:
            if len(nucleotide_list) % 3 != 0:
                raise ValueError("Size list must be multiple of 3")
            
            
            protein = []

            for start in range(0, len(nucleotide_list), 3):
                codon = ''.join(nucleotide_list[start:start+3])
                if codon in BIO_Processor.codon_table:
                    protein.append(BIO_Processor.codon_table[codon])
            return "".join(protein)

        except Exception as e:
            raise e


    


    @staticmethod
    def nucleotideToCodon(tripleNucleotides:str)->int:

        codonNumber = 0

        for p in range(3):
            char = tripleNucleotides[p]

            if char in BIO_Processor.nucleotides:
                codonNumber += BIO_Processor.base[p] * BIO_Processor.nucleotides[char]
                continue

            if char == "-":
                codonNumber = 64      # gap
            elif char in ("n", "N"):
                codonNumber = 65      # unknown nucleotide
            else:
                codonNumber = 66      # IUPAC ambiguous
            break

        return codonNumber

    @staticmethod
    def nucleotideSequenceToCodons(sequence):
        triples = (sequence[i:i+3] for i in range(0, len(sequence), 3))
        return [BIO_Processor.nucleotideToCodon(triple) for triple in triples]