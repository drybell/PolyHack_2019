# Daniel Ryaboshapka
# analyze and export to csv 
# test1.txt 
# analysis.py 

import csv


def main():
    filename = "fixed_dump2.txt"
    # print(filename)
    directory_names = []
    totals = []
    permissions = []
    links = []
    owner = []
    group = []
    size = []
    month = []
    day = []
    time = []
    name = []
    directory_count = []
    flag = False
    cnt = 0
    new_block = True
    overall = 0
    with open(filename) as f:
        # print("Opened File")
        for line in f:
            #first line is file path: 
            if new_block == True:
                #print(line)
                line = line.replace('\n', "")
                line = line[:-1]
                print(line)
                directory_names.append(line)
                flag = True
                new_block = False
            elif flag is True:
                #print(line)
                totals.append(line)
                flag = False
            elif line == "\n":
                directory_count.append(cnt)
                cnt = 0
                new_block = True
            else:
                change_line = line.split(" ")
                while("" in change_line):
                    change_line.remove("")
                #print(change_line)
                #print(change_line[0])
                permissions.append(change_line[0])
                links.append(change_line[1])
                owner.append(change_line[2])
                group.append(change_line[3])
                size.append(change_line[4])
                month.append(change_line[5])
                day.append(change_line[6])
                if ":" in change_line[7]:
                    time.append(2019)
                else:
                    time.append(change_line[7])
                new_name = change_line[8].replace('\n', "")
                print("\t"+new_name)
                name.append(new_name)
                flag = False
                cnt = cnt + 1
            overall = overall + 1
            # print(overall)

    directory_count.append(cnt)

    # with open("node_graph1.txt", "w"):
    #     count_trailing = 0
    #     count_leading = 0
    #     for count in directory_count:
    #         count_leading = count_leading + count - 1
    #         while count_trailing <= count_leading:
    #             data.append(row)
    #             count_trailing = count_trailing + 1
    #         count_leading = count_leading + 1

    with open('small.csv', 'w', newline="") as csvfile:
        count_trailing = 0
        count_leading = 0
        data = []
        fieldnames = ['permissions', 'links', 'owner', 'group', 'size', 'month', 'day', 'time', 'name']
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldnames)

        for count in directory_count:
            count_leading = count_leading + count - 1
            while count_trailing <= count_leading:
                row = []
                row.append(permissions[count_trailing])
                row.append(links[count_trailing])
                row.append(owner[count_trailing])
                row.append(group[count_trailing])
                row.append(size[count_trailing])
                row.append(month[count_trailing])
                row.append(day[count_trailing])
                row.append(time[count_trailing])
                row.append(name[count_trailing])
                print(row)
                data.append(row)
                count_trailing = count_trailing + 1
            count_leading = count_leading + 1
        
        for row in data:
            writer.writerow(row)


#for name, perm, link, o, g, a, m, d, t, n



            







if __name__ == '__main__':
    main()