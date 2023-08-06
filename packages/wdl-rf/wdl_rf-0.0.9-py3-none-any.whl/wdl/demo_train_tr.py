from wdl.demo_train import train_experiment
from wdl.run_utils import InitParam,InitParam2
from wdl.demo_train_v2 import train_experiment as train_experiment2

def train_experiment_tr(source_weights,param,k=1):
    """
    wdl_rf的迁移学习版本
    :param source_weights: 源域训练得到的权重值文件
    :param param: 必要参数
    :param k: k折交叉验证
    :return:
    """
    param.set_source_domain_weights_file(source_weights)
    train_experiment(param=param,k=k)

def train_experiment2_tr(source_weights,param,k=1):
    """
    wdl_rf2的迁移学习版本
    :param source_weights: 源域训练得到的权重文件
    :param param: 必要参数
    :param k: k折交叉验证
    :return:
    """
    param.set_source_domain_weights_file(source_weights)
    train_experiment2(param2=param,k=k)