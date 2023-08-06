### gma.unbalance_varcom
import numpy as np
import pandas as pd
from gmat.gmatrix import agmat
from gmat.longwas.unbalance import unbalance_varcom
import logging

logging.basicConfig(level=logging.INFO)

bed_file = '../data/mouse_long/plink'
kin_lst = agmat(bed_file, inv=True, small_val=0.001, out_fmt='id_id_val')
data_file = '../data/mouse_long/phe.unbalance.txt'
id = 'ID'
tpoint = 'weak'
trait = 'trait'
kin_inv_file = '../data/mouse_long/plink.agiv2'
tfix = 'Sex'
prefix_outfile = '../data/mouse_long/gma_unbalance_varcom'
res_var = unbalance_varcom(data_file, id, tpoint, trait, kin_inv_file, tfix=tfix, prefix_outfile=prefix_outfile)


print(res_var)



### gma.unbalance_longwas_fixreg
import numpy as np
import pandas as pd
from gmat.gmatrix import agmat
from gmat.longwas.unbalance import unbalance_varcom
from gmat.longwas.unbalance import unbalance_longwas_fixed
from gmat.longwas.unbalance import unbalance_longwas_fixed_permutation
import logging

logging.basicConfig(level=logging.INFO)

bed_file = '../data/mouse_long/plink'
# kin_lst = agmat(bed_file, inv=True, small_val=0.001, out_fmt='id_id_val')
data_file = '../data/mouse_long/phe.unbalance.txt'
id = 'ID'
tpoint = 'weak'
trait = 'trait'
kin_inv_file = '../data/mouse_long/plink.agiv2'
tfix = 'Sex'
prefix_outfile = '../data/mouse_long/gma_unbalance_varcom'
# res_var = unbalance_varcom(data_file, id, tpoint, trait, kin_inv_file, tfix=tfix, prefix_outfile=prefix_outfile)
print(res_var)


kin_file = '../data/mouse_long/plink.agrm2'
var_com = pd.read_csv("../data/mouse_long/gma_unbalance_varcom.var", sep='\s+', header=0)
prefix_outfile = '../data/mouse_long/unbalance_longwas_fixreg'
#res_lst = unbalance_longwas_fixed(data_file, id, tpoint, trait, bed_file, kin_file, var_com, tfix=tfix,
#                             prefix_outfile=prefix_outfile)

res_lst = unbalance_longwas_fixed_permutation(data_file, id, tpoint, trait, bed_file, kin_file, var_com, tfix=tfix,
                             prefix_outfile=prefix_outfile)



### gma.unbalance_longwas_lt
import numpy as np
import pandas as pd
from gma import cal_kin
from gma import unbalance_varcom
from gma import unbalance_longwas_lt
bed_file = './tests/plink'
kin_lst = cal_kin(bed_file)
data_file = './tests/phe.unbalance.txt'
id = 'ID'
tpoint = 'weak'
trait = 'trait'
kin_inv_file = './tests/plink.giv'
tfix = 'Sex'
prefix_outfile = './tests/gma_unbalance_varcom'
res_var = unbalance_varcom(data_file, id, tpoint, trait, kin_inv_file, tfix=tfix, prefix_outfile=prefix_outfile)
print res_var

kin_file = './tests/plink.grm'
var_com = pd.read_csv("./tests/gma_unbalance_varcom.var", sep='\s+', header=0)
prefix_outfile = './tests/gma_unbalance_longwas_lt'
res_lst = unbalance_longwas_lt(data_file, id, tpoint, trait, bed_file, kin_file, kin_inv_file, var_com, tfix=tfix,
                             prefix_outfile=prefix_outfile)

