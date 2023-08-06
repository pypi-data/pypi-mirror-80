# A custom ML library to do resampling,regression and classification model's will also be added your dataset with different methods like train_test_split
# or K-fold Cross Validation

# Ritesh Yadav 27 sep 2020

# train_test_split


# Split a dataset into a train and test set

from random import randrange, seed
import numpy as np

def data_split(data,ratio):
    np.random.seed(42)
    shuffled = np.random.permutation(len(data))
    test_set_size = int(len(data) * ratio)
    test_indices = shuffled[:test_set_size]
    train_indices = shuffled[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


# Split a dataset into k folds


def cross_validation_split(dataset, folds=3):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset) / folds)
    for i in range(folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split

#if __name__ == '__main__':
    #seed()
    #dataset1 = [[0.1], [2.88], [3], [4], [5], [6], [7], [8], [9], [10]]
    #dataset2 = [[0.1], [2.88], [3], [4], [5], [6], [7], [8], [9], [10]]
    #X_train,X_test = train_test_split(dataset1,dataset2, split=0.40)
    #folds = cross_validation_split(dataset1, 4)
    #print(folds)
    #print(X_train)
    #print(X_test)