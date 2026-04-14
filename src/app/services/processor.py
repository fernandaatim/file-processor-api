import pandas as pd
import io
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

async def process_file(file: UploadFile, contents: bytes):
    try:
        if file.filename.endswith(".csv"):
            params = detect_csv_params(contents)
            df = pd.read_csv(io.BytesIO(contents), **params)
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")
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