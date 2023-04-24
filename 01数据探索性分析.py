
import  pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#plt.rcParams['font.sans-serif'] =['SimHei']  #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus'] =False   #用来正常显示负号

# 类别型变量的分布
def plot_cate_var(df,col_list,hspace=0.4,wspace=0.4,plt_size=None,plt_num=None,x=None,y=None):
    """
    df:数据集
    col_list:变量list集合
    hspace :子图之间的间隔(y轴方向)
    wspace :子图之间的间隔(x轴方向)
    plt_size :图纸的尺寸
    plt_num :子图的数量
    x :子图矩阵中一行子图的数量
    y :子图矩阵中一列子图的数量
    
    return :变量的分布图（柱状图形式）
    """
    plt.figure(figsize=plt_size)
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    plt.rcParams['font.sans-serif']=['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    for i,col in zip(range(1,plt_num+1,1),col_list):
        plt.subplot(x,y,i)
        plt.title(col)
        sns.countplot(data=df,y=col)
        plt.ylabel('')
    return plt.show()

# 数值型变量的分布
def plot_num_col(df,col_list,hspace=0.4,wspace=0.4,plt_type=None,plt_size=None,plt_num=None,x=None,y=None):
    """
    df:数据集
    col_list:变量list集合
    hspace :子图之间的间隔(y轴方向)
    wspace :子图之间的间隔(x轴方向)
    plt_type: 选择直方图/箱线图
    plt_size :图纸的尺寸
    plt_num :子图的数量
    x :子图矩阵中一行子图的数量
    y :子图矩阵中一列子图的数量
    
    return :变量的分布图（箱线图/直方图）
    """
    plt.figure(figsize=plt_size)
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    if plt_type=='hist':
        for i,col in zip(range(1,plt_num+1,1),col_list):
            plt.subplot(x,y,i)
            plt.title(col)
            sns.distplot(df[col].dropna())
            plt.xlabel('')
    if plt_type=='box':
        for i,col in zip(range(1,plt_num+1,1),col_list):
            plt.subplot(x,y,i)
            plt.title(col)
            sns.boxplot(data=df,x=col)
            plt.xlabel('')
    return plt.show()


# 类别型变量的违约率分析
def plot_default_cate(df,col_list,target,hspace=0.4,wspace=0.4,plt_size=None,plt_num=None,x=None,y=None):
    """
    df:数据集
    col_list:变量list集合
    target ：目标变量的字段名
    hspace :子图之间的间隔(y轴方向)
    wspace :子图之间的间隔(x轴方向)
    plt_size :图纸的尺寸
    plt_num :子图的数量
    x :子图矩阵中一行子图的数量
    y :子图矩阵中一列子图的数量
    
    return :违约率分布图（柱状图形式）
    """
    all_bad = df[target].sum()
    total = df[target].count()
    all_default_rate = all_bad*1.0/total
    
    plt.figure(figsize=plt_size)
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    plt.rcParams['font.sans-serif']=['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    for i,col in zip(range(1,plt_num+1,1),col_list):
        d1 = df.groupby(col)
        d2 = pd.DataFrame()
        d2['total'] = d1[target].count()
        d2['bad'] = d1[target].sum()
        d2['default_rate'] = d2['bad']/d2['total']
        d2 = d2.reset_index()
        plt.subplot(x,y,i)
        plt.title(col)
        plt.axvline(x=all_default_rate)
        sns.barplot(data=d2,y=col,x='default_rate')
        plt.ylabel('')
    return plt.show()

# 数值型变量的违约率分析
def plot_default_num(df,col_list,target,hspace=0.4,wspace=0.4,q=None,plt_size=None,plt_num=None,x=None,y=None):
    """
    df:数据集
    col_list:变量list集合
    target ：目标变量的字段名
    hspace :子图之间的间隔(y轴方向)
    wspace :子图之间的间隔(x轴方向)
    q :等深分箱的箱体个数
    plt_size :图纸的尺寸
    plt_num :子图的数量
    x :子图矩阵中一行子图的数量
    y :子图矩阵中一列子图的数量
    
    return :违约率分布图（折线图形式）
    """
    all_bad = df[target].sum()
    total = df[target].count()
    all_default_rate = all_bad*1.0/total 
    
    plt.figure(figsize=plt_size)
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    for i,col in zip(range(1,plt_num+1,1),col_list):
        bucket = pd.qcut(df[col],q=q,duplicates='drop')
        d1 = df.groupby(bucket)
        d2 = pd.DataFrame()
        d2['total'] = d1[target].count()
        d2['bad'] = d1[target].sum()
        d2['default_rate'] = d2['bad']/d2['total']
        d2 = d2.reset_index()
        plt.subplot(x,y,i)
        plt.title(col)
        plt.axhline(y=all_default_rate)
        sns.pointplot(data=d2,x=col,y='default_rate',color='hotpink')
        plt.xticks(rotation=60)
        plt.xlabel('')
    return plt.show()
    
    
    
def plot_default_cate_(df,col,target,plt_size=(7,7),save_path='./picture/'):
    """
    类别型变量违约率分布（单个图）
    
    df:数据集
    col：变量名
    target ：目标变量的字段名
    
    """
    plt.figure(figsize=plt_size)
    plt.rcParams['font.sans-serif']=['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    all_bad = df[target].sum()
    total = df[target].count()
    all_default_rate = all_bad*1.0/total
    d1 = df.groupby(col)
    d2 = pd.DataFrame()
    d2['total'] = d1[target].count()
    d2['bad'] = d1[target].sum()
    d2['default_rate'] = round(d2['bad']/d2['total'],2)
    d2 = d2.reset_index()
    sns.barplot(data=d2,y='default_rate',x=col)
    plt.ylabel('bad_rate')
    plt.title(col)
    figSavePath = save_path+str(col)+'.png'
    plt.savefig(figSavePath)
    
    
    return plt.show()
    


-------------chuss
def plot_obj_rate(df,col,target,save_path='./picture/',ylim1=None,ylim2=None):
    """
    类别型变量的分布和违约率分布组合

    df:数据集
    col：变量名
    target ：目标变量的字段名
    ylim1：左轴的刻度范围
    ylim2:右轴的刻度范围

    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    sns.set(font='SimHei', style='white', )  # 解决Seaborn中文显示问题

    # 取出作图的数据

    all_bad = df[target].sum()
    total = df[target].count()
    all_default_rate = all_bad*1.0/total
    d1 = df.groupby(col)
    d2 = pd.DataFrame()
    d2['total'] = d1[target].count()
    d2['bad'] = d1[target].sum()
    d2['default_rate'] = round(d2['bad']/d2['total'],2)
    d2 = d2.reset_index()

    x = d2[col]
    y1=d2['total']
    y2=d2['default_rate']

    # 设置图形大小
    plt.rcParams['figure.figsize'] = (7, 6)
    fig = plt.figure()


# 画柱形图
    ax1 = fig.add_subplot(111)
    if ylim1 !=None:
        ax1.set_ylim(ylim)
    ax1.bar(x, y1, alpha=0.7, color='k')
    ax1.set_ylabel(u'total', fontsize='20')
    # ax1.set_xlabel(u'年份', fontsize='20')
    ax1.tick_params(labelsize=15)
    for i, (_x, _y) in enumerate(zip(x, y1)):
        plt.text(_x, _y, y1[i], color='black', fontsize=20, ha='center', va='bottom')  # 将数值显示在图形上
    ax1.set_title(col, fontsize='20')


    # 画折线图
    ax2 = ax1.twinx()  # 组合图必须加这个
    if ylim2 !=None:
        ax2.set_ylim(ylim2)      
    ax2.plot(x, y2, 'r', ms=10, lw=3, marker='o') # 设置线粗细，节点样式
    ax2.set_ylabel(u'rate', fontsize='20')
    sns.despine(left=True, bottom=True)   # 删除坐标轴，默认删除右上
    ax2.tick_params(labelsize=15)
    for x, y in zip(x, y2):   # # 添加数据标签
        plt.text(x, y-2.5, str(y), ha='center', va='bottom', fontsize=20, rotation=0)

    figSavePath = save_path+str(col)+'.png'
    plt.savefig(figSavePath)
    return plt.show()
    
# 类别变量组合图 
def plot_obj_zuhe(df,col,target,save_path='./picture/'):
    all_bad = df[target].sum()
    total = df[target].count()
    all_default_rate = all_bad*1.0/total
    d1 = df.groupby(col)
    d2 = pd.DataFrame()
    d2['total'] = d1[target].count()
    d2['bad'] = d1[target].sum()
    d2['good']=d2['total']-d2['bad']
    d2['default_rate'] = round(d2['bad']/d2['total'],2)
    d2 = d2.reset_index()

    plt.bar(d2[col], d2['good'], width=0.2, color='r', label='good')                 #绘制股票最高价条形图
    plt.bar(d2[col], d2['bad'], bottom= d2['good'], width=0.2, color='b', label='neg') #以股票最高价为起点绘制股票最低价条形图
    plt.title(col)                                                  #设置标题
    plt.legend(loc=1)
    
    figSavePath = save_path+str(col)+'.png'
    plt.savefig(figSavePath)
    return plt.show()
