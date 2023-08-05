from azureml.core import Workspace, Run, Experiment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.environment import Environment
from azureml.core.model import Model, InferenceConfig
from azureml.core.runconfig import RunConfiguration
from azureml.core.webservice import AksWebservice, AciWebservice, Webservice
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline

import yaml
import io
import argparse
import json
import os
import mlflow


def IfRunInAzureML():
    try:
        run = Run.get_context(allow_offline=False)
    except:
        return False
    
    return run is not None

def RegisterModel(model_path, description, args):

    if IfRunInAzureML():
        experiment = Run.get_context(allow_offline=False).experiment
        ws = experiment.workspace

        Model.register(model_path = model_path,
                       model_name = args.operationId,
                       description = description,
                       workspace = ws,
                       tags={'userId': args.userId, 
                        'productName': args.productName, 
                        'deploymentName': args.deploymentName, 
                        'apiVersion':args.apiVersion,
                        'subscriptionId':args.subscriptionId})
    else:
        print('run on MLflow')
        mlFlowRun = mlflow.active_run()
        print(mlFlowRun)
        if mlFlowRun:
            mlflow.log_artifacts(model_path, model_path)
            model_uri = "runs:/{run_id}/{artifact_path}".format(run_id=mlFlowRun.info.run_id, artifact_path=model_path)
            print(model_uri)
            result = mlflow.register_model(
                model_uri,
                args.operationId
            )
            print(result)

    
def DownloadModel(model_id, model_path):
    if IfRunInAzureML():
        experiment = Run.get_context(allow_offline=False).experiment
        ws = experiment.workspace
        model = Model(ws, model_id)
        model.download(target_dir = model_path, exist_ok=True)

def DownloadOutputFromPredecessorOperation(predecessor_op_id, folder_path):
    return

def GetModelPath():
    # get model path if the model is deployed using AML
    if os.getenv('AZUREML_MODEL_DIR'):
        return os.getenv('AZUREML_MODEL_DIR')

def ParseArguments(run_type):
    parser = argparse.ArgumentParser(run_type)

    parser.add_argument("--runMode", type=str, help="run mode, support azureML or MLflow")
    parser.add_argument("--userInput", type=str, help="input data")
    parser.add_argument("--modelId", type=str, help="model key")

    if run_type == 'inference':
        parser.add_argument("--operationId", type=str, help="run id")
    else:
        parser.add_argument("--userId", type=str, help="user id")
        parser.add_argument("--productName", type=str, help="product name")
        parser.add_argument("--deploymentName", type=str, help="deployment name")
        parser.add_argument("--apiVersion", type=str, help="api version")
        parser.add_argument("--subscriptionId", type=str, help="subscription id")

        if run_type == 'deployment':
            parser.add_argument("--endpointId", type=str, help="endpoint id")

    args = parser.parse_args()
    userInput = json.loads(args.userInput)

    return args, userInput


def Init(luna_config_file='luna_config.yml'):
    with open(luna_config_file) as file:
        luna_config = yaml.full_load(file)
    return luna_config

def GetDeploymentConfig(luna_config, dns_name_label,tags):
    workspace_full_path = os.path.join(luna_config['azureml']['test_workspace_path'], luna_config['azureml']['test_workspace_file_name'])
    with open(workspace_full_path) as file:
        documents = json.load(file)
        deployment_target = documents['DeploymentTarget']
        aks_cluster = documents['AksCluster']


    with open(luna_config['deploy_config']) as file:
        documents = yaml.full_load(file)

        if deployment_target == 'aci':
            deployment_config = AciWebservice.deploy_configuration()
            deployment_config.__dict__.update(documents['azureContainerInstance'])
            deployment_config.dns_name_label = dns_name_label
        elif deployment_target == 'aks':
            deployment_config = AksWebservice.deploy_configuration()
            deployment_config.__dict__.update(documents['kubernetes'])
            deployment_config.compute_target_name = aks_cluster
            deployment_config.namespace = dns_name_label

        deployment_config.tags = tags
    return deployment_config

