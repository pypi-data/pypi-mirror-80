"""Main module."""
import pandas as pds
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score as sil_s
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

def clustering(df, nbr_clust):
    df = df.apply(pds.to_numeric)
    df_kmeans = KMeans(n_clusters=nbr_clust).fit(df)
    return df_kmeans

def pca_making(dataset, df_clust):
    featuresPCA = dataset.copy()
    stand_pca = StandardScaler().fit_transform(featuresPCA)
    pca = PCA(n_components=2).fit_transform(stand_pca)
    pca = pds.DataFrame(data=pca, columns=['PC1', 'PC2'])
    final_pca_df = pds.concat([pca, df_clust[['cluster']]], axis=1)
    pds.set_option('display.max_rows', None)
    return final_pca_df

def optimal_n_cluster(df):
    df = df.apply(pds.to_numeric)
    sil = []
    k_max = 10
    n_sample = len(df)
    for k in range(2, k_max+1):
        if k > n_sample - 1:
            break
        kmeans = KMeans(n_clusters=k).fit(df)
        labels = kmeans.labels_
        sil.append(sil_s(df, labels, metric='euclidean'))
    max_sil = np.max(sil)
    i = 0
    while max_sil != sil[i]:
        i += 1
    return i+3

def parse_df(df):
    colmns = len(df.columns)
    if colmns != 5:
        return False
    if {'total_duration(min)', 'nbr_questions', 'mean_time_response(min)',
    'success_rate', 'course'}.issubset(df.columns) == True:
        return True
    elif {'total_duration(min)', 'nbr_questions', 'mean_time_response(min)',
    'success_rate', 'course'}.issubset(df.columns) == False:
        return False

def modif_df(dataset):
    dict = {}
    for student in dataset['id_eleve'].unique():
        dict[student] = [student]
        student_df = dataset[dataset.id_eleve==student]
        dict[student].append(sum(student_df['duree']) / 60)
        dict[student].append(student_df.shape[0])
        dict[student].append(((sum(student_df['duree']))/(student_df.shape[0])) / 60)
        dict[student].append((student_df[student_df.correct == True].shape[0]/student_df.shape[0]) * 100)
        parcours_df = student_df[student_df.etape == 2]
        if parcours_df.shape[0] == 0:
            dict[student].append(0)
        else:
            parcours_df.sort_values(by='tps_posix', ascending=True)
            dict[student].append(parcours_df.iloc[0, 2])
    final_df = np.array(list(dict.values()))
    final_df = pds.DataFrame(final_df)
    final_df.columns = ['student_id', 'total_duration(min)', 'nbr_questions', 'mean_time_response(min)', 'success_rate', 'course']
    return final_df

def display_graph(pca_df, nbr_clusters):
    fig = plt.figure(figsize=(8,8))
    axe = fig.add_subplot(1, 1, 1)
    axe.set_xlabel('PC1', fontsize=15)
    axe.set_ylabel('PC2', fontsize=15)
    axe.set_title('2D Clustering Representation')
    clusts = np.empty(nbr_clusters, dtype=int)
    for i in range(nbr_clusters):
        clusts[i] = i
    colors_to_chose = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'peachpuff', 'lightseagreen', 'peru', 'sandybrown', 'seashell', 'turquoise', 'aquamarine', 'lightcyan']
    colors = colors_to_chose[:nbr_clusters]
    for target, color, in zip(clusts, colors):
        indicesToKeep = pca_df['cluster'] == target
        axe.scatter(pca_df.loc[indicesToKeep, 'PC1'], pca_df.loc[indicesToKeep, 'PC2'],
                    c=color, s=50)
    axe.legend(clusts)
    axe.grid()
    plt.show()
    return

def main(argv):
    df = pds.read_csv(os.path.join(".", "data", argv[1]))
    if parse_df(df) == False:
    #Dataset must have those columns {'total_duration(min)', 'nbr_questions', 'mean_time_response(min)', 'success_rate', 'course'}
    #Otherwise programm doesn't work (return)
        return
    #nbr_clust is the nbr of clusters found beforehand
    nbr_clust = optimal_n_cluster(df)
    df_kmeans = clustering(df, nbr_clust)
    df_clust = df.copy()
    df_clust['cluster'] = df_kmeans.labels_
    pca_df = pca_making(df, df_clust)
    display_graph(pca_df, nbr_clust)
    return

if __name__ == "__main__":
    main(sys.argv)
    pass