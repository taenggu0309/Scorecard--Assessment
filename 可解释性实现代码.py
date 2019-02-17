
# coding: utf-8

# In[ ]:


"""
1.提升图/洛伦兹曲线
"""
def plot_lifting(df,score_col,target,bins=10,plt_size=None):
    """
    df:数据集，包含最终的得分
    score_col:最终分数的字段名
    target:目标变量名
    bins:分数划分成的等份数
    plt_size:绘图尺寸
    
    return:提升图和洛伦兹曲线
    """
    score_list = list(df[score_col])
    label_list = list(df[target])
    items = sorted(zip(score_list,label_list),key = lambda x:x[0])
    step = round(df.shape[0]/bins,0)
    bad = df[target].sum()
    all_badrate = float(1/bins)
    all_badrate_list = [all_badrate]*bins
    all_badrate_cum = list(np.cumsum(all_badrate_list))
    all_badrate_cum.insert(0,0)
    
    score_bin_list=[]
    bad_rate_list = []
    for i in range(0,bins,1):
        index_a = int(i*step)
        index_b = int((i+1)*step)
        score = [x[0] for x in items[index_a:index_b]]
        tup1 = (min(score),)
        tup2 = (max(score),)
        score_bin = tup1+tup2
        score_bin_list.append(score_bin)
        label_bin = [x[1] for x in items[index_a:index_b]]
        bin_bad = sum(label_bin)
        bin_bad_rate = bin_bad/bad
        bad_rate_list.append(bin_bad_rate)
    bad_rate_cumsum = list(np.cumsum(bad_rate_list))
    bad_rate_cumsum.insert(0,0)
    
    plt.figure(figsize=plt_size)
    x = score_bin_list
    y1 = bad_rate_list
    y2 = all_badrate_list
    y3 = bad_rate_cumsum
    y4 = all_badrate_cum
    plt.subplot(1,2,1)
    plt.title('提升图')
    plt.xticks(np.arange(bins)+0.15,x,rotation=90)
    bar_width= 0.3
    plt.bar(np.arange(bins),y1,width=bar_width,color='hotpink',label='score_card')
    plt.bar(np.arange(bins)+bar_width,y2,width=bar_width,color='seagreen',label='random')
    plt.legend(loc='best')
    plt.subplot(1,2,2)
    plt.title('洛伦兹曲线图')
    plt.plot(y3,color='hotpink',label='score_card')
    plt.plot(y4,color='seagreen',label='random')
    plt.xticks(np.arange(bins+1),rotation=0)
    plt.legend(loc='best')
    return plt.show()

"""
2.woe可视化
"""
def plot_woe(bin_df,hspace=0.4,wspace=0.4,plt_size=None,plt_num=None,x=None,y=None):
    """
    bin_df:list形式，里面存储每个变量的分箱结果
    hspace :子图之间的间隔(y轴方向)
    wspace :子图之间的间隔(x轴方向)
    plt_size :图纸的尺寸
    plt_num :子图的数量
    x :子图矩阵中一行子图的数量
    y :子图矩阵中一列子图的数量
    
    return :每个变量的woe变化趋势图
    """
    plt.figure(figsize=plt_size)
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    for i,df in zip(range(1,plt_num+1,1),bin_df):
        col_name = df.index.name
        df = df.reset_index()
        plt.subplot(x,y,i)
        plt.title(col_name)
        sns.barplot(data=df,x=col_name,y='woe')
        plt.xlabel('')
        plt.xticks(rotation=30)
    return plt.show()

"""
3.检查变量的woe是否单调
"""
def woe_monoton(bin_df):
    """
    bin_df:list形式，里面存储每个变量的分箱结果
    
    return :
    woe_notmonoton_col :woe没有呈单调变化的变量，list形式
    woe_judge_df :df形式，每个变量的检验结果
    """
    woe_notmonoton_col =[]
    col_list = []
    woe_judge=[]
    for woe_df in bin_df:
        col_name = woe_df.index.name
        woe_list = list(woe_df.woe)
        if woe_df.shape[0]==2:
            #print('{}是否单调: True'.format(col_name))
            col_list.append(col_name)
            woe_judge.append('True')
        else:
            woe_not_monoton = [(woe_list[i]<woe_list[i+1] and woe_list[i]<woe_list[i-1])                                or (woe_list[i]>woe_list[i+1] and woe_list[i]>woe_list[i-1])                                for i in range(1,len(woe_list)-1,1)]
            if True in woe_not_monoton:
                #print('{}是否单调: False'.format(col_name))
                woe_notmonoton_col.append(col_name)
                col_list.append(col_name)
                woe_judge.append('False')
            else:
                #print('{}是否单调: True'.format(col_name))
                col_list.append(col_name)
                woe_judge.append('True')
    woe_judge_df = pd.DataFrame({'col':col_list,
                                 'judge_monoton':woe_judge})
    return woe_notmonoton_col,woe_judge_df


"""
4.某个区间的woe值是否过大（绝对值大于等于1）
"""
def woe_large(bin_df):
    """
    bin_df:list形式，里面存储每个变量的分箱结果
    
    return:
    woe_large_col: 某个区间woe大于1的变量，list集合
    woe_judge_df :df形式，每个变量的检验结果
    """
    woe_large_col=[]
    col_list =[]
    woe_judge =[]
    for woe_df in bin_df:
        col_name = woe_df.index.name
        woe_list = list(woe_df.woe)
        woe_large = list(filter(lambda x:abs(x)>=1,woe_list))
        if len(woe_large)>0:
            col_list.append(col_name)
            woe_judge.append('True')
            woe_large_col.append(col_name)
        else:
            col_list.append(col_name)
            woe_judge.append('False')
    woe_judge_df = pd.DataFrame({'col':col_list,
                                 'judge_large':woe_judge})
    return woe_large_col,woe_judge_df

