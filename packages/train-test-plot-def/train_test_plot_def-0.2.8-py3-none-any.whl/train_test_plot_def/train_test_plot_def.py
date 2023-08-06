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

# Import LogisticRegression, KNeighborsClassifier, SVM, DecisionTreeClassifier, RandomForestClassifier, XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

import warnings
warnings.filterwarnings("ignore")

# Pre-defined Classifier Models
model_lrg = LogisticRegression(random_state=42, solver='lbfgs', max_iter=10000)
model_knn = KNeighborsClassifier(n_neighbors=5, leaf_size=30, n_jobs=-1)
model_svm = svm.SVC(random_state=42)
model_dtr = DecisionTreeClassifier(random_state=42)
model_rfr = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model_xgb = XGBClassifier()

# List of pre-defined models 
models = [model_lrg, model_knn, model_svm, model_dtr, model_rfr, model_xgb]

# List of pre-defined model names
model_names = ['LogisticRegression', 'KNeighborsClassifier', 'SVC', 
               'DecisionTreeClassifier', 'RandomForestClassifier', 'XGBClassifier']

# First letters of model names
model_ids = 'LKSDRX'

# Initialize an empty list of classification algorithms
algorithm_list = []

# Initialize an empty list for the accuracy of each algorithm
accuracy_list = []

def _plot_confusion_matrix(conf_mat, classes, normalize = False, title = 'Confusion Matrix',
                          cmap = plt.cm.Greens, size = 5):
    """
    Plots confusion matrix for binary or multi-class classification
       
    Parameters:
    conf_mat: confusion matrix, given test and predicted values of the target (dependent) variable
    classes: comma separated unique class names of the target variable to be predicted
    normalize: boolean flag indicating if normalization is to be applied
    title: title of the plot
    ax: axes object(s) of the plot
    cmap: color map
    size: integer controlling size of the plot and the labels proportionally
    
    """
    
    fig, ax = plt.subplots(figsize = (size,size))
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

    ax.set_ylabel('True label', fontsize = size + 8)
    ax.set_xlabel('Predicted label', fontsize = size + 8)
    ax.imshow(conf_mat, interpolation = 'nearest', cmap = cmap)
    
    plt.show()
    
    return

    
def _compare_algos(algorithm_list, accuracy_list, size=5):
    
    """
    Plots algorithm name vs the testing accuracy figures
    
    Parameters:
    algorithm_list: list of names of algorithms
    accuracy_list: list of accuracy values
    size: integer controlling size of the plot and the labels proportionally
    
    """
# Combine the list of algorithms and list of accuracy scores into a dataframe
# and sort the values based on accuracy score
    df_accuracy = pd.DataFrame(list(zip(algorithm_list, accuracy_list)), 
                  columns = ['Algorithm', 'AccuracyScore']).sort_values(by = ['AccuracyScore'], ascending = True)

    
    # Plot
    ax = df_accuracy.plot.barh('Algorithm', 'AccuracyScore', align = 'center', legend = False, color = 'g')

    # Add the data labels
    for i in ax.patches:
        ax.text(i.get_width()+0.02, i.get_y()+0.2, str(round(i.get_width(),2)), fontsize=10)

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

def train_test_plot_def(df, target, algos, size):
    
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
    5. Reports comparative plot of accuracies for all the algorithms
       
    Parameters:
    ----------
       df (pandas dataframe): the whole dataset containing observations for both target and predictor variables
       
       target (string): column name of the target variable in df, e.g. 'Species'
       
       algos (comma separated charcter string): the first letters of classification algorithms to be applied, e.g. l,r,x
           l: LogisticRegression
           k: KNeighborsClassifier
           s: Support Vector Machine 
           d: DecisionTreeClassifier
           r: RandomForestClassifier
           x: XGBClassifier
           
       size (int): size of the plots, typical values are 5, 10, 15
       
    Returns:
    -------
        None
       
    Example:
    -------
       train_test_plot(iris_df, 'Species', 'l,r,x', 5)
       where,
            iris_df: input dataframe.  e.g. iris_df = pd.read_csv('Iris.csv')
            'Species': name of the target column in iris_df
            'l,r,x': first letters of (L)ogisticRegression', (R)andomForestClassifier and (X)GBClassifier (case insensitive)
            5: size of the plots generated
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
    algos_selected = algos.upper().split(',')
    
    for i in range(len(algos_selected)):
        this_algo = algos_selected[i].strip()
        indx = model_ids.index(this_algo)
        model = models[indx]
        algorithm_list.append(model_names[indx])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        disp_line = '<h1>' + model_names[indx] + '</h1>'
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
        
        
        _plot_confusion_matrix(cm_model, classes=classes, title=model_names[indx]+'\nTest Accuracy: {:.2f}'.format(acc))
       
        
        if hasattr(model, 'feature_importances_'):
        
            fig, ax = plt.subplots(figsize=(size,size))
            plt.tick_params(axis='x', labelsize=size+5)
            plt.tick_params(axis='y', labelsize=size+5)
            plt.xticks(size=size+5)
            plt.yticks(size=size+5)
            plt.xlabel('')
            ax.set_title('Feature Importance (using '+ model_names[indx]+')', fontsize=size+10)
            
            importances = pd.DataFrame(np.zeros((X_train.shape[1], 1)), columns=['importance'], index=df.drop(target,axis=1).columns)
            importances.iloc[:,0] = model.feature_importances_
            importances.sort_values(by='importance', inplace=True, ascending=False)
            importancestop = importances.head(10)
            
            sns.barplot(x='importance', y=importancestop.index, data=importancestop)
            
            plt.show()
    
    _compare_algos(algorithm_list, accuracy_list)
    return