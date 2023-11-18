from typing import Tuple
import os
import csv

def d09_loader() -> Tuple[list[list[str]], list[list[str]], list[Tuple[int, int]]]:
    """
        Đọc dữ liệu của dataset dblp/scholar:
        

        Kết quả trả ra:
        + Danh sách X loại list[list[str]]
        + Danh sách Y loại list[list[str]]
        + Kết quả là các cặp id của (x, y), loại list[Tuple[int, int]]
    """

    current_file = __file__  # __file__ contains the path of the current file
    current_dir = os.path.dirname(os.path.abspath(current_file))

    d1_path = current_dir + "/../data/ccer/D9/dblp.csv"
    d2_path = current_dir + "/../data/ccer/D9/scholar.csv"
    gt_path = current_dir + "/../data/ccer/D9/gt.csv"

    ans = []
    for path in (d1_path, d2_path):
        set = []
        with open(path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter='>')
            
            # Read each row in the CSV file
            for row in csv_reader:
                line = row["title"] + " " + row["authors"] + " " + row["venue"] + " " + row["year"]
                line = line.replace(", "," ")
                line = line.replace(". "," ")
                line = line.replace("-"," ")
                line = line.replace("(","")
                line = line.replace(")","")
                line.lower()
                token_list = line.split(" ")
                set.append(token_list)
        ans.append(set)

    with open(gt_path, newline='') as csvfile:
        set = []
        csv_reader = csv.DictReader(csvfile, delimiter='>')
        for row in csv_reader:
            tup = (int(row["EntityFromPartA"]), int(row["EntityFromPartB"]))
            set.append(tup)
        ans.append(set)

    return ans[0], ans[1], ans[2]