# Multiobjective optimization methodology
This folder shows an example of the automated approximation of TNN with arbitrary inputs. It is adapted to 

The scripts are compatible with the requirements in (../requirements.txt)

```sh
cd ..
pip install -r requirements.txt
cd TNN_moo
python3 breastcancer2b.py
python moo_pcc_mb.py
```


## Library of approximate components
Folder AxLibrary shows exact and approximate implementation of two-bit inputs LTGS with following ternary weights:

 - breastcancer2b_0: [1, -1, 1, -1, -1, -1]
 - breastcancer2b_1: [1, -1, 1, 1, 1, 1]
 - breastcancer2b_2: [1, 1, 1, 1, -1, -1, 1, 1]
 - breastcancer2b_3: [-1, 1, -1, 1, -1]
 - breastcancer2b_4: [-1, 1, 1, 1]
 - breastcancer2b_5: [1, -1, 1, 1, 1, -1, 1]
 - breastcancer2b_6: [1, -1, -1, 1, 1, -1, -1]
 - breastcancer2b_7: [1, -1, -1, 1, -1, -1, -1, 1]
 - breastcancer2b_8: [1, -1, 1, -1, 1, -1, -1]
 - breastcancer2b_9: [-1, -1, 1, 1, 1, -1, 1]
 - breastcancer2b_10: [1, 1, -1, -1, 1]
 - breastcancer2b_11: [-1, -1, -1, 1, -1, -1, -1, 1, 1]

and 14-bit popcount for the output layer.

The libraries are parsed to one pickle file for LTGS and one for Popcounts using AxLibrary/parse.py.


## Evaluation of accurate implementation
This script load accurate implementation of the approximate LTGS and Popcount. These circuits are located in the folder AxLibrary/Exact

```sh
python breastcancer2b.py
# Training: 81.59%
# Testing: 83.90%
```

## Multiobjective optimization