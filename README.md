# SeqFactorScout

SeqFactorScout is a simple Python script for analyzing FASTA sequences to identify transcription factor binding sites using JASPAR position frequency matrices. Works well for genome-scale analysis, it scans sequences on both strands, scores potential binding sites against a motif's position-specific scoring matrix, and writes the results to an Excel file.

## Installation

### Step 1: Clone the repository

```
git clone https://github.com/aidanmeyers/SeqFactorScout.git
cd SeqFactorScout
```

### Step 2: Set up a virtual environment

```
python -m venv venv
```

### Step 3: Activate the virtual environment

**Windows**

```
.\venv\Scripts\activate
```

**macOS/Linux**

```
source venv/bin/activate
```

### Step 4: Install requirements

```
pip install -r requirements.txt
```

## Usage

SeqFactorScout is run from the command line:

```
python seqfactor.py <jaspar_file> <fasta_file> <output_file> [options]
```

### Example

```
python seqfactor.py atfs-1.jaspar glycolysis.fasta results.xlsx -t 80 -r upstream
```

### Arguments

| Argument | Description |
| --- | --- |
| `jaspar_file` | Path to the JASPAR motif file (PFM). |
| `fasta_file` | Path to the input FASTA file. |
| `output_file` | Path to the output `.xlsx` file (the extension is added automatically if omitted). |

### Options

| Option | Description |
| --- | --- |
| `-t`, `--threshold` | Minimum score threshold as a percentage of the motif's maximum possible score (0–100). Higher is more stringent. Default: `75`. |
| `-r`, `--region` | Region context for position reporting: `upstream`, `downstream`, or `other`. Default: `upstream`. |

## Inputs

### JASPAR file

The JASPAR file stores a transcription factor binding profile as a position frequency matrix, which SeqFactorScout uses to find and score potential binding sites. Profiles can be downloaded from the [JASPAR database](https://jaspar.elixir.no/). To learn more about the format, see the [JASPAR documentation](https://jaspar.elixir.no/docs/#jaspar-format).

### FASTA file

A standard FASTA file of the sequences to scan. Headers are expected in the form:

```
>gene-name|transcript-id
```

For example, `>gpd-2|K10B3.8.1` is parsed as gene `gpd-2`, transcript `K10B3.8.1`.

## Output

The tool writes an Excel (`.xlsx`) file with one row per match, including the transcript and gene IDs, start and end positions, the matched sequence, its raw score, the maximum possible score, the percentage of maximum, and the strand (direct or reverse).

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
