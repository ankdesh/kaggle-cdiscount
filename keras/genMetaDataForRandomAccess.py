import os, sys, math, io
import numpy as np
import pandas as pd
import multiprocessing as mp
import bson
import struct

from collections import defaultdict
from tqdm import *


def genCategoryCsv(data_dir):
  categories_path = os.path.join(data_dir, "category_names.csv")
  assert os.path.exists(categories_path), 'Cannot find path ' + categories_path
  
  categories_df = pd.read_csv(categories_path, index_col="category_id")
  
  # Maps the category_id to an integer index. This is what we'll use to
  # one-hot encode the labels.
  categories_df["category_idx"] = pd.Series(range(len(categories_df)), index=categories_df.index)
  return categories_df  

# Create dictionaries for quick lookup of `category_id` to `category_idx` mapping.
def make_category_tables():
    cat2idx = {}
    idx2cat = {}
    for ir in categories_df.itertuples():
        category_id = ir[0]
        category_idx = ir[4]
        cat2idx[category_id] = category_idx
        idx2cat[category_idx] = category_id
    return cat2idx, idx2cat

def read_bson(bson_path, num_records, with_categories):
    rows = {}
    with open(bson_path, "rb") as f, tqdm(total=num_records) as pbar:
        offset = 0
        while True:
            item_length_bytes = f.read(4)
            if len(item_length_bytes) == 0:
                break

            length = struct.unpack("<i", item_length_bytes)[0]

            f.seek(offset)
            item_data = f.read(length)
            assert len(item_data) == length

            item = bson.BSON(item_data).decode()
            product_id = item["_id"]
            num_imgs = len(item["imgs"])

            row = [num_imgs, offset, length]
            if with_categories:
                row += [item["category_id"]]
            rows[product_id] = row

            offset += length
            f.seek(offset)
            pbar.update()

    columns = ["num_imgs", "offset", "length"]
    if with_categories:
        columns += ["category_id"]

    df = pd.DataFrame.from_dict(rows, orient="index")
    df.index.name = "product_id"
    df.columns = columns
    df.sort_index(inplace=True)
    return df

if __name__=='__main__':  

  DATA_DIR = "../../dataset/"
  METADATA_DIR = 'metadata'
  
  train_bson_path = os.path.join(DATA_DIR, "train.bson")
  num_train_products = 7069896

  test_bson_path = os.path.join(DATA_DIR, "test.bson")
  num_test_products = 1768182
  
  # Dump category metada 
  if os.path.exists(os.path.join(METADATA_DIR, "categories.csv")):
    print (os.path.join(METADATA_DIR, "categories.csv") + ' exists. Skip generation of category file')
  else:
    categories_df = genCategoryCsv (DATA_DIR)
    categories_df.to_csv(os.path.join(METADATA_DIR, "categories.csv"))

  # Dump offset metadata -Train data
  if os.path.exists(os.path.join(METADATA_DIR,'train_offsets.csv')):
    print (train_bson_path + ' exists. Skip generation of Train metadata file')
  else:
    train_offsets_df = read_bson(train_bson_path, num_records=num_train_products, with_categories=True)
    print ('Dumping offsets to train_offsets.csv...')
    train_offsets_df.to_csv(os.path.join(METADATA_DIR,"train_offsets.csv"))
    # How many categories?
    print ('num_categories= ',len(train_offsets_df["category_id"].unique()))
    # How many images in total?
    print ('total num images Train= ', train_offsets_df["num_imgs"].sum())
 
  # FIXME NO CATEGORY field in test data file
  # Dump offset metadata -Test data
  #if os.path.exists(os.path.join(METADATA_DIR,'test_offsets.csv')):
  #  print (test_bson_path + ' exists. Skip generation of Train metadata file')
  #else:
  #  test_offsets_df = read_bson(test_bson_path, num_records=num_train_products, with_categories=True)
  #  print ('Dumping offsets to test_offsets.csv...')
  #  test_offsets_df.to_csv(os.path.join(METADATA_DIR,"test_offsets.csv"))
  #  # How many images in total?
  #  print ('total num images Test= ', test_offsets_df["num_imgs"].sum())
