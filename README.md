# SeqFactorScout
This tool analyzes FASTA sequences and uses JASPAR files to find and score potential transcription factor binding sites. It utilizes a graphical user interface (GUI) built with PySimpleGUI for ease of use.

**Note: This repository is still under construction!**
## Installation
### Step 1: Clone repository
    git clone https://github.com/aidanmeyers/SeqFactorScout.git
    cd SeqFactorScout
### Step 2: Set up virtual environment
    python -m venv SeqFactorScout
For simplicity, I've named the virtual environment "SeqFactorScout." You can name it whatever you would like, however.
### Step 3: Activate virtual environment
#### Windows
    .\SeqFactorScout\Scripts\activate
#### macOS/Linux
    source SeqFactorScout/bin/activate
### Step 4: Install requirements
    pip install -r requirements.txt
## Usage
### 1. Ensure virtual environment is activated
### 2. Run the tool
    python SeqFactorScout.py

## Inputs

## Algorithm Details

## Contributing

## License

## Additional information regarding PySimpleGUI licensing
**TL;DR: This tool's GUI was created using PySimpleGUI, which has a non-open source license. As a hobbyist developer, anyone using this application will see PySimpleGUI asking you to register to use their product. If you are using this tool for any non-commercial work, such as academic research, you will not have to pay for PySimpleGUI. You can either: 1) Use the 31-day trial and/or 2) Register as a hobbyist. If you use this tool for any commercial purpose, please register for a commercial license.**

The graphical user interface for this tool uses PySimpleGUI version 5.0.2. Please note that starting from version 5, PySimpleGUI transitioned from being completely open-source to having an open-source code but not an open-source license. Here are some key points about the PySimpleGUI license:

- Hobbyist Developers: If you are a Hobbyist Developer, you can use PySimpleGUI for non-commercial purposes at no cost. You will need to refresh your Hobbyist Developer License annually.

- Commercial Developers: If you are not a Hobbyist Developer, you are considered a Commercial Developer, and you or your company must purchase a perpetual license for $99, which includes one year of free upgrades and priority support.

"Hobbyist Developer" means any individual who uses PySimpleGUI for development purposes solely for either or both of the following: (1) personal (e.g., not on behalf of an employer or other third party), non-commercial purposes; or (2) non-commercial educational or learning purposes (together, the "Permitted No-cost Purposes"). "Commercial Developer" means any individual who uses PySimpleGUI for development purposes who is not a Hobbyist Developer.

For the sake of clarity, this licensing structure unequivocally qualifies me as a "Hobbyist Developer" under the PySimpleGUI license. I created this script in my free time, driven by a desire to simplify existing workflows for identifying transcription factor binding profiles. My primary intention was and always has been educational, both as an exercise in Python programming and as a means to facilitate the advancement of academic research. This project was entirely my own initiative, and although I am a student employee at UA, at no point was I directed by UA as an institution or any faculty member to undertake this work. From the project's inception, I have been committed to making this algorithm open source, firmly believing that there should be no financial or bureaucratic barriers to using this tool. Therefore, given these facts, I, as well as anyone else using this tool for non-commercial research, would be considered hobbyists.
