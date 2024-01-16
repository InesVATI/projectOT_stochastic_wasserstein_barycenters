from texttable import Texttable
import latextable
# from typing import List
import pickle
from glob import glob
from pathlib import Path

class METHOD :
   MONGE = 'Optimal_Monge_Map'
   OT = 'OT_free_support_Sinkhorn'
   BREGMAN = 'Iterative_Bregman'
   ALGO = 'Ascent_Snap_algorithm'

def build_time_table(result_folder : str):
    caption = 'Computation time (in seconds) for the different methods'
    table_label = 'time_table'
    file_paths = glob(f'{result_folder}/time*.pkl')
    nb_exp = len(file_paths)
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't', 't', 't'])
    table.set_cols_align(["l", "r", "r", "r", "r"])

    table.add_rows([["Experiment", METHOD.MONGE.replace('_', ' '), METHOD.BREGMAN.replace('_', ' '),
                     METHOD.OT.replace('_', ' '), METHOD.ALGO.replace('_', ' ')]])
    for i in range(nb_exp):
        with open(file_paths[i], 'rb') as f:
            data = pickle.load(f)
        name_exp = file_paths[i].split('\\')[-1].split('_')
        table.add_row([f'{name_exp[2]} {name_exp[3][:-4]}',
                       '-' if len(data[METHOD.MONGE]) == 0 else f'${data[METHOD.MONGE][0]:.2f} \pm {data[METHOD.MONGE][1]:.2f}$',
                       f'${data[METHOD.BREGMAN][0]:.2f} \pm {data[METHOD.BREGMAN][1]:.2f}$',
                       f'${data[METHOD.OT][0]:.2f} \pm {data[METHOD.OT][1]:.2f}$',
                       '${:.2f} \pm {:.2f}$'.format(data[METHOD.ALGO]['total'][0], data[METHOD.ALGO]['total'][1]),
                       ])

    print(table.draw())
    print(latextable.draw_latex(
        table,
        caption=caption,
        label=f"table:{table_label}"))
   
def build_time_algo_table(result_folder : str):
    caption = 'Computation time (in seconds) for each step of the algorithm'
    table_label = 'time_algo_table'
    file_paths = glob(f'{result_folder}/time*.pkl')
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(["l", "r", "r"])
    table.add_rows([['Experiment', 'Ascent step', 'Snap step']])
    for i in range(len(file_paths)):
        with open(file_paths[i], 'rb') as f:
            data = pickle.load(f)
        name_exp = file_paths[i].split('\\')[-1].split('_')
        table.add_row([f'{name_exp[2]} {name_exp[3][:-4]}',
                       '${:.2f} \pm {:.2f}$'.format(data[METHOD.ALGO]['ascent_time'][0], data[METHOD.ALGO]['ascent_time'][1]),
                       '${:.2f} \pm {:.2f}$'.format(data[METHOD.ALGO]['snap_time'][0], data[METHOD.ALGO]['snap_time'][1])
                       ])
    print(table.draw())
    print(latextable.draw_latex(
        table,
        caption=caption,
        label=f"table:{table_label}"))

if __name__ == '__main__':
    result_folder = Path(__file__).parent / 'results'
    print(result_folder)
    build_time_table(str(result_folder))
    build_time_algo_table(str(result_folder))