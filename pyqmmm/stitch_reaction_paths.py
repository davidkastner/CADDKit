'''
See more here: https://github.com/davidkastner/quick-csa/blob/main/README.md
DESCRIPTION
    Potential energy scans can be generated by running it forward and backwards.
    This script will stitch the two halves back together as an .xyz file.
    It will also return a .dat file of the energies vs. the reaction coordindate.
    The data will also be plotted.

    Author: David Kastner
    Massachusetts Institute of Technology
    kastner (at) mit . edu

'''
################################ DEPENDENCIES ##################################
import glob
import sys
import pandas as pd
import numpy as np

################################# FUNCTIONS ####################################

'''
Get the user's linear combination of restraints.
Returns
-------
curr_rc_list : list
    Takes an arbitrary length list of prompts for user e.g., ['first', 'second']
Returns
-------
first : list
    List of atoms indices corresponding to the first reaction coordinate
second : list
    List of atoms indices corresponding to the second reaction coordinate
'''


def user_input(curr_rc_list):
    for curr_rc in curr_rc_list:
        # What atoms define the reaction coordinate (RC)
        rxn_rc = input('What atoms define your {} rxn coord?'.format(curr_rc))
        # Convert user input to a list even if it is hyphenated
        temp = [(lambda sub: range(sub[0], sub[-1] + 1))
                (list(map(int, ele.split('-')))) for ele in raw.split(',')]
        # Save the RC lists to the corresponding variables
        if curr_rc == 'first':
            first = [b for a in temp for b in a]
        elif curr_rc == 'second':
            second = [b for a in temp for b in a]

    return first, second


def stitch_reaction_paths():
    print('\n.-----------------------.')
    print('| STITCH REACTION PATHS |')
    print('.-----------------------.\n')
    print('Name the forward scan trajectory forward.xyz.')
    print('Name the reverse scan trajectory reverse.xyz.')
    print('Combines the two trajectories and save it as a new file.\n')

    # This list will be populated with dictionaries for each frame
    user_input(['first', 'second']):


if __name__ == "__main__":
    stitch_reaction_paths()
