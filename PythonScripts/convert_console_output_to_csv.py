import pandas as pd
import argparse


index_time = 1
index_step = 5
index_time_per_step = 8
index_loss = 9
# 0     1               2               3                    4    5    6        7    8      9
# I0429 19:24:54.645233 139728892675968 model_lib_v2.py:679] Step 1000 per-step time 1.434s loss=8.465


def main(path: str) -> None:
    print(f"Got '{path}'")
    with open(path, 'r') as token:
        lines = token.readlines()
    # Process file
    data = []
    for line in lines:
        words = line.split(' ')
        try:  # Read data
            time = words[index_time]
            step = int(words[index_step])
            time_per_step = float(words[index_time_per_step].split('s')[0])
            loss = float(words[index_loss].split('=')[-1])
            # Append data
            data.append(
                [time, time_per_step, step, loss]
            )
        except IndexError:
            continue
        except ValueError:
            continue
        pass
    # Create data frame
    column_name = ['time', 'per_step_time', 'step', 'loss']
    time_loss_df = pd.DataFrame(data, columns=column_name)
    # Save data
    ext = path.split('.')[-1]
    path = path.replace(ext, 'csv')
    time_loss_df.to_csv(path, index=False)
    print(f"Saved file under '{path}'")
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert console output (from file) to csv")
    parser.add_argument('--path', type=str, required=True, help='Path to file with console output')
    args = parser.parse_args()
    main(args.path)
    pass
