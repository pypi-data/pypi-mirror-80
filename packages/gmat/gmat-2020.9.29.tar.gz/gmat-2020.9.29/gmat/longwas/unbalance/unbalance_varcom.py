import logging
from scipy import sparse
from scipy.sparse import csr_matrix, hstack
import numpy as np
import pandas as pd
from patsy import dmatrix
import gc
import os


from .common import *
from .unbalance_emai import *


def unbalance_varcom(data_file, id, tpoint, trait, kin_inv_file, tfix=None, fix=None, forder=3, aorder=3, porder=3,
             na_method='omit', init=None, maxiter=100, cc_par=1.0e-8, cc_gra=1.0e6,
                     em_weight_step=0.01, prefix_outfile='unbalance_varcom'):
    logging.info('########################################################################')
    logging.info('###Prepare the data for unbalanced longitudinal variances estimation.###')
    logging.info('########################################################################')
    logging.info('***Read the data file***')
    logging.info('Data file: ' + data_file)
    data_df = pd.read_csv(data_file, sep='\s+', header=0)
    logging.info('NA method: ' + na_method)
    if na_method == 'omit':
        data_df = data_df.dropna()
    elif na_method == 'include':
        data_df = data_df.fillna(method='ffill')
        data_df = data_df.fillna(method='bfill')
    else:
        print('na_method does not exist', na_method)
        exit()
    col_names = data_df.columns
    logging.info('The column names of data file: ' + ' '.join(list(col_names)))
    logging.info('Note: Variates beginning with a capital letter is converted into factors.')
    class_vec = []
    for val in col_names:
        if not val[0].isalpha():
            print("The first character of columns names must be alphabet!")
            exit()
        if val[0] == val.capitalize()[0]:
            class_vec.append(val)
            data_df[val] = data_df[val].astype('str')
        else:
            try:
                data_df[val] = data_df[val].astype('float')
            except Exception as e:
                print(e)
                print(val, "may contain string, please check!")
                exit()
    logging.info('Individual column: ' + id)
    if id not in col_names:
        print(id, 'is not in the data file, please check!')
        exit()
    if id not in class_vec:
        print('The initial letter of', id, 'should be capital')
        exit()
    id_order = []
    id_arr = list(data_df[id])
    id_order.append(id_arr[0])
    for i in range(1, len(id_arr)):
        if id_arr[i] != id_arr[i - 1]:
            id_order.append(id_arr[i])
    id_in_data = set(data_df[id])
    if len(id_in_data) - len(id_order) != 0:
        print('The data is not sored by individual ID!')
        exit()
    logging.info('Time points column: ' + tpoint)
    if tpoint not in col_names:
        print(tpoint, 'is not in the data file, please check!')
        exit()
    if tpoint in class_vec:
        print('The initial letter of', tpoint, 'should be lowercase')
        exit()
    logging.info('Trait column: ' + trait)
    if trait not in col_names:
        print(trait, 'is not in the data file, please check!')
        exit()
    if trait in class_vec:
        print('The initial letter of', trait, 'should be lowercase')
        exit()
    logging.info('Code factor variables of the data file: ' + ' '.join(list(class_vec)))
    code_val = {}
    code_dct = dct_2D()
    for val in class_vec:
        code_val[val] = 0
        temp = []
        for i in range(data_df.shape[0]):
            if data_df[val][i] not in code_dct[val]:
                code_val[val] += 1
                code_dct[val][data_df[val][i]] = str(code_val[val])
            temp.append(code_dct[val][data_df[val][i]])
        data_df[val] = np.array(temp)
    for val in class_vec:
        data_df[val] = data_df[val].astype('int')
    logging.info('***Build the design matrix for fixed effect***')
    logging.info('Time dependent fixed effect: ' + str(tfix))
    leg_fix = leg(data_df[tpoint], forder)
    if tfix == None:
        xmat_t = np.concatenate(leg_fix, axis=1)
        xmat_t = csr_matrix(xmat_t)
    else:
        if tfix not in class_vec:
            logging.error(tfix + ' is not the class variate')
            exit()
        row = np.array(range(data_df.shape[0]))
        col = np.array(data_df[tfix]) - 1
        val = np.array([1.0] * data_df.shape[0])
        tfix_mat = csr_matrix((val, (row, col)))
        xmat_t = []
        for i in range(len(leg_fix)):
            xmat_t.append(tfix_mat.multiply(leg_fix[i]))
        xmat_t = hstack(xmat_t)
        del row, col, val
        gc.collect()
    logging.info('Time independent fix effect: ' + str(fix))
    xmat_nt = None
    if fix == None:
        xmat_nt = None
    else:
        try:
            fix_exp = ''
            vec = fix.split('+')
            for i in vec:
                val = i.strip()
                if val in class_vec:
                    fix_exp += 'C(' + val + ')'
                else:
                    fix_exp += val
            xmat_nt = dmatrix(fix_exp, data_df)
            logging.info('The expression for fixed effect: ' + fix_exp)
        except Exception as e:
            logging.error(e + ': Check the fix effect expression.')
            exit()
        xmat_nt = csr_matrix(xmat_nt[:, 1:])
    xmat = hstack([xmat_t, xmat_nt])
    max_id = max(data_df[id]) + 1
    tmin = min(data_df[tpoint])
    tmax = max(data_df[tpoint])
    leg_lst = []  # legendre polynomials for time dependent fixed SNP effects, save for each individuals
    for i in range(1, max_id):
        leg_lst.append(leg_mt(data_df[data_df[id] == i][tpoint], tmax, tmin, forder))
    logging.info('***Read the inversion of kinship matrix***')
    with open(kin_inv_file, 'r') as fin:
        row = []
        col = []
        kin_inv = []
        id_in_kin = {}
        for line in fin:
            arr = line.split()
            id_in_kin[arr[0]] = 1
            id_in_kin[arr[1]] = 1
            if arr[0] not in code_dct[id]:
                code_val[id] += 1
                code_dct[id][arr[0]] = str(code_val[id])
            if arr[1] not in code_dct[id]:
                code_val[id] += 1
                code_dct[id][arr[1]] = str(code_val[id])
            row.append(int(code_dct[id][arr[0]]))
            col.append(int(code_dct[id][arr[1]]))
            kin_inv.append(float(arr[2]))
    kin_inv = csr_matrix((np.array(kin_inv), (np.array(row) - 1, np.array(col) - 1))).toarray()
    kin_inv = np.add(kin_inv, kin_inv.T)  # Notice: maybe not lower triangular matrix
    np.fill_diagonal(kin_inv, 0.5 * np.diag(kin_inv))
    del row, col
    gc.collect()
    id_in_kin = set(id_in_kin.keys())
    id_not_in_kin = list(id_in_data - id_in_kin)
    if len(id_not_in_kin) != 0:
        logging.error('The ID: ' + ' '.join(id_not_in_kin) + ' in the data file is not in the kinship file!')
        exit()
    logging.info('***Build the dedign matrix for random effect***')
    logging.info('Legendre order for additive effects: ' + str(aorder))
    leg_add = leg(data_df[tpoint], aorder)
    row = np.array(range(data_df.shape[0]))
    col = np.array(data_df[id]) - 1
    val = np.array([1.0] * data_df.shape[0])
    add_mat = csr_matrix((val, (row, col)), shape=(data_df.shape[0], kin_inv.shape[0]))
    zmat_add = []
    for i in range(len(leg_add)):
        zmat_add.append(add_mat.multiply(leg_add[i]))
    logging.info('Legendre order for permanent environmental effect: ' + str(porder))
    leg_per = leg(data_df[tpoint], porder)
    per_mat = csr_matrix((val, (row, col)))
    zmat_per = []
    for i in range(len(leg_per)):
        zmat_per.append((per_mat.multiply(leg_per[i])))
    del row, col, val
    gc.collect()
    zmat = [zmat_add, zmat_per]
    y = data_df[trait].values.reshape(data_df.shape[0], 1)
    kin_inv = [kin_inv, sparse.eye(max(data_df[id]), format="csr")]
    logging.info('###########################################################')
    logging.info('###Start the unbalanced longitudinal variances estimation###')
    logging.info('###########################################################')
    res = unbalance_emai(y, xmat, zmat, kin_inv, init=init, maxiter=maxiter, cc_par=cc_par, cc_gra=cc_gra, em_weight_step=em_weight_step)
    var_file = prefix_outfile + '.var'
    res.to_csv(var_file, sep=' ', index=False)
    return res
