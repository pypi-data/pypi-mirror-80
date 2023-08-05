#################################################################
# Optimisation contains the Optimisation Class to use CPLEX
#################################################################

# Import python modules
import os
import cplex as cp
import docplex as dp
import subprocess as sp
from ibm_watson_machine_learning import APIClient
import tarfile as tf
import time


# Begin class breakdown
class Optimisation:
    """ Prepare and runs optimisation with IBM ILOG CPLEX Optimisation Studio
    """
    def __init__(self):
        """ Initialise the optimisation class
        """

    def use_bash_shell(self, command):
        """ Execute bash commands in python scripts

        Args:
            command (str): Command to execute
        """
        # Execute the demand
        sp.Popen([['/bin/bash', '-c', command]])

    def create_linear_programme_file(self, directory, data_file, model_file,
                                     output_file):
        """ Creates the model file through executing model system commands

            Args:
                directory (str): Name of directory to put data into
                data_file (str): Name of energy system data file
                model_file (str): Name of energy system model file
                output_file (str): Name of output linear programme
            """
        # Change the working directory
        os.chdir(directory)
        # Load the custom anaconda environment
        # This assumes the conda environment has already been initialised.
        os.system('conda activate osemosys')
        # Execute the file structure to create the linear programming file
        # (glpsol -m GOCPI_Model.txt -d GOCPI_Data.txt --wlp GOCPI.lp)
        command = 'glpsol -m ' + data_file + ' -d ' + model_file + '--wlp ' + output_file
        os.system(command)

    def run_cplex_local(self, model_file):
        """ This function runs cplex on the local device if the energy system
            is of a small enough complexity
        """
        # Creates the model structure
        model = cp.Cplex()
        # Produces the results stream and log streams
        output = model.set_results_stream(None)
        output = model.set_log_stream(None)
        # Write the energy system model to Cplex
        model.read(model_file)
        # Solve the model using the version of Cplex installed on the local
        # device (IBM ILOG CPLEX Optimisation Studio)
        model.solve()
        # Return the value of the objective function
        objective_value = model.solution.get_objective_value()
        return objective_value

    def run_ibm_wml_do(self, apikey, url, deployment_space_name,
                       cloud_object_storage_credential, service_instance_id,
                       deployment_space_exists, data_assets_exist,
                       data_asset_dictionary, model_name, model_type,
                       model_runtime_uid, model_tar_file, num_nodes,
                       deployment_exists, payload_input_data_id,
                       payload_input_data_file, payload_output_data_id):
        """ This function enables the user to solve python-based
            optimisation models. The legacy offering
            to solve optimisation models on IBM cloud was using
            the docplex python api to run Cplex on DOcloud. 
            As of September 2020, the DOcloud 
            was discontinued with Decision Optimisation
            functionalities imported to IBM's Watson Machine 
            Learning Service. The new process requires the
            energy system model to be written in python. This 
            project saw the implementation of the osemosys 
            modelling methodology in GNU Mathprog written into
            LP Files. IBM Decision Optimisation in cannot deploy 
            models in LP File formats to get jobs. Therefore,
            this function is for future work in converting the
            entire energy system modelling tool to python-based only.
            This is well-documented the report in the Future Work
            Section. Note: You must have access to IBM Watson Studio
            and Cloud Products through the IBM Academic Initiative or
            Similar.

        Args:
            apikey (str): API key from user's IBM Cloud Account
            url ([type]): URL for the server the user is using for the IBM services
            deployment_space_name (str): Name of the deployment space
            cloud_object_storage_credential (str): Credential for the cloud object storage asset
            service_instance_id (str): Service instance id for the service being used (IBM WML)
            deployment_space_exists (boolean): True/False if the deployment space already exists
            data_assets_exist (boolean): True/False if the data assets (e.g. input data stored on cloud)
            data_asset_dictionary (dict): A dictionary of data assets to stored on IBM cloud
            model_name (str): Name of the model
            model_type (str): Name of the model
            model_runtime_uid (str): Runtime ID for the model
            model_tar_file (tar): Tar file containing the python model
            num_nodes (int): Number of nodes the model is run off.
            deployment_exists (boolean): True/False if the deployment already exists
            payload_input_data_id (str): Name of input data
            payload_input_data_file (dataframe): Input data file in the form of a dataframe
            payload_output_data_id (str): Name of output data file
        """

        # Creates the Watson Machine learning Credientials
        api_wml_credentials = {
            # IBM Cloud User Account Access Code
            "apikey": apikey,
            # Url to code repository
            "url": url
        }
        # Initials the clent credientials
        client = APIClient(api_wml_credentials)

        # Create a deployment space on the IBM Cloud Service
        space_metadata = {
            # Configures deployment space name
            client.spaces.ConfigurationMetaNames.NAME:
            deployment_space_name,
            # Configures deployment space description
            client.spaces.ConfigurationMetaNames.DESCRIPTION:
            deployment_space_name + ' Deployment for energy systems models',
            # Configures deployment space storage location
            client.spaces.ConfigurationMetaNames.STORAGE: {
                "type": "bmcos_object_storage",
                "resource_crn": cloud_object_storage_credential
            },
            # Configures deployment
            client.spaces.ConfigurationMetaNames.COMPUTE: {
                "name": "existing_instance_id",
                "crn": service_instance_id
            }
        }
        # Bypasses the creation of the deployment space if is already exists
        if deployment_space_exists == True:
            client.spaces.list()
            # Asks user to input the Space ID of the Input Space
            space_id = input('Please input the Space ID: ')
        else:
            # Stores the newly created space in the depositories spaces list
            space = client.spaces.store(meta_props=space_metadata)
            space_id = client.spaces.get_id(space)

        # Sets the client space
        client.set.default_space(space_id)

        # Creates input and output data assets if they don't exist
        if data_assets_exist == False:
            # Loop through dictionary of data assets to create
            for key in data_asset_dictionary:
                client.data_assets.create(key, data_asset_dictionary[key])

        # Creates software mane and specification for the deployment
        client.software_specifications.list()
        software_name = input("Please Input Software Name: ")
        software_spec_uid = client.software_specifications.get_uid_by_name(
            software_name)

        # Creates the model deployment
        model_metadata = {
            client.repository.ModelMetaNames.NAME: model_name,
            client.repository.ModelMetaNames.DESCRIPTION: model_name + 'Model',
            client.repository.ModelMetaNames.TYPE: model_type,
            client.repository.ModelMetaNames.RUNTIME_UID: model_runtime_uid,
            client.repository.ModelMetaNames.SOFTWARE_SPEC_UID:
            software_spec_uid
        }
        # Creates the energy model details
        model_details = client.repository.store_model(
            model=model_tar_file, meta_props=model_metadata)
        # Creates model uid
        model_uid = client.repository.get_model_uid(model_details)

        # Creates a deployment
        meta_props = {
            client.deployments.ConfigurationMetaNames.NAME:
            "Deployment " + str(num_nodes),
            client.deployments.ConfigurationMetaNames.DESCRIPTION:
            "Deployment " + str(num_nodes),
            # client.deployments.ConfigurationMetaNames.HARDWARE_SPEC:
            client.deployments.ConfigurationMetaNames.BATCH: {},
            client.deployments.ConfigurationMetaNames.COMPUTE: {
                'name': 'S',
                'nodes': num_nodes
            }
        }

        # Tests if deployment already exists
        if deployment_exists == True:
            client.deployments.list()
            deployment_uid = input('Please input the Deployment UID: ')
        else:
            deployment_details = client.deployments.create(
                model_uid, meta_props=meta_props)
            deployment_uid = client.deployments.get_uid(deployment_details)

        # Creates a payload for the solver to solve (Note: Ammend based on the model you are solving)
        payload = {
            client.deployments.DecisionOptimizationMetaNames.INPUT_DATA: [{
                "id":
                payload_input_data_id,
                "values":
                payload_input_data_file
            }],
            client.deployments.DecisionOptimizationMetaNames.OUTPUT_DATA: [{
                "id":
                payload_output_data_id
            }]
        }

        # Creates a new job using the deployment and payload
        job_details = client.deployments.create_job(deployment_uid, payload)
        job_uid = client.deployments.get_job_uid(job_details)

        # Print the status of the job until competition
        while job_details['entity']['decision_optimization']['status'][
                'state'] not in ['completed', 'failed', 'canceled']:
            print(job_details['entity']['decision_optimization']['status']
                  ['state'] + '...')
            job_details = client.deployments.get_job_details(job_uid)
            time.sleep(5)
            print(job_details['entity']['decision_optimization']['status']
                  ['state'])

    # Reset tarfile function (Source: IBM Watson Machine Learning)
    def reset(self, tarinfo):
        """ Resets the tarfile information when creating tar files
            This is to input into the filter when using tar.add()

        Args:
            tarinfo (Object): Tar Object containing an ID of 0 and the root as the name

        Returns:
            tarinfo (Object): Tar Object containing an ID of 0 and the root as the name
        """
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "root"
        return tarinfo
