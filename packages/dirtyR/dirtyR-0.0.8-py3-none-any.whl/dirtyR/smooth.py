import glob


def smooth(ca_dir, wo_dir, output_dir):

    with open(f'{output_dir}/smooth.r', 'w') as f:

        for t, d in zip(['cat_alone', 'with_owner'], [ca_dir, wo_dir]):

            if t == 'cat_alone':

                variables = [
                    'x_cat', 'y_cat', 'cat_distance', 'velocity', 'acceleration'
                ]

            elif t == 'with_owner':

                variables = [
                    'x_cat', 'y_cat', 'x_owner', 'y_owner', 'distance', 'cat_distance',
                    'velocity', 'acceleration'
                ]

            # Load packages

            print('library(readr)\nlibrary(signal)\n', file=f)

            # Load files and create dataframes

            csv_files_dir = d + '/*.csv'

            files = glob.glob(csv_files_dir)

            for file in files:

                print('\n\ndf <- read_csv("' + file + '")\n', file=f)
                print('df <- df[-c(1, 2  ), ]\n', file=f)

                # Loess

                for i in variables:
                    print(i + '_loessMod' + '<- loess(' + i,
                          '~ time, data = df, span = 0.05', ')', file=f)
                    print(i + '_loess05'
                           + '<- predict(' + i + '_loessMod' + ')', file=f)
                    print('df$' + i + '_loess05'
                           + ' <- ' + i + '_loess05', file=f)

                print('write.csv(df, "' + file[:-4] +
                      '.csv" , row.names = FALSE)', file=f)
