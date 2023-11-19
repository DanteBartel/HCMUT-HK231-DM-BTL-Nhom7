import os
import csv
from math import floor

def _is_float_or_int(string: str) -> bool:
    if string.isnumeric():
        return True
    if string.replace(".", "").isnumeric():
        return True
    return False
    
def d03_loader() -> tuple[list[list[str]], list[list[str]], list[tuple[int,int]]]:
    """
    d02_loader reads the dataset in the data/ccer/D3 directory, which contains information about the products of Amazon and GP.

    Each row contains the id, title, description, manufacture, and price of an individual product.

    d02_loader will remove the id column from each row, and the price will be round to the nearest of 10. Any special character or delimiter will be removed.

    The final string will be split by a blank character.
    
    Data shape:
    D1: list of rows; each row is a list of words; each word is a string.
    D2: the same as X.
    GT: list of rows; each row is a tuple with type (int, int), and each interger is the index of the corresponding rows in D1 and D2 that have the same string.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    d1_path = current_dir + "/../data/ccer/D3/amazon.csv"
    d2_path = current_dir + "/../data/ccer/D3/gp.csv"
    gt_path = current_dir + "/../data/ccer/D3/gt.csv"

    data = [] # type: list[list[list[str]]]
    for path in (d1_path, d2_path):
        set = []
        with open(file=path,mode='rt', newline='') as file:
            data_file = csv.DictReader(file, delimiter='#')
            data_file.fieldnames ='id', 'title', 'description', 'manufacturer', 'price'
            # Read each row in the CSV file
            next(data_file)
            for row in data_file:
                rounded_price = str(floor(float(row['price'])/10)*10) if _is_float_or_int(row['price']) else row['price'] # type: str
                line = row['title'] + " " + row['description'] + " " + row['manufacturer'] + " " + rounded_price
                for spec_char in ["/", "-", ". ", ": ", ".."]:
                    line = line.replace(spec_char, " ")
                token_list = line.split()
                set.append(token_list)
        data.append(set)
    gt = [] # type: list[tuple[int,int]]
    with open(file=gt_path, mode = 'rt', newline='') as file:
        gt_file = csv.DictReader(file,  delimiter='#')
        for row in gt_file:
            tuple = (int(row['D1']), int(row['D2'])) # type: tuple[int,int]
            gt.append(tuple)
    dataset = (data[0], data[1], gt) # type: tuple[list[list[str]], list[list[str]], list[tuple[int,int]]]
    return dataset

        
if __name__ == "__main__":
    (d1, d2, gt) = d02_loader()
    # print(d1)
    (i1, i2) = gt[0]
    print(i1, i2)
    print(d1[i1])
    print(d2[i2])