import csv

if __name__ == '__main__':
    path=input("请输入要处理的文件路径:")
    path=path.strip() #去掉收尾空格
    new_path_ls=path.split(".")
    new_path_ls[-2]=new_path_ls[-2]+"_New"
    new_path=".".join(new_path_ls)
    with open(path,"r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[1]!="Title":
                ls=row[1].split(" ")
                new_str=" ".join(ls[:-1])
                row[1]=new_str
            with open(new_path,"a") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(row)
    print("处理完毕")
