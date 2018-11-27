import csv


def obtain_simplified_data(file_name):
    fieldnames = [
        "Bats", "Age", "PA", "BA", "OBP", "SLG", "BB%", "K%",
        "BB/K", "HR%", "Lev", "Aff", "First", "Last", 'ID']

    input_csvfile = open(file_name, 'r')
    output_csvfile = open('MiLB-Player-Data-Simplified.csv', 'w')

    writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
    writer.writeheader()

    reader = csv.reader(input_csvfile)
    previous_data = []
    ids_processed = set()
    for i, input_row in enumerate(reader):
        if i == 0:
            continue
        if not input_row[2]:
            to_write = {
                "Bats": "",
                "Age": "",
                "PA": "",
                "BA": "",
                "OBP": "",
                "SLG": "",
                "BB%": "",
                "K%": "",
                "BB/K": "",
                "HR%": "",
                "Lev": "",
                "Aff": "",
                "First": input_row[0],
                "Last": input_row[1],
                "ID": "",
            }
            writer.writerow(to_write)
            continue
        if not input_row[5] == '2018':
            if previous_data and not input_row[2] == previous_data[-1] and\
             not previous_data[-1] in ids_processed:
                to_write = {
                    "Bats": "",
                    "Age": "",
                    "PA": "",
                    "BA": "",
                    "OBP": "",
                    "SLG": "",
                    "BB%": "",
                    "K%": "",
                    "BB/K": "",
                    "HR%": "",
                    "Lev": "",
                    "Aff": "",
                    "First": previous_data[0],
                    "Last": previous_data[1],
                    "ID": previous_data[2],
                }
                writer.writerow(to_write)
                ids_processed.add(previous_data[-1])
            previous_data = input_row[:3]
            continue
        if input_row[2] in ids_processed:
            continue
        to_write = {
            "Bats": input_row[3],
            "Age": input_row[6],
            "PA": input_row[13],
            "BA": input_row[25],
            "OBP": input_row[26],
            "SLG": input_row[27],
            "BB%": input_row[35],
            "K%": input_row[36],
            "BB/K": input_row[37],
            "HR%": input_row[38],
            "Lev": input_row[10],
            "Aff": input_row[11],
            "First": input_row[0],
            "Last": input_row[1],
            "ID": input_row[2],
        }
        writer.writerow(to_write)
        ids_processed.add(input_row[2])
    input_csvfile.close()
    output_csvfile.close()
    print('Simplified file created')

if __name__ == '__main__':
    file_name = '../MiLB-Player-Data-Master.csv'
    obtain_simplified_data(file_name)
