import numpy as np
import pandas as pd
import seaborn as sns
# import matplotlib.pyplot as plt

df = sns.load_dataset('penguins')
# print(df.info())
#      Column             Non-Null Count  Dtype  
# ---  ------             --------------  -----  
#  0   species            344 non-null    object 
#  1   island             344 non-null    object 
#  2   bill_length_mm     342 non-null    float64
#  3   bill_depth_mm      342 non-null    float64
#  4   flipper_length_mm  342 non-null    float64
#  5   body_mass_g        342 non-null    float64
#  6   sex                333 non-null    object     -> 성별 누락된게 11개

# print(df.head())
# print(df.tail())

# print(df.describe())
# print(df['body_mass_g'].describe())
# print(df['bill_depth_mm']>=55.0)  # true, false로 출력됨


print(df[df['bill_length_mm']>=55.0])
#        species  island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
# 169  Chinstrap   Dream            58.0           17.8              181.0       3700.0  Female
# 215  Chinstrap   Dream            55.8           19.8              207.0       4000.0    Male
# 253     Gentoo  Biscoe            59.6           17.0              230.0       6050.0    Male
# 321     Gentoo  Biscoe            55.9           17.0              228.0       5600.0    Male
# 335     Gentoo  Biscoe            55.1           16.0              230.0       5850.0    Male

