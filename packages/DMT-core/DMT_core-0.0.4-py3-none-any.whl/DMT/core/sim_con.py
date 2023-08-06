""" This module supplies a class to manage all simulations, regardless of the device simulator.

It works together with the DutView class, which is the subclass of all device simulators.
Features:

* Manages all simulations in a unified way, independent of the actual simulation backend.
* Supports to run simulations on multiple cores in parallel
* Supports to run simulations on a remote server (including file up and download)

Author: Mario Krattenmacher | Mario.Krattenmacher@tu-dresden.de
Author: Markus Müller | markus.mueller3@tu-dresden.de
"""
# DMT
# Copyright (C) 2019  Markus Müller and Mario Krattenmacher and the DMT contributors <https://gitlab.hrz.tu-chemnitz.de/CEDIC_Bipolar/DMT/>
#
# This file is part of DMT.
#
# DMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import copy
import logging
import os
import time
import subprocess
from reprint import output
from pathlib import PurePosixPath, PureWindowsPath

from DMT.core import Singleton
from DMT.config import DATA_CONFIG
from DMT.exceptions import SimulationUnsuccessful

if DATA_CONFIG['backend_remote']:
    import paramiko
    from scp import SCPClient

class SimCon(object, metaclass=Singleton):
    """ Simulation controller class. SINGLETON design pattern.

    Parameters
    -----------
    n_core  :  int
        Number of cores that shall be used for simulations.
    t_max   :  float
        Timeout for simulations. If a simulation runs longer than t_max in seconds, it is killed.

    Attributes
    -----------
    n_core  :  int
        Number of cores that shall be used for simulations.
    t_max   :  float
        Timeout for simulations. If a simulation runs longer than t_max in seconds, it is killed.
    sim_list :  [{'dut': dut, 'sweep': sweep}]
        A list of dicts containing the queued simulations. Each dict holds a 'dut' key value pair and a 'sweep' key value pair.

    ssh_client
        Client to execute SSH commands on a remote server.
    scp_client
        Client to transfer files to a remote server via SCP.
    """
    def __init__(self, n_core=4, t_max=30):
        self.n_core    =  n_core
        self.t_max     =  t_max
        self.sim_list  =  []

        ### ssh stuff
        self.ssh_client = None
        self.scp_client = None

    def clear_sim_list(self):
        """ Remove everything from the sim_list
        """
        self.sim_list  =  []


    def append_simulation(self, dut, sweep):
        """ Adds one DutView class object together with one Sweep class object to the list of simulations sim_list.

        This methods adds a dut with a sweep to the simulation. The following pairs of input parameters are implemented:

        * [dut] + sweep: add many duts with the same sweep to the sim_list
        * dut+[sweep]: add one dut with many sweeps to the sim_list
        * dut+sweep: add one dut with one sweep to the sim list

        dmt adds a the dut itself and a COPY of the sweep to self.sim_list.

        Parameters
        -----------
        dut : :class:`~DMT.core.dut_view.DutView` or [:class:`~DMT.core.dut_view.DutView`]
            Objected of a subclass of DutView. This object describes the device to be simulated and specifies the backend.
        sweep : :class:`~DMT.core.sweep.Sweep` or [:class:`~DMT.core.sweep.Sweep`]
            Definition of the sweep to be performed on the DUT according to the Sweep class.
        """
        if isinstance(dut, list) and not isinstance(sweep, list):
            for d in dut:
                self.sim_list.append({'dut':d, 'sweep':copy.deepcopy(sweep)})

        elif not isinstance(dut, list) and isinstance(sweep, list):
            for s in sweep:
                self.sim_list.append({'dut':dut, 'sweep':copy.deepcopy(s)})

        elif not isinstance(dut, list) and not isinstance(sweep, list):
            self.sim_list.append({'dut':dut, 'sweep':copy.deepcopy(sweep)})

        else:
            raise IOError('DMT -> append_simulation(): parameters are not of correct type. Supported: [dut]+sweep; dut+[sweep]; dut+sweep .')

    def run_and_read(self, force=False, remove_simulations=False):
        """ Run all queued simulations and load the results into the Duts' databases.

        Parameters
        ----------
        force  :  bool
            default=False. If =True, the simulations will be run and saved back. If =False, the simulations will only be run if that has not already been done before. This is ensured using the hash system.
        """
        run_sims = False
        if force:
            logging.info('Simulations forced!')
            sims_to_simulate =  self.sim_list
            run_sims = True
        else:
            #check which simulations really need to be run
            sims_to_simulate =  []
            for sim in self.sim_list:
                dut_name = sim['dut'].name + str( sim['dut'].get_hash() )
                sim_name = sim['sweep'].name + '_' + sim['sweep'].get_hash()
                if not sim['dut'].check_existence_sweep(sim['sweep']):
                    # if not in dut.data and not in dut.db
                    try:
                        # was it simulated already successfully ?
                        sim['dut'].validate_simulation_successful(sim['sweep'])
                        logging.info('Simulation of DuT %s with sweep %s already done and results are valid, only data needs to be read.', dut_name, sim_name)
                        logging.debug("The simulation folder of this simulation was %s", sim['dut'].get_sim_folder(sim['sweep']))
                        sim['dut'].add_data(sim['sweep'])
                        run_sims = True
                    except (SimulationUnsuccessful, FileNotFoundError):
                        # ok simulate it!
                        sim['dut'].delete_sim_results(sim['sweep'], ignore_errors=True) # remove for safety
                        logging.info('Simulation of DuT %s with sweep %s needed.', dut_name, sim_name)
                        sims_to_simulate.append(sim)
                        run_sims = True
                else:
                    logging.info('Simulation of DuT %s with sweep %s loaded from database.', dut_name, sim_name)

        # remote simulations ?
        if any([sim for sim in sims_to_simulate if sim['dut'].simulate_on_server]):
            self.create_ssh_client()

        #start the simulations using the simulation control.
        process_finished = self.run_simulations(sims_to_simulate)

        if self.ssh_client is not None:
            self.close_ssh_client()

        all_sim_success = True
        for p in process_finished:
            all_sim_success  =  all_sim_success and p['success']

            dut_name = p['dut'].name + str( p['dut'].get_hash() )
            sim_name = p['sweep'].name + '_' + p['sweep'].get_hash()
            # inform data_manager about the finished simulations
            try:
                if p['success']:
                    p['dut'].add_data(p['sweep'])
                    logging.info('Simulation of DuT %s with sweep %s successfull.', dut_name, sim_name)
                else:
                    color_red = '\033[91m'
                    color_end = '\033[0m'
                    print('{0:s}Simulation of DuT {1:s} with sweep {2:s} failed.{3:s}'.format(color_red, dut_name, sim_name, color_end))
                    logging.info('Simulation of DuT %s with sweep %s failed.', dut_name, sim_name)
            except SimulationUnsuccessful:
                color_red = '\033[91m'
                color_end = '\033[0m'
                print('{0:s}Simulation of DuT {1:s} with sweep {2:s} failed.{3:s}'.format(color_red, dut_name, sim_name, color_end))
                logging.info('Simulation of DuT %s with sweep %s failed.', dut_name, sim_name)

        if remove_simulations:
            # if storage saving is on, the read simulations can be deleted:
            for sim in self.sim_list:
                sim['dut'].delete_sim_results(sim['sweep'], ignore_errors=True)
        #reset the queue
        self.sim_list  =  []

        return all_sim_success, run_sims # the list is empty if no simulations were necessary, empty list -> False

    def create_ssh_client(self):
        """ Creates the clients to communicate with the server.
        """
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(
            DATA_CONFIG['server']['adress'],
            username=DATA_CONFIG['server']['ssh_user'],
            key_filename=os.path.expanduser(DATA_CONFIG['server']['ssh_key']),
        )

        self.scp_client = SCPClient(self.ssh_client.get_transport())

        # ensure the correct path:
        if DATA_CONFIG['server']['unix']:
            DATA_CONFIG['server']['simulation_path'] = PurePosixPath(DATA_CONFIG['server']['simulation_path'])
        else:
            DATA_CONFIG['server']['simulation_path'] = PureWindowsPath(DATA_CONFIG['server']['simulation_path'])

    def close_ssh_client(self):
        """ Closes the ssh connection again.
        """
        self.ssh_client.close()

        self.ssh_client = None
        self.scp_client = None

    def copy_to_server(self, dut, sweep):
        """ Copies the simulation data to the server.

        Parameters
        -----------
        dut : DutView
        sweep : Sweep
        """
        sim_folder = dut.get_sim_folder(sweep)

        root, _sweep_folder = os.path.split(sim_folder)
        _root, dut_folder = os.path.split(root)

        self.ssh_client.exec_command('mkdir ' + str(DATA_CONFIG['server']['simulation_path'] / dut_folder))

        self.scp_client.put(
            sim_folder,
            remote_path=DATA_CONFIG['server']['simulation_path'] / dut_folder,
            recursive=True,
        )

    def copy_from_server(self, dut, sweep):
        """ Collects the simulation data from the server.

        Parameters
        -----------
        dut : DutView
        sweep : Sweep
        """
        sim_folder = dut.get_sim_folder(sweep)

        root, sweep_folder = os.path.split(sim_folder)
        _root, dut_folder = os.path.split(root)

        self.scp_client.get(
            DATA_CONFIG['server']['simulation_path'] / dut_folder / sweep_folder,
            local_path=root,
            recursive=True,
        )

    def run_simulations(self, sim_list):
        """ Runs all given simulations in parallel.

        Parameters
        -----------
        sim_list :  [{}]
            List of dictionaries, each dictionary has a 'dut': :class:`~DMT.core.DutView` and 'sweep': :class:`~DMT.core.Sweep` key value pair.

        Returns
        -------
        success  :  list[process]
            List of finished processes
        """
        if len(sim_list) == 0:
            return []

        # test if same simulation is added twice.
        set_dut_hashes = set([sim_i['dut'].get_hash() for sim_i in sim_list])

        list_to_delete = []
        for dut_hash in set_dut_hashes:
            list_sweep_hashes = []
            for i_sim, sim_a in enumerate(sim_list):
                if sim_a['dut'].get_hash() == dut_hash:
                    if sim_a['sweep'].get_hash() in list_sweep_hashes:
                        list_to_delete.append(i_sim)
                    else:
                        list_sweep_hashes.append(sim_a['sweep'].get_hash())

        for to_delete in sorted(list_to_delete, reverse=True):
            del sim_list[to_delete]

        #start simulations
        process_running     = []
        process_finished    = []
        finished            = False
        n                   = 0
        n_total             = len(sim_list)
        with output(output_type='list', initial_len=self.n_core+7, interval=0) as output_list:
            while not finished:
                # run infinite processes parallel on the server
                if (len([process for process in process_running if not process['backend_remote']]) < self.n_core) and (len(sim_list) > 0 ):
                    #take the next element from the self.sim_list and start it
                    sim            =  sim_list[0]
                    sim_list       =  sim_list[1:]
                    #start the simulation on this core
                    sweep          =  sim['sweep']
                    dut            =  sim['dut']
                    if not hasattr(dut, 't_max') or dut.t_max is None: # make sure t_max is set in every simulated dut
                        dut.t_max  = self.t_max
                    dut.prepare_simulation(sweep)
                    if dut.simulate_on_server:
                        self.copy_to_server(dut, sweep)

                    t0             =  time.time()
                    if dut.simulate_on_server:
                        self.run_simulation_remote(dut, sweep)
                        process  = 0
                        pid      = -1
                    else:
                        process  =  self.run_simulation_local(dut, sweep)
                        pid      =  process.pid
                    n +=  1
                    process_running.append(
                        {'n': n, 't0':t0, 'dt':t0, 'dut':dut, 'sweep':sweep,
                        'process':process, 'pid':pid, 'success':True,
                        'backend_remote':dut.simulate_on_server, 'last_poll': 0,
                    })

                #check for finished processes. DO THIS BEFORE TIMEOUT CHECKING.
                for p in process_running:
                    process  =  p['process']
                    if p['backend_remote']:
                        p['last_poll'] += 1
                        if p['last_poll']%20 == 0: # every 20th round -> every 2 seconds (is this too much?)
                            self.copy_from_server(p['dut'], p['sweep'])
                            try:
                                p['dut'].validate_simulation_successful(p['sweep'])
                                process_finished.append(p)
                            except (SimulationUnsuccessful, FileNotFoundError):
                                pass
                    else:
                        returncode = process.poll()
                        if returncode is not None:
                            if returncode != 0 and returncode != 134 and returncode != 139 and returncode !=1: #134 sometimes happens but still ads works...
                                p['success'] = False

                            process_finished.append(p)

                #check for timeouts
                t  =  time.time()
                for p in process_running:
                    p['dt']  =  t - p['t0']
                    if (p['dut'].t_max > self.t_max) and (p['dt'] > self.t_max): # both t_max have to be smaller than the simulation time
                        if not p['backend_remote']:
                            p['process'].kill()
                        p['success'] = False
                        process_finished.append(p)

                #remove finished processes from running processes
                for p in process_finished:
                    if p in process_running:
                        process_running.remove(p)

                #update status that is displayed on the console
                len_progress     =  20 #number of #
                progress         =  int(len(process_finished)/ ( len(sim_list) + len(process_running) + len(process_finished) )*len_progress)
                output_list[0]   =  'DMT is now simulating!         '
                output_list[1]   =  'finished: ' + str(len(process_finished)) + ' of ' + str(n_total) +':[' + '#' * progress + ' ' * (len_progress-progress) + ']'
                output_list[2]   =  '-------------------------------'
                output_list[3]   =  '| sim_n | pid        | dt     |'
                output_list[4]   =  '-------------------------------'
                for i in range(self.n_core):
                    try:
                        p  =  process_running[i]
                        str_='|{:^7d}|{:^12d}|{:^8.1f}|'.format(p['n'], p['pid'], p['dt'])
                    except (KeyError, IndexError):
                        str_='|{:^7s}|{:^12s}|{:^8.1f}|'.format('x', 'x', 0)

                    output_list[i+5]=str_


                output_list[-2]  =  '-------------------------------'
                output_list[-1]  =  '                               '

                #are we finished?
                if len(process_running)  ==  0 and len(sim_list)  ==  0:
                    finished  =  True
                elif len(process_running) == self.n_core or len(sim_list)  ==  0:
                    time.sleep(0.1)

        return process_finished

    def run_simulation_local(self, dut, sweep):
        """ Starts the simulation

        Parameters
        -----------
        dut : DutView
        sweep : Sweep
        """ 
        sim_folder = dut.get_sim_folder(sweep)
        logging.info("Started the simulation for the dut %s of the sweep %s!", dut.get_hash(), sweep.name)
        logging.debug("The simulation folder of this simulation is %s", sim_folder)
        log_file = open(sim_folder/'sim.log', 'w')
        return subprocess.Popen(dut.get_start_sim_command().split(), shell=False, cwd=sim_folder, stderr=subprocess.STDOUT, stdout=log_file)

    def run_simulation_remote(self, dut, sweep):
        """ Starts the remote simulation

        Parameters
        -----------
        dut : DutView
        sweep : Sweep
        """
        sim_folder = dut.get_sim_folder(sweep)

        root, sweep_folder = os.path.split(sim_folder)
        _root, dut_folder = os.path.split(root)

        logging.info("Started the remote simulation for the dut %s of the sweep %s!", dut.get_hash(), sweep.name)
        logging.debug("The simulation folder of this simulation is %s", sim_folder)

        # start a subprocess with the ssh command
        self.ssh_client.exec_command(
            (
                'cd ' + str(DATA_CONFIG['server']['simulation_path'] / dut_folder / sweep_folder) + ';'
                + dut.get_start_sim_command() + ' > sim.log &'
            )
        )