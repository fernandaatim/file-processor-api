import pandas as pd
import io
import json
import chardet
import csv
from fastapi import UploadFile, HTTPException

REQUIRED_COLUMNS = ["id", "cliente", "valor"]

def detect_csv_params(contents: bytes) -> dict:
    content_detected = chardet.detect(contents)
    encoding = content_detected["encoding"] or "utf-8-sig"

    sample = contents.decode(encoding, errors="ignore")[:2048]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t"])
        sep = dialect.delimiter
    except csv.Error:
        sep = ","
    return {"encoding": encoding, "sep": sep}

FILE_READERS = {
    "csv": lambda contents: pd.read_csv(io.BytesIO(contents), **detect_csv_params(contents)),
    ("xls", "xlsx"): lambda contents: pd.read_excel(io.BytesIO(contents)),
    "json": lambda contents: pd.read_json(io.BytesIO(contents)),
    "parquet": lambda contents: pd.read_parquet(io.BytesIO(contents))
}

async def process_file(file: UploadFile, contents: bytes):
    try:
        extension = file.filename.rsplit(".", 1)[-1].lower()
        reader = FILE_READERS.get(extension)

        if not reader:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")
        
        df = reader(contents)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o arquivo: {str(e)}")
    
    
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Colunas faltantes: {', '.join(missing_columns)}")
    
    try:
        total = df["valor"].sum()
        negative_values = df[df["valor"] < 0].to_dict(orient="records")
        duplicate_values = df[df.duplicated()].to_dict(orient="records")

        output_filename = file.filename.rsplit(".", 1)[0] + "_processed.xlsx"
        df.to_excel(f"data/{output_filename}", index=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar os dados: {str(e)}")
    
    return {
        "total_value": float(total),
        "qtd_records": len(df),
        "negative_values": negative_values,
        "duplicate_values": duplicate_values
    }