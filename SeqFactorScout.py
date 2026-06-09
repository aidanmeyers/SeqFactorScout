import argparse
import os
import pandas as pd
from Bio import motifs, SeqIO
from Bio.Seq import Seq

def format_position(pos, choice, seq_length):
    if choice == 1:
        return f"-{seq_length - pos}"
    elif choice == 2:
        return f"+{abs(pos)}"
    else:
        return str(abs(pos))

def search_pwm(sequence, pwm, threshold_percentage):
    max_score = pwm.max
    threshold = max_score * threshold_percentage / 100

    for start in range(len(sequence) - pwm.length + 1):
        subseq = sequence[start:start+pwm.length]
        score = pwm.calculate(subseq)
        if score > threshold:
            yield start, score

def main(jaspar_file, fasta_file, output_file, threshold_percentage, choice):
    with open(jaspar_file) as f:
        motif = motifs.read(f, "jaspar")

    pssm = motif.counts.normalize(pseudocounts=0.5).log_odds()
    dfs = []

    records = list(SeqIO.parse(fasta_file, "fasta"))
    total_records = len(records)

    for idx, record in enumerate(records):
        print(f"Processing record {idx + 1} of {total_records}", end='\r')
        seq_length = len(record.seq)
        header_parts = record.description.split('|')
        gene_id = header_parts[0]
        transcript_id = header_parts[1] if len(header_parts) > 1 else header_parts[0]

        for strand, sequence in [("direct", record.seq), ("reverse", record.seq.reverse_complement())]:
            matches = []
            for pos, score in search_pwm(sequence, pssm, threshold_percentage):
                start = format_position(pos, choice, seq_length)
                end = format_position(pos + motif.length - 1, choice, seq_length)
                percentage_max = (score/pssm.max) * 100
                matches.append((transcript_id, gene_id, start, end, sequence[pos:pos+motif.length], score, pssm.max, percentage_max, strand))

            if matches:
                df = pd.DataFrame(matches, columns=['Transcript ID', 'Gene ID', 'Start', 'End', 'TFBS Sequence', 'Score', 'Max Possible Score', 'Percentage of Maximum Possible Score', 'Direction'])
                dfs.append(df)

    print()  # newline after progress

    if not dfs:
        print("No matches found above the threshold.")
        return

    result_df = pd.concat(dfs, ignore_index=True)
    result_df.to_excel(output_file, index=False)
    print(f"The analysis has been completed successfully! Output written to: {output_file}")

region_choice_map = {
    'upstream': 1,
    'downstream': 2,
    'other': 3
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sequence TFBS Algorithm')
    parser.add_argument('jaspar_file', help='Path to the JASPAR motif file')
    parser.add_argument('fasta_file', help='Path to the FASTA file')
    parser.add_argument('output_file', help='Output .xlsx file path')
    parser.add_argument('-t', '--threshold', type=float, default=75.0,
                        help='Minimum threshold percentage (0-100, default: 75)')
    parser.add_argument('-r', '--region', choices=['upstream', 'downstream', 'other'],
                        default='upstream', help='Region choice (default: upstream)')

    args = parser.parse_args()

    output_file = args.output_file
    if not output_file.lower().endswith('.xlsx'):
        output_file += '.xlsx'

    choice = region_choice_map[args.region]

    main(args.jaspar_file, args.fasta_file, output_file, args.threshold, choice)
