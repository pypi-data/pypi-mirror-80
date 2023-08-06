import os
import argparse
from Bio.PDB import PDBList


class ImportPdb:
    def __init__(self, dir, user, pdb):
        self.data_dir = dir
        self.user_id = user
        self.pdb_code = pdb.lower()
        self.pdb_exists = False

    def pdb_importer(self):
        if not os.path.exists(os.path.join(self.data_dir, self.user_id)):
            os.makedirs(os.path.join(self.data_dir, self.user_id))
            print('making directory')

        if not os.path.exists(os.path.join(self.data_dir, self.user_id, self.pdb_code + '.pdb')):
            pdbl = PDBList()
            ### line below makes test stall on travis ###
            pdbl.retrieve_pdb_file(self.pdb_code, pdir=os.path.join(self.data_dir, self.user_id), file_format='pdb')
            os.rename(os.path.join(self.data_dir, self.user_id, 'pdb' + self.pdb_code + '.ent'),
                      os.path.join(self.data_dir, self.user_id, self.pdb_code + '.pdb'))
            self.pdb_exists = True
        else:
            print('File is already downloaded')
            self.pdb_exists = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--user_id', required=True, help='user ID')
    parser.add_argument('-pdb', '--pdb', required=True, help='pdb code you want to import')
    args = vars(parser.parse_args())

    user_id = args['user_id']
    data_dir = os.path.abspath(os.path.join('..', '..', 'data', 'xcimporter', 'input'))
    pdb_code = args['pdb']

    init = ImportPdb(data_dir, user_id, pdb_code.lower())
    init.pdb_importer()
