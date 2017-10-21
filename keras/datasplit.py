import os, sys, math, io
import numpy as np
import pandas as pd

from collections import defaultdict
from tqdm import *
import click

def make_category_tables(categories_df):
  cat2idx = {}
  idx2cat = {}
  for ir in categories_df.itertuples():
      category_id = ir[0]
      category_idx = ir[4]
      cat2idx[category_id] = category_idx
      idx2cat[category_idx] = category_id
  return cat2idx, idx2cat

def dataSplitRandomDrop(df, cat2idx, split_percentage=0.2, drop_percentage=0.):

  # Find the product_ids for each category.
  category_dict = defaultdict(list)
  for ir in tqdm(df.itertuples()):
      category_dict[ir[4]].append(ir[0])

  train_list = []
  val_list = []
  with tqdm(total=len(df)) as pbar:
      for category_id, product_ids in category_dict.items():
          category_idx = cat2idx[category_id]

          # Randomly remove products to make the dataset smaller.
          keep_size = int(len(product_ids) * (1. - drop_percentage))
          if keep_size < len(product_ids):
              product_ids = np.random.choice(product_ids, keep_size, replace=False)

          # Randomly choose the products that become part of the validation set.
          val_size = int(len(product_ids) * split_percentage)
          if val_size > 0:
              val_ids = np.random.choice(product_ids, val_size, replace=False)
          else:
              val_ids = []

          # Create a new row for each image.
          for product_id in product_ids:
              row = [product_id, category_idx]
              for img_idx in range(df.loc[product_id, "num_imgs"]):
                  if product_id in val_ids:
                      val_list.append(row + [img_idx])
                  else:
                      train_list.append(row + [img_idx])
              pbar.update()
              
  columns = ["product_id", "category_idx", "img_idx"]
  train_df = pd.DataFrame(train_list, columns=columns)
  val_df = pd.DataFrame(val_list, columns=columns)   
  return train_df, val_df

@click.command()
@click.option('--policy', default='RandomSplit', help='Policy to use for data split Options are - RandomSplit, ')
@click.option('--drop_percentage', default=0.9, help='Percentage of data to drop for Random drop policy')
@click.option('--split_percentage', default=0.2, help='Percentage of Validation set for Random drop policy')
def main(policy, drop_percentage, split_percentage):
  METADATA_DIR = 'metadata'
  
  categories_df = pd.read_csv(os.path.join(METADATA_DIR,"categories.csv"), index_col=0)
  cat2idx, idx2cat = make_category_tables(categories_df)

  if policy == 'RandomSplit':
    train_img_filename = 'RandomSplit_Train_' + str(drop_percentage) + '_' + str(split_percentage) + '.csv'
    val_img_filename = 'RandomSplit_Val_' + str(drop_percentage) + '_' + str(split_percentage) + '.csv'

    if os.path.exists(os.path.join(METADATA_DIR, train_img_filename)) and \
       os.path.exists(os.path.join(METADATA_DIR, val_img_filename)):
      print (train_img_filename + ' and ' + val_img_filename + 'exists. Skipping..')
      
    else:
      train_offsets_df = pd.read_csv(os.path.join(METADATA_DIR,"train_offsets.csv"), index_col=0) 
      train_images_df, val_images_df = dataSplitRandomDrop(train_offsets_df, cat2idx, split_percentage, 
                                                            drop_percentage)

      print("Number of training images:", len(train_images_df))
      print("Number of validation images:", len(val_images_df))
      print("Total images:", len(train_images_df) + len(val_images_df))
      print('Num Categories in Training Set = ' + str(len(train_images_df["category_idx"].unique())))
      print('Num Categories in Val Set = ' + str(len(val_images_df["category_idx"].unique())))
  
      print ('Writing to ' + os.path.join(METADATA_DIR,train_img_filename))
      train_images_df.to_csv(os.path.join(METADATA_DIR,train_img_filename))
      
      print ('Writing to ' + os.path.join(METADATA_DIR,val_img_filename))
      val_images_df.to_csv(os.path.join(METADATA_DIR,val_img_filename))


if __name__=='__main__':
  main()
