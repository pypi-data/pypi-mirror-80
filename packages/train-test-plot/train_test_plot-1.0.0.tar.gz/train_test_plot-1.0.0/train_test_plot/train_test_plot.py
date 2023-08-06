#------------------------------------------------------------------------------------------------------------------
# train_test_plot_def
#
# MIT License 
# Dr Debdarsan Niyogi (debdarsan.niyogi@gmail.com)
#------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from IPython.display import HTML

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score

import warnings
warnings.filterwarnings("ignore")

# Initialize an empty list of classification algorithms
algorithm_list = []

# Initialize an empty list for the accuracy of each algorithm
accuracy_list = []

def _plot_confusion_matrix(conf_mat, classes, normalize = False, title = 'Confusion Matrix',
                          cmap = plt.cm.Greens, size = 5):
    """
    Plots confusion matrix for binary or multi-class classification
       
    Parameters:
    ----------
        conf_mat: confusion matrix, given test and predicted values of the target (dependent) variable
        classes: comma separated unique class names of the target variable to be predicted
        normalize: boolean flag indicating if normalization is to be applied
        title: title of the confusion matrix plot
        ax: axes object(s) of the plot
        cmap: color map
        size: integer controlling size of the plot and the labels proportionally
    
    Returns:
    -------
        None
    
    """
    
    fig, ax = plt.subplots(figsize = (size, size))
    ax.set_title(title, fontsize = size + 10)
    plt.tick_params(axis = 'x', labelsize = size + 8)
    plt.tick_params(axis = 'y', labelsize = size + 8)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 45, size = size + 8)
    plt.yticks(tick_marks, classes, size = size + 8)
    plt.sca(ax)
    
    fmt = '.2f' if normalize else 'd'
    thresh = conf_mat.max() / 2.
    for i, j in itertools.product(range(conf_mat.shape[0]), range(conf_mat.shape[1])):
        ax.text(j, i, format(conf_mat[i, j], fmt),
                horizontalalignment = "center",
                color= "white" if conf_mat[i, j] > thresh else "black", size = size + 8)

    ax.set_ylabel('True Label', fontsize = size + 8)
    ax.set_xlabel('Predicted Label', fontsize = size + 8)
    ax.imshow(conf_mat, interpolation = 'nearest', cmap = cmap)
    
    plt.show()
    
    return

    
def _compare_algos(algorithm_list, accuracy_list, size = 5):
    
    """
    Plots algorithm names vs the testing accuracy figures
    
    Parameters:
    algorithm_list: list of names of the algorithms
    accuracy_list: list of accuracy values
    size: integer controlling the size of the plot and the labels proportionally
    
    """

    # Combine the list of algorithms and list of accuracy scores into a dataframe
    # and sort the values based on accuracy score
    df_accuracy = pd.DataFrame(list(zip(algorithm_list, accuracy_list)), 
                  columns = ['Algorithm', 'Accuracy Score']).sort_values(by = ['Accuracy Score'], ascending = True)
    
    # Plot
    ax = df_accuracy.plot.barh('Algorithm', 'Accuracy Score', align = 'center', legend = False, color = 'g')

    # Add the data labels
    for i in ax.patches:
        ax.text(i.get_width() + 0.02, i.get_y() + 0.2, str(round(i.get_width(), 2)), fontsize = 10)

    # Set the limit
    plt.xlim(0, 1.1)
    
    # Set the lables
    plt.xlabel('Test Accuracy Score')
    
    # Set ticks
    # Generate a list of ticks for y-axis
    y_ticks = np.arange(len(algorithm_list))
    plt.yticks(y_ticks, df_accuracy['Algorithm'], rotation = 0)
    
    # Set title
    plt.title('Algorithm performance')
    
    # Turn of top and right frames
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return

def train_test_plot(df, target, size, models):
    
    """
    Performs the following operations:
    ---------------------------------
    
    1. Splits the dataframe into target (dependent variable) and predictors (independent variable)
    2. Scales the values of independent variables (all input values must be numeric)
    3. Splits the dataset into train and test sets
    4. Loops through the list of classification algorithms to
       a) Train
       b) Test
       c) Evaluate and report performance
       d) Plot Confusion Matrix
       e) Plot feature importance (if it is available for this particular algorithm)
    5. Shows comparative plot of accuracies for all the algorithms
       
    Parameters:
    ----------
       df (pandas dataframe): the whole dataset containing observations for both target and predictor variables
       target (string): column name of the target variable in df, e.g. 'Species'
       size (int): size of the plots, typical values are 5, 10, 15
       models: model objects
       
    Returns:
    -------
        None
       
    Example:
    -------
       train_test_plot(iris_df, 'Species', 5, models)
       where,
            iris_df: input dataframe,  e.g. iris_df = pd.read_csv('Iris.csv')
            'Species': name of the target column in iris_df
            5: size of the plots generated
            models: list of model objects
            
    """ 
    
    # set X and y
    y = df[target]
    X = df.drop(target, axis=1)

    # scale X
    X = StandardScaler().fit(X).transform(X)

    # Split the data set into training and testing data sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Target class names
    classes = np.unique(df[target])
    
    algorithm_list = []
    accuracy_list = []
    
    for i in range(len(models)):
        
        model = model_clf[i]
        algorithm_list.append(model_clf.index[i])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        disp_line = '<h1>' + model_clf.index[i] + '</h1>'
        display(HTML(disp_line))
        disp_line = '<h2>Scores:</h2>'
        display(HTML(disp_line))
        
        acc = accuracy_score(y_test, y_pred)
        precision, recall, fscore, support = score(y_test, y_pred)
        
        score_df = pd.DataFrame(list(zip(precision, recall, fscore, support)), 
                   columns =['precision', 'recall', 'fscore', 'support'])
        score_df = pd.concat([pd.DataFrame(classes), score_df], axis = 1)        
        score_df.columns =['Target Class', 'precision', 'recall', 'fscore', 'support'] 
        
        
        display(HTML(score_df.to_html(index=False)))

        accuracy_list.append(acc)
        cm_model = confusion_matrix(y_test, y_pred)
        
        
        _plot_confusion_matrix(cm_model, classes=classes, title=model_clf.index[i]+'\nTest Accuracy: {:.2f}'.format(acc))
       
        
        if hasattr(model, 'feature_importances_'):
        
            fig, ax = plt.subplots(figsize=(size,size))
            plt.tick_params(axis='x', labelsize=size+5)
            plt.tick_params(axis='y', labelsize=size+5)
            plt.xticks(size=size+5)
            plt.yticks(size=size+5)
            plt.xlabel('')
            ax.set_title('Feature Importance (using '+ model_clf.index[i] + ')', fontsize=size+10)
            
            importances = pd.DataFrame(np.zeros((X_train.shape[1], 1)), columns=['importance'], index=df.drop(target,axis=1).columns)
            importances.iloc[:,0] = model.feature_importances_
            importances.sort_values(by='importance', inplace=True, ascending=False)
            importancestop = importances.head(10)
            
            sns.barplot(x='importance', y=importancestop.index, data=importancestop)
            
            plt.show()
    
    _compare_algos(algorithm_list, accuracy_list)
    
    return