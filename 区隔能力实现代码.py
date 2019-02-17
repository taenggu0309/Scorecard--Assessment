
# coding: utf-8

# In[ ]:


"""
1.AUC
"""
def plot_roc(y_label,y_pred):
    """
    y_label:测试集的y
    y_pred:对测试集预测后的概率
    
    return:ROC曲线
    """
    tpr,fpr,threshold = metrics.roc_curve(y_label,y_pred) 
    AUC = metrics.roc_auc_score(y_label,y_pred) 
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(1,1,1)
    ax.plot(tpr,fpr,color='blue',label='AUC=%.3f'%AUC) 
    ax.plot([0,1],[0,1],'r--')
    ax.set_ylim(0,1)
    ax.set_xlim(0,1)
    ax.set_title('ROC')
    ax.legend(loc='best')
    return plt.show(ax)

"""
2.KS
"""
def plot_model_ks(y_label,y_pred):
    """
    y_label:测试集的y
    y_pred:对测试集预测后的概率
    
    return:KS曲线
    """
    pred_list = list(y_pred) 
    label_list = list(y_label)
    total_bad = sum(label_list)
    total_good = len(label_list)-total_bad 
    items = sorted(zip(pred_list,label_list),key=lambda x:x[0]) 
    step = (max(pred_list)-min(pred_list))/200 
    
    pred_bin=[]
    good_rate=[] 
    bad_rate=[] 
    ks_list = [] 
    for i in range(1,201): 
        idx = min(pred_list)+i*step 
        pred_bin.append(idx) 
        label_bin = [x[1] for x in items if x[0]<idx] 
        bad_num = sum(label_bin)
        good_num = len(label_bin)-bad_num  
        goodrate = good_num/total_good 
        badrate = bad_num/total_bad
        ks = abs(goodrate-badrate) 
        good_rate.append(goodrate)
        bad_rate.append(badrate)
        ks_list.append(ks)
    
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1,1,1)
    ax.plot(pred_bin,good_rate,color='green',label='good_rate')
    ax.plot(pred_bin,bad_rate,color='red',label='bad_rate')
    ax.plot(pred_bin,ks_list,color='blue',label='good-bad')
    ax.set_title('KS:{:.3f}'.format(max(ks_list)))
    ax.legend(loc='best')
    return plt.show(ax)

"""
3.基尼系数(这里用的是R代码)
"""

gini.plot <- function(glmWoeFit, trainWoe, y) {
    """
    glmWoeFit:模型
    trainWoe：训练集数据
    y: target字段名
    
    return:gini曲线
    """
  library(ineq)
  predTrainProba <-predict(glmWoeFit, trainWoe, type='response')
  predTrainResult <- prediction(predTrainProba, trainWoe[, y])
  fnr <- performance(predTrainResult, measure='fnr')@y.values[[1]] 
  tnr <- performance(predTrainResult, measure='tnr')@y.values[[1]] 
  plot(tnr, fnr, type='l', main='train_Gini', xlab='x-tnr', ylab='y-fnr', yaxs="i", xaxs="i", col=2)
  abline(a=0, b=1, col=1)
  kslable1 <- paste("Gini:", round(Gini(fnr), 3), sep="")
  legend(0.5, 0.5, c(kslable1), bty="n", ncol = 1)
  legend("bottomright", legend=c("RandomSelection", "ModelPick"), col=c("1", "2"), cex=0.75, lwd=2)
}

"""
4.评分分布图
"""
def plot_score_hist(df,target,score_col,plt_size=None,cutoff=None):
    """
    df:数据集
    target:目标变量的字段名
    score_col:最终得分的字段名
    plt_size:图纸尺寸
    cutoff :划分拒绝/通过的点
    
    return :好坏用户的得分分布图
    """    
    plt.figure(figsize=plt_size)
    x1 = df[df[target]==1][score_col]
    x2 = df[df[target]==0][score_col]
    sns.kdeplot(x1,shade=True,label='坏用户',color='hotpink')
    sns.kdeplot(x2,shade=True,label='好用户',color ='seagreen')
    plt.axvline(x=cutoff)
    plt.legend()
    return plt.show()