def DeployModel():

    luna_config = Init()

    args, userInput = ParseArguments("deployment")

    dns_name_label = userInput["dns_name_label"]
    model_id = args.predecessorOperationId
    endpoint_id = args.operationId

    print(dns_name_label)

    ## If it is running in AML context
    if IfRunInAzureML():
        experiment = Run.get_context(allow_offline=False).experiment
        ws = experiment.workspace
        model = Model(ws, model_id)

        myenv = Environment.from_conda_specification('scoring', luna_config['conda_env'])

        inference_config = InferenceConfig(entry_script=luna_config['code']['inference_entry_script'], source_directory = os.getcwd(), environment=myenv)

        deployment_config = GetDeploymentConfig(
            luna_config, 
            dns_name_label,
            tags={'userId': args.userId, 
                'productName': args.productName, 
                'deploymentName': args.deploymentName, 
                'apiVersion':args.apiVersion,
                'subscriptionId':args.subscriptionId})
        
        service = Model.deploy(ws, endpoint_id, [model], inference_config, deployment_config)
        service.wait_for_deployment(show_output = True)

def RunProject(azureml_workspace, entry_point, experiment_name, parameters, tags, compute_cluster="default", luna_config_file='luna_config.yml'):

    luna_config = Init(luna_config_file)
    if azureml_workspace:
        run_config = RunConfiguration.load(luna_config['azureml']['run_config'])

        if compute_cluster == "default":
            workspace_full_path = os.path.join(luna_config['azureml']['test_workspace_path'], luna_config['azureml']['test_workspace_file_name'])
            with open(workspace_full_path) as file:
                documents = json.load(file)
                aml_compute = documents['AmlCompute']
                run_config.target = aml_compute
        else:
            run_config.target = compute_cluster

        arguments = GetPipelineArguments(luna_config['MLproject'], entry_point, parameters)

        entry_point_script = GetEntryPointScriptPath(luna_config['MLproject'], entry_point)

        trainStep = PythonScriptStep(
            script_name=entry_point_script,
            arguments=arguments,
            inputs=[],
            outputs=[],
            source_directory=os.getcwd(),
            runconfig=run_config,
            allow_reuse=False
        )

        pipeline = Pipeline(workspace=azureml_workspace, steps=[trainStep])

        experiment = Experiment(azureml_workspace, experiment_name)
        pipeline_run = experiment.submit(pipeline, tags=tags)
        return pipeline_run.id
    
    else:
        return '00000000-0000-0000-0000-000000000000'

def PublishAMLPipeline(azureml_workspace, entry_point, name, description, parameters={}, luna_config_file='luna_config.yml'):
    luna_config = Init(luna_config_file)
    if azureml_workspace:
        run_config = RunConfiguration.load(luna_config['azureml']['run_config'])

        arguments = GetPipelineArguments(luna_config['MLproject'], entry_point, parameters)
        entry_point_script = GetEntryPointScriptPath(luna_config['MLproject'], entry_point)
        trainStep = PythonScriptStep(
            script_name=entry_point_script,
            arguments=arguments,
            inputs=[],
            outputs=[],
            source_directory=os.getcwd(),
            runconfig=run_config
        )

        pipeline = Pipeline(workspace=azureml_workspace, steps=[trainStep])
        published_pipeline = pipeline.publish(name=name, description=description)
        return published_pipeline.endpoint

def GetPipelineArguments(mlproject_file_path, run_type, parameters):
    with open(mlproject_file_path) as file:
        documents = yaml.full_load(file)
        arguments = []
        for param in documents['entry_points'][run_type]['parameters']:
            argumentName = '--' + param
            arguments.append(argumentName)
            # get input parameter values, set default value if not provided
            if param in parameters:
                pipelineParam = PipelineParameter(name=param, default_value=parameters[param])
            else:
                pipelineParam = PipelineParameter(name=param, default_value=documents['entry_points'][run_type]['parameters'][param]['default'])
            arguments.append(pipelineParam)
        return arguments

def GetEntryPointScriptPath(mlproject_file_path, entry_point):
    with open(mlproject_file_path) as file:
        documents = yaml.full_load(file)
        command = documents['entry_points'][entry_point]['command']
        script_path = command.split(" ")[1]
        return script_path

def GetOperationNameByVerb(operationVerb):
    
    luna_config = Init()
    with open(luna_config['MLproject']) as file:
        documents = yaml.full_load(file)
        for operation in documents['entry_points']:
            if documents['entry_points'][operation]['verb'] == operationVerb:
                return operation

    return None


def GetOperationNameByNoun(operationNoun):
    
    luna_config = Init()
    with open(luna_config['MLproject']) as file:
        documents = yaml.full_load(file)
        for operation in documents['entry_points']:
            if documents['entry_points'][operation]['noun'] == operationNoun:
                return operation

    return None


def GetOutputType(operationName):
    
    luna_config = Init()
    with open(luna_config['MLproject']) as file:
        documents = yaml.full_load(file)
        return documents['entry_points'][operationName]['output']