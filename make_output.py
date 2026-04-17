import glob
import os
import pandas as pd

DATA_DIR = "data"
OUT_PATH = os.path.join(DATA_DIR, "pink_morsels_sales.csv")

def main():
    csv_paths = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in {DATA_DIR}/")

    frames = []
    for path in csv_paths:
        df = pd.read_csv(path)

    
        df.columns = [c.strip().lower() for c in df.columns]


        required = {"product", "quantity", "price", "date", "region"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{path} is missing columns: {sorted(missing)}")

  
        df = df[df["product"] == "Pink Morsels"].copy()

        
        df["sales"] = df["quantity"] * df["price"]

        
        df = df[["sales", "date", "region"]].copy()
        df.columns = ["Sales", "Date", "Region"]

        frames.append(df)

    out = pd.concat(frames, ignore_index=True)

  
    out = out.sort_values(["Date", "Region"], kind="stable").reset_index(drop=True)

    out.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(out)} rows to {OUT_PATH}")

if __name__ == "__main__":
    main()