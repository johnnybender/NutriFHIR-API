import hei_loader
import pandas as pd

# run the program that writes the upc->hei file
if __name__ == '__main__':
    output = hei_loader.get_unique_upc_df()
    output.to_csv("./data/output_hei_scores.csv", index=False)
    print("successfully wrote output file to data folder")
