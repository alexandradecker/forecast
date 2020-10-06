import pandas as pd
from tqdm import tqdm, trange


def add_time(participant):
    data = pd.read_csv("eyetracking/" + participant +
                       "_encoding.csv_rm_cols.csv")
    data['Time'] = "NULL"

    start = 0
    display = None
    size = len(data.index)
    for index in trange(size):
        if start > index:
            continue
        if data['SAMPLE_MESSAGE'][index] == 'display':
            trial = data['TRIAL_INDEX'][index]
            display = index

            # Update time for every entry before display
            for i in range(start, display):
                data['Time'][i] = - 1 * (display - i) / 1000
            start = display + 1

            # Update time for every entry after display
            while start < size and data['TRIAL_INDEX'][start] == trial:
                data['Time'][start] = (start - display) / 1000
                start += 1

        # # FOR TESTING ONLY
        # if index >= 1000:
        #     break

    return data


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')

    for i in trange(1, 2):
        if i < 10:
            participant = "0" + str(i)
        else:
            participant = str(i)
        add_time(participant).to_csv(
            "eyetracking_final/" + participant + ".csv")
