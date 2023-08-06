import numpy as np
import pandas as pd
import os


def write_gene_txt(trainset_dir):
    dataset_list = os.listdir(trainset_dir)
    gene = ''
    for dataset in dataset_list:
        with open(trainset_dir + dataset) as k:
            file_gene = k.readline().strip('\n').lower().split('\t')
        for i in file_gene:
            if i == 'cell_label':
                continue
            if i not in gene:
                gene = gene + i + ', '
    gene = gene + 'cell_label'
    gene = gene.split(', ')
    return gene

def get_all_gene(trainset_dir):
    dataset_list = os.listdir(trainset_dir)
    gene = []
    for dataset in dataset_list:
        with open(trainset_dir + dataset) as k:
            file_gene = k.readline().strip('\n').lower().split('\t')
        for i in file_gene:
            if i == 'cell_label':
                continue
            if i not in gene:
                gene.append(i)
    gene.append('cell_label')
    return gene

def treat_to_same_gene(gene, root_dir,output_dir):
    dataset_list = os.listdir(root_dir)
    for dataset in dataset_list:
        all_data = pd.read_csv(root_dir + dataset, sep='\t')
        with open(root_dir+dataset) as f:
            all_data_columns = f.readline().strip('\n').lower().split('\t')
        all_data.index = range(all_data.shape[0])
        all_data.columns = all_data_columns
        df = pd.DataFrame(np.zeros((all_data.shape[0], len(gene))), columns=gene)
        for i in df.columns:
            if i in all_data.columns:
                df[i] = all_data[i]
        df['cell_label'] = df['cell_label'].astype(str)
        train_indices = np.array([]).astype(int)

        cell_label = df['cell_label']
        df.drop(labels=['cell_label'], axis=1, inplace=True)
        df.insert(len(df.columns), 'cell_label', cell_label)

        df.to_hdf(output_dir+dataset.split('.')
                            [0]+'.h5', key='data')
