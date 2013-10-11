# Scantobuy QR-Code Generator
Tool to print QR-Codes from CSV.

Needs an file named code_list.csv, that includes data for QR-codes.
Also a file with the logo for labelbag, named scantobuy_logo_no_qr.jpg.

## Install
Just install packages with

```bash
git clone git@github.com:scantobuy/qr-code-generator.git
cd qr-code-generator/
mkdir qr-code-labelbags qr-code-labelbags-small qr-codes
pip install -r requirements.txt
```

## Run

```bash
python generate_scantobuy_codes.py
```
