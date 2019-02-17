
# coding: utf-8

# In[ ]:


"""
1.精确率，查全率，误伤率
"""
def rule_verify(df,col_score,target,cutoff):
    """
    df:数据集
    target:目标变量的字段名
    col_score:最终得分的字段名    
    cutoff :划分拒绝/通过的点
    
    return :混淆矩阵
    """
    df['result'] = df.apply(lambda x:30 if x[col_score]<=cutoff else 10,axis=1)
    TP = df[(df['result']==30)&(df[target]==1)].shape[0] 
    FN = df[(df['result']==30)&(df[target]==0)].shape[0] 
    bad = df[df[target]==1].shape[0] 
    good = df[df[target]==0].shape[0] 
    refuse = df[df['result']==30].shape[0] 
    passed = df[df['result']==10].shape[0] 
    
    acc = round(TP/refuse,3) 
    tpr = round(TP/bad,3) 
    fpr = round(FN/good,3) 
    pass_rate = round(refuse/df.shape[0],3) 
    matrix_df = pd.pivot_table(df,index='result',columns=target,aggfunc={col_score:pd.Series.count},values=col_score) 
    
    print('精确率:{}'.format(acc))
    print('查全率:{}'.format(tpr))
    print('误伤率:{}'.format(fpr))
    print('规则拒绝率:{}'.format(pass_rate))
    return matrix_df

"""
2.PR曲线
"""
def plot_PR(df,score_col,target,plt_size=None):
    """
    df:得分的数据集
    score_col:分数的字段名
    target:目标变量的字段名
    plt_size:绘图尺寸
    
    return: PR曲线
    """
    total_bad = df[target].sum()
    score_list = list(df[score_col])
    target_list = list(df[target])
    score_unique_list = sorted(set(list(df[score_col])))
    items = sorted(zip(score_list,target_list),key=lambda x:x[0]) 

    precison_list = []
    tpr_list = []
    for score in score_unique_list:
        target_bin = [x[1] for x in items if x[0]<=score]  
        bad_num = sum(target_bin)
        total_num = len(target_bin)
        precison = bad_num/total_num
        tpr = bad_num/total_bad
        precison_list.append(precison)
        tpr_list.append(tpr)
    
    plt.figure(figsize=plt_size)
    plt.title('PR曲线')
    plt.xlabel('查全率')
    plt.ylabel('精确率')
    plt.plot(tpr_list,precison_list,color='tomato',label='PR曲线')
    plt.legend(loc='best')
    return plt.show()

