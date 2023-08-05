from __future__ import print_function

from sklearn.metrics import *
import pandas as pd
import numpy as np
import pandas as pd


def binary_score(model, test, y_test, name='test', silent=False):

    from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
    from collections import Counter
    try:
        pred_test_proba = model.predict_proba(test)
        if len(pred_test_proba.shape)>1:
            try:
                pred_test_proba = pred_test_proba[:, 1]
            except IndexError:
                pred_test_proba = pred_test_proba.reshape(-1,)
    except AttributeError:
        pred_test_proba = model.predict(test)
    gini_test = gini(y_test, pred_test_proba)
    pred_test = model.predict(test)
    if len(np.unique(pred_test))>2 :
        pred_test = pred_test>.5
    is_balanced_ = y_test.sum()/(len(y_test))
    if np.abs(is_balanced_-.5)<.02:
        is_balanced = True
    else:
        is_balanced = False
    recall = recall_score(y_test, pred_test)
    if silent:
        return gini_test, recall
    print('*'*80)
    print('on %s'%name.upper())
    if not is_balanced:
        acc_test = balanced_accuracy_score(y_test, pred_test)*100
        print('balanced accuracy = %.3f %%' % acc_test, end=' | ')
    acc_test = accuracy_score(y_test, pred_test)*100
    print('Accuracy = %.3f %%' % acc_test, end=' | ')
    print('Gini = %.3f ' % gini_test, end=' | ')
    print('Recall score=%.3f' % recall, end=' | ')

    print('confusion matrix:')
    df = pd.DataFrame(confusion_matrix(y_test, pred_test), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    print(df)


def binary_score_(y_test, pred_test_label, pred_test_proba, name='test'):

    from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
    from collections import Counter
    if len(pred_test_proba.shape)>1:
        try:
            pred_test_proba=pred_test_proba[:,1]
        except IndexError:
            pred_test_proba=pred_test_proba.reshape(-1,)
    gini_test = gini(y_test, pred_test_proba)
    is_balanced_ = pred_test_label.sum()/(len(pred_test_label))
    if np.abs(is_balanced_-.5)<.02:
        is_balanced = True
    else:
        is_balanced = False
    print('*'*80)
    print('on %s'%name.upper())
    if not is_balanced:
        acc_test = balanced_accuracy_score(y_test, pred_test_label)*100
        print('balanced accuracy = %.3f %%' % acc_test, end=' | ')
    acc_test = accuracy_score(y_test, pred_test_label)*100
    print('Accuracy = %.3f %%' % acc_test, end=' | ')
    print('Gini = %.3f ' % gini_test, end=' | ')
    recall = recall_score(y_test, pred_test_label)
    print('Recall score=%.3f' % recall, end=' | ')

    print('confusion matrix:')
    df = pd.DataFrame(confusion_matrix(y_test, pred_test_label), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    print(df)


def multiclass_score(model, test, y_test, name):

    from sklearn.metrics import balanced_accuracy_score, accuracy_score
    pred_test = model.predict(test)
    if len(pred_test.shape)>1:
        pred_test = np.argmax(pred_test, axis=1)
    acc_test = balanced_accuracy_score(y_test, pred_test)*100
    print('*'*80)
    print('On %s: Balanced accuracy  = %.3f %%' % (name, acc_test), end=' | ')
    print('accuracy = %.3f %%' % accuracy_score(y_test, pred_test), end=' | ')
    index = ['True_%s' % str(i) for i in range(len(np.unique(y_test)))]
    columns = ['Pred_%s' % str(i) for i in range(len(np.unique(y_test)))]
    df = pd.DataFrame(confusion_matrix(y_test, pred_test), index=index, columns=columns)
    print('Confusion matrix:')
    print(df)


def gini(actual, pred):

    from sklearn.metrics import roc_curve, auc
    fpr, tpr, thresholds = roc_curve(actual, pred, pos_label=1)
    auc_score = auc(fpr,tpr)
    return 2*auc_score-1


def confusion_matrix(actual, pred):

    from sklearn.metrics import confusion_matrix
    return confusion_matrix(actual, pred)


def KfoldWithoutCv(models, test, y_test, name='test'):

    from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
    from collections import Counter
    ginis = []
    recalls = []
    acc = []
    acc_balanced = []
    df = pd.DataFrame(np.zeros((2, 2)), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    for model in models:
        try:
            pred_test_proba = model.predict_proba(test.copy())
            if len(pred_test_proba.shape)>1:
                pred_test_proba = pred_test_proba[:, 1]
        except AttributeError:
            pred_test_proba = model.predict(test.copy())
        ginis.append(gini(y_test, pred_test_proba))
        pred_test = model.predict(test)
        if len(np.unique(pred_test)) > 2 :
             pred_test = pred_test > .5
        acc.append(accuracy_score(y_test, pred_test)*100)
        recalls.append(recall_score(y_test, pred_test)*100)
        acc_balanced.append(balanced_accuracy_score(y_test, pred_test)*100)
        df = df.add(pd.DataFrame(confusion_matrix(y_test, pred_test), index=['True_0', 'True_1'],columns=['Pred_0', 'Pred_1']))
    is_balanced_ = y_test.sum()/len(y_test)
    if np.abs(is_balanced_-.5) < .02:
        is_balanced = True
    else:
        is_balanced = False
    recalls = np.array(recalls)
    acc = np.array(acc)
    ginis = np.array(ginis)
    acc_balanced = np.array(acc_balanced)
    print('*'*80)
    print('on %s'%name.upper())
    if not is_balanced:
        print('Balanced accuracy = %.3f+/-%.03f%%' % (acc_balanced.mean(), acc_balanced.std()), end=' | ')
    print('Accuracy = %.3f+/-%.03f%%' % (acc.mean(), acc.std()), end=' | ')
    print('Gini = %.3f+/-%.03f' % (ginis.mean(), ginis.std()), end=' | ')
    print('Recall = %.3f+/-%.03f%%' % (recalls.mean(), recalls.std()), end=' | ')
    print('confusion matrix:')
    print(df/len(models))


def binary_scoreKfold(models, cv, X, y, get_score=False):
    '''
    :param models: list of model for Cv
    :param cv: cross validation kFolds
    :param X: Data
    :param y: target
    :param get_score: If true, return the score of all data set X, from test set in each kfold
    :return: score_ if get_score is set true
    '''
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
    from collections import Counter
    ginis_train, ginis_test = [], []
    recalls_train, recalls_test = [], []
    acc_train, acc_test = [], []
    acc_balanced_train, acc_balanced_test = [], []
    df_train = pd.DataFrame(np.zeros((2, 2)), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    df_test = pd.DataFrame(np.zeros((2, 2)), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    if y is not None:
        if not X.index.equals(y.index):
            X = X.reset_index(drop=True)
            y= y.reset_index(drop=True)
    for model, (index_train, index_test) in zip(models, cv.split(X, y)):
        train, test = X.iloc[index_train], X.iloc[index_test]
        y_train, y_test = y.iloc[index_train], y.iloc[index_test]
        try:
            pred_test_proba = model.predict_proba(test)
            try:
                score_ = np.append(score_, pred_test_proba[:,1])
            except NameError:
                score_ = pred_test_proba[:,1]
            pred_train_proba = model.predict_proba(train)
            if len(pred_test_proba.shape)>1:
                pred_test_proba = pred_test_proba[:, 1]
                pred_train_proba = pred_train_proba[:, 1]
        except AttributeError:
            pred_test_proba = model.predict(test)
            pred_train_proba = model.predict(train)
        ginis_train.append(gini(y_train, pred_train_proba))
        ginis_test.append(gini(y_test, pred_test_proba))
        pred_test = model.predict(test)
        pred_train = model.predict(train)
        if len(np.unique(pred_test))>2:
            pred_test = pred_test>.5
            pred_train = pred_train>.5
        acc_test.append(accuracy_score(y_test, pred_test)*100)
        acc_train.append(accuracy_score(y_train, pred_train)*100)
        recalls_test.append(recall_score(y_test, pred_test)*100)
        recalls_train.append(recall_score(y_train, pred_train)*100)
        acc_balanced_test.append(balanced_accuracy_score(y_test, pred_test)*100)
        acc_balanced_train.append(balanced_accuracy_score(y_train, pred_train)*100)
        df_test = df_test.add(pd.DataFrame(confusion_matrix(y_test, pred_test), \
                                index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1']))
        df_train = df_train.add(pd.DataFrame(confusion_matrix(y_train, pred_train), \
                                 index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1']))
    if get_score:
        return score_
    is_balanced_ = y_test.sum()/(len(y_test))
    if np.abs(is_balanced_-.5) < .02:
        is_balanced = True
    else:
        is_balanced = False
    recalls_train, recalls_test = np.array(recalls_train), np.array(recalls_test)
    acc_train, acc_test = np.array(acc_train), np.array(acc_test)
    ginis_train, ginis_test = np.array(ginis_train), np.array(ginis_test)
    acc_balanced_train, acc_balanced_test = np.array(acc_balanced_train), np.array(acc_balanced_test)
    print('*'*80)
    print('ON TEST')
    if not is_balanced:
        print('Balanced accuracy = %.3f+/-%.03f%%' % (acc_balanced_test.mean(), acc_balanced_test.std()), end=' | ')
    print('Accuracy = %.3f+/-%.03f%%' % (acc_test.mean(), acc_test.std()), end=' | ')
    print('Gini = %.3f+/-%.03f' % (ginis_test.mean(), ginis_test.std()), end=' | ')
    print('Recall = %.3f+/-%.03f%%' % (recalls_test.mean(), recalls_test.std()), end=' | ')
    print('confusion matrix:')
    print(df_test/len(models))
    print('*'*80)
    print('ON TRAIN')
    if not is_balanced:
        print('Balanced accuracy = %.3f+/-%.03f%%' % (acc_balanced_train.mean(), acc_balanced_train.std()), end=' | ')
    print('Accuracy = %.3f+/-%.03f%%' % (acc_train.mean(), acc_train.std() ), end=' | ')
    print('Gini = %.3f+/-%.03f' % (ginis_train.mean(), ginis_train.std() ), end=' | ')
    print('Recall = %.3f+/-%.03f%%' % (recalls_train.mean(), recalls_train.std()), end=' | ')
    print('confusion matrix:')
    print(df_train/len(models))



