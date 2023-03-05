"""
    retrieve and process a list of eldritch names from
    https://en.wikipedia.org/wiki/List_of_Great_Old_Ones
"""

import pandas as pd


if __name__ == '__main__':

    # retrieve the original data
    url = 'https://en.wikipedia.org/wiki/List_of_Great_Old_Ones'
    beings = pd.read_html(url, match='Name')[0]

    # preprocess data, remove references and non-english characters
    names = beings['Name'].str.lower()
    names = names.str.replace('[\[].*?[\]]','')
    names = names.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # split paired names in two, i.e. Nug and Yeb -> [Nug,Yeb]
    names = names.str.split(' and ')
    names = names.explode(ignore_index=True)
    names = names.str.split(' & ')
    names = names.explode(ignore_index=True)

    # remove non-eldritch names
    to_remove = ['the color', 'god of the red flux', 'the green god',
                 'the unimaginable horror', 'the worm that gnaws in the night']
    names = names[~names.isin(to_remove)]

    # sort and reset index
    names = names.sort_values()
    names = names.reset_index(drop=True)

    # save processed data
    names.to_csv('./names.cvs', header=False, index=False)
