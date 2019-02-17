
# coding: utf-8

# In[ ]:


"""
1.交叉验证
"""
def cross_verify(x,y,estimators,fold,scoring='roc_auc'):
    """
    x:自变量的数据集
    y:target的数据集
    estimators：验证的模型
    fold：交叉验证的策略
    scoring:评级指标，默认auc
    
    return:交叉验证的结果
    """
    cv_result = cross_val_score(estimator=estimators,X=x,y=y,cv=fold,n_jobs=-1,scoring=scoring)
    print('CV的最大AUC为:{}'.format(cv_result.max()))
    print('CV的最小AUC为:{}'.format(cv_result.min()))
    print('CV的平均AUC为:{}'.format(cv_result.mean()))
    plt.figure(figsize=(6,4))
    plt.title('交叉验证的AUC分布图')
    plt.boxplot(cv_result,patch_artist=True,showmeans=True,
            boxprops={'color':'black','facecolor':'yellow'},
            meanprops={'marker':'D','markerfacecolor':'tomato'},
            flierprops={'marker':'o','markerfacecolor':'red','color':'black'},
            medianprops={'linestyle':'--','color':'orange'})
    return plt.show()

"""
2.学习曲线
"""
def learning_curve(estimator,x,y,cv=None,train_size = np.linspace(0.1,1.0,5),plt_size =None):
    """
    estimator :画学习曲线的基模型
    x:自变量的数据集
    y:target的数据集
    cv:交叉验证的策略
    train_size:训练集划分的策略
    plt_size:画图尺寸
    
    return:学习曲线
    """
    from sklearn.model_selection import learning_curve
    train_sizes,train_scores,test_scores = learning_curve(estimator=estimator,
                                                          X=x,
                                                          y=y,
                                                          cv=cv,
                                                          n_jobs=-1,
                                                          train_sizes=train_size)
    train_scores_mean = np.mean(train_scores,axis=1)
    train_scores_std = np.std(train_scores,axis=1)
    test_scores_mean = np.mean(test_scores,axis=1)
    test_scores_std = np.std(test_scores,axis=1)
    plt.figure(figsize=plt_size)
    plt.xlabel('Training-example')
    plt.ylabel('score')
    plt.fill_between(train_sizes,train_scores_mean-train_scores_std,
                     train_scores_mean+train_scores_std,alpha=0.1,color='r')
    plt.fill_between(train_sizes,test_scores_mean-test_scores_std,
                     test_scores_mean+test_scores_std,alpha=0.1,color='g')
    plt.plot(train_sizes,train_scores_mean,'o-',color='r',label='Training-score')
    plt.plot(train_sizes,test_scores_mean,'o-',color='g',label='cross-val-score')
    plt.legend(loc='best')
    return plt.show()

