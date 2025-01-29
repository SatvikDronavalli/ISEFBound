import pandas as pd
from pathlib import Path
GRF_right_path = Path("Force_Data") / "GRF_F_V_PRO_right.csv"
GRF_left_path = Path("Force_Data") / "GRF_F_V_PRO_left.csv"
metadata_path = Path("Force_Data") / "GRF_metadata.csv"
GRF_right = pd.read_csv(GRF_right_path)
GRF_left = pd.read_csv(GRF_left_path)
metadata = pd.read_csv(metadata_path)
# average data if necessary instead of dropping duplicates
metadata = metadata.drop_duplicates(subset=["SUBJECT_ID"])
metadata = metadata[metadata["CLASS_LABEL"].isin(["HC","H"])]
metadata["at risk of falls"] = [None] * len(metadata)
metadata["at risk of falls"] = metadata["CLASS_LABEL"].apply(lambda x: 0 if x == "HC" else 1)
valid_IDs = metadata["SUBJECT_ID"].tolist()
# Deleting extra rows
GRF_right = GRF_right[GRF_right["SUBJECT_ID"].isin(valid_IDs)]
GRF_left = GRF_left[GRF_left["SUBJECT_ID"].isin(valid_IDs)]
# Merging 'at risk of falls' information to force data
GRF_right = GRF_right.merge(metadata[["SUBJECT_ID","at risk of falls"]], on="SUBJECT_ID", how="inner")
GRF_left = GRF_left.merge(metadata[["SUBJECT_ID","at risk of falls"]], on="SUBJECT_ID", how="inner")
GRF_right = GRF_right.merge(metadata[["SUBJECT_ID","TRAIN_BALANCED", "TEST","at risk of falls"]], on="SUBJECT_ID", how="inner")
GRF_left = GRF_left.merge(metadata[["SUBJECT_ID","TRAIN_BALANCED", "TEST", "at risk of falls"]], on="SUBJECT_ID", how="inner")
GRF_right_train = GRF_right[GRF_right["TRAIN_BALANCED"] == 1]
GRF_right_test = GRF_right[GRF_right["TEST"] == 1]
GRF_left_train = GRF_left[GRF_left["TRAIN_BALANCED"] == 1]
GRF_left_test = GRF_left[GRF_left["TEST"] == 1]
GRF_left_test.to_csv('testing.csv')
print(len(GRF_right_train),len(GRF_left_train),len(GRF_right_test),len(GRF_left_test))
# All desired subjects are in the GRF dataframes according to the checks below
#print(len(metadata[metadata["TRAIN_BALANCED"] == 1]), len(metadata[metadata["TRAIN_BALANCED"] == 0]))
#print(set(GRF_left["SUBJECT_ID"]) == set(metadata["SUBJECT_ID"]))
#print(set(GRF_right["SUBJECT_ID"]) == set(metadata["SUBJECT_ID"]))

