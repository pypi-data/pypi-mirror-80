import glob
from pathlib import Path


def turnpoints(csv_dir, variable, output_dir):
    """
    csv_dir is combined and timed files
    variable is usually 'velocity_loess05'
    """
    files = glob.glob(f'{csv_dir}/*.csv')

    with open('plot_turnpoints.r', 'w') as f:

        print("library(pastecs)\nlibrary(readr)\n", file=f)

        for file in files:

            cat = Path(file).stem

            print(f'\n\ndf = read.csv("{file}")\n', file=f)

            print(f'{variable}.tp <- turnpoints(df[,"{variable}"])\n', file=f)

            print(
                f'png("{output_dir}/{Path(file).stem}_turnpoints.png", width=2000, height=1000, res=200)\n', file=f)

            print(
                f'plot(df[, "{variable}"], type = "l", ylab="{variable[:-8]} in Pixels per Second", xlab="Time")\n', file=f)

            print(
                f'lines({variable}.tp, median=FALSE, type = "p", col=c(4,2))\n', file=f)

            print(f'title("{cat}")\n', file=f)

            print("dev.off()\n", file=f)

            for i in ['tppos', 'nturns', 'firstispeak', 'proba']:

                print(f'{i} <- {variable}.tp${i}\n', file=f)

            print(f'cat <- "{cat}"\n', file=f)

            if cat in ['daisy', 'mila', 'marmalade', 'washburne', 'lavoisier']:

                print('infection_status <- "Positive"\n', file=f)

            else:

                print('infection_status <- "Negative"\n', file=f)

            print(
                "turns <- cbind.data.frame(tppos, nturns, firstispeak, cat, infection_status, proba)\n", file=f)

            print(
                f'tppos <- write_csv(turns, "{output_dir}/{Path(file).stem}.csv")\n\n', file=f)

            print('#' * 25, file=f)
