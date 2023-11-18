from typing import Tuple
import os
import csv

def d01_loader() -> Tuple[list[list[str]], list[list[str]], list[Tuple[int, int]]]:
    """
        Đọc dữ liệu của dataset rest1/rest2:
        + Bỏ qua cột id
        + Nối tất cả chuỗi lại với nhau
        + ... ...

        Kết quả trả ra:
        + Danh sách X loại list[list[str]]
        + Danh sách Y loại list[list[str]]
        + Kết quả là các cặp id của (x, y), loại list[Tuple[int, int]]
    """

    current_file = __file__  # __file__ contains the path of the current file
    current_dir = os.path.dirname(os.path.abspath(current_file))

    d1_path = current_dir + "/../data/ccer/D1/rest1.csv"
    d2_path = current_dir + "/../data/ccer/D1/rest2.csv"
    gt_path = current_dir + "/../data/ccer/D1/gt.csv"

    ans = []
    for path in (d1_path, d2_path):
        set = []
        with open(path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter='|')
            csv_reader.fieldnames = "id", "name", "phone_number", "street"
            # Read each row in the CSV file
            next(csv_reader)
            for row in csv_reader:
                line = row["name"] + " " + row["phone_number"] + " " + row["street"]
                line = line.replace("/"," ")
                line = line.replace("-", " ")
                for w in ["st. ", "w. ", "s. ", "n. ", "e. ", "ave. "]:
                    line = line.replace(w, w[:-1])
                for e in ["st.", "w.", "s.", "n.", "e.", "ave."]:
                    if line.endswith(e):
                        line = line[:-len(e)]
                token_list = line.split()
                set.append(token_list)
        ans.append(set)

    with open(gt_path, newline='') as csvfile:
        set = []
        csv_reader = csv.DictReader(csvfile, delimiter='|')
        for row in csv_reader:
            tup = (int(row["D1"]), int(row["D2"]))
            set.append(tup)
        ans.append(set)

    return ans[0], ans[1], ans[2]