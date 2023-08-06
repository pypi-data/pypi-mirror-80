import numpy as np
from .backend import calc_error, select_second_alpha, update_alpha


def SMO_inner_loop(svc, x, y, i):
    """内循环 用于寻找第二个要更新的变量alpha_j，并进行参数更新"""

    # 计算违背情况
    if svc.non_bound_alpha[i]:
        error_i = svc.error_cache[i]
    else:
        error_i = calc_error(x, y, i, svc.b, svc.alphas, svc.non_zero_alpha, svc.kernel, svc.degree, svc.gamma, svc.beta, svc.theta, svc.customize_kernel)

    num_of_sample = x.shape[0]
    y_i = y[i, :]
    alpha_i = svc.alphas[i]

    # 更新变化量不能太小且0<alpha<C
    if ((y_i * error_i < - svc.tol) and (alpha_i < svc.C)) or ((y_i * error_i > svc.tol) and (alpha_i > 0)):
        best_j = None
        if np.sum(svc.non_bound_alpha) > 0:
            j, error_j = select_second_alpha(error_i, svc.error_cache, svc.non_bound_alpha)
            if update_alpha(svc, x, y, i, j, error_i, error_j):
                # 更新成功
                return 1
            best_j = j

        # 取出所有决策边界的样本的索引
        bound_index = svc.non_bound_alpha.nonzero()[0]

        # 更新样本
        for j in np.random.permutation(bound_index):
            if j == best_j:
                continue
            error_j = svc.error_cache[j]
            if update_alpha(svc, x, y, i, j, error_i, error_j):
                return 1

        # 上述更新都不成功，酒便利所有的样本，强制更新
        for j in np.random.permutation(num_of_sample):
            if j in bound_index:
                continue
            error_j = calc_error(x, y, j, svc.b, svc.alphas, svc.non_zero_alpha, svc.kernel, svc.degree, svc.gamma, svc.beta, svc.theta, svc.customize_kernel)
            if update_alpha(svc, x, y, i, j, error_i, error_j):
                return 1

    return 0


def SMO(svc, x, y):
    """Sequential Minimal Optimization-序列最小优化函数
        SMO算法的思想每次优化两个变量，使之满足KKT条件；不断迭代，最后使得所有变量满足KKT条件
    """
    iter = 0
    num_of_sample = x.shape[0]
    entire_flag = True

    while (svc.max_iter == -1) or (iter < svc.max_iter):
        pair_of_alpha_changed = 0

        if entire_flag:
            # 初始化的时候, 必须遍历一遍全部样本
            for sample in range(num_of_sample):
                pair_of_alpha_changed += SMO_inner_loop(svc, x, y, sample)
        else:
            non_bound_index = svc.non_bound_alpha.nonzero()[0]
            for sample in non_bound_index:
                pair_of_alpha_changed += SMO_inner_loop(svc, x, y, sample)

        # iter增加不能放在最后,不然有可能已经返回导致iter没有改变
        iter += 1

        if entire_flag is True:
            if pair_of_alpha_changed == 0:
                # 遍历了所有的样本，且没有一对alpha被更新，就退出
                return svc
            entire_flag = False
        elif pair_of_alpha_changed == 0:
            entire_flag = True

    return svc
