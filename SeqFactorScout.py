import PySimpleGUI as sg
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

def main(jaspar_file, fasta_file, output_file, threshold_percentage, choice, window):
    with open(jaspar_file) as f:
        motif = motifs.read(f, "jaspar")
    
    pssm = motif.counts.normalize(pseudocounts=0.5).log_odds()
    dfs = []

    records = list(SeqIO.parse(fasta_file, "fasta")) 
    total_records = len(records)
    
    for idx, record in enumerate(records):
        window['progress'].update_bar(idx + 1, total_records)
        seq_length = len(record.seq)
        header_parts = record.description.split(';')
        transcript_id = header_parts[0].split('=')[1]  
        gene_id = header_parts[1].split('=')[1]  

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
    
    result_df = pd.concat(dfs, ignore_index=True)
    result_df.to_excel(output_file, index=False)

region_choice_map = {
    'upstream region': 1,
    'downstream region': 2,
    'other': 3
}

if __name__ == "__main__":
    sg.theme('LightGreen')

    layout = [
        [sg.Text('JASPAR File', size=(15, 1)), sg.InputText(size=(40, 1), key='jaspar_file'), sg.FileBrowse()],
        [sg.Text('FASTA File', size=(15, 1)), sg.InputText(size=(40, 1), key='fasta_file'), sg.FileBrowse()],
        [sg.Text('Output File Name', size=(15, 1)), sg.InputText(size=(40, 1), key='file_name')],
        [sg.Text('Output Folder', size=(15, 1)), sg.InputText(size=(40, 1), key='folder_path'), sg.FolderBrowse('Browse')],
        [sg.Text('Minimum Threshold (%)', size=(18, 1))],
        [sg.Slider(range=(0, 100), orientation='h', size=(52, 20), default_value=75, tooltip='Set Minimum Threshold Percentage', key='threshold_slider')],
        [sg.Text('Region Choice', size=(15, 1)), sg.Combo(['upstream region', 'downstream region', 'other'], default_value='upstream region', size=(40, 1), readonly=True, key='region_choice')],
        [sg.Submit(), sg.Cancel()],
        [sg.Text('Progress:', size=(8, 1)), sg.ProgressBar(1000, orientation='h', size=(52, 20), key='progress')]
    ]
 
    window = sg.Window('Sequence TFBS Algorithm', layout)

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Cancel'):
            break
        if event == 'Submit':
            jaspar_file = values['jaspar_file']
            fasta_file = values['fasta_file']
            file_name = values['file_name'] + '.xlsx'  
            folder_path = values['folder_path']
            output_file = os.path.join(folder_path, file_name)
            threshold_percentage = values['threshold_slider']
            region_choice_str = values['region_choice'] 
            choice = region_choice_map[region_choice_str]  

            try:
                threshold_percentage = float(threshold_percentage)
                window.perform_long_operation(lambda: main(jaspar_file, fasta_file, output_file, threshold_percentage, choice, window), '-END-')
            except Exception as e:
                sg.popup('Error', 'An error occurred:', str(e))

        if event == '-END-':
            sg.popup('Success', 'The analysis has been completed successfully!')

    window.close()
