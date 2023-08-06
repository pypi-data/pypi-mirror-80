import kfp
from kfp import components
from kfp import dsl
from kfp.dsl import ContainerOp
from anodetection.car_workflow import create_workflow
import requests
import uuid
import boto3


@kfp.dsl.pipeline(
  name='AnoDetPipeline1',
  description='AnoDetPipeline1'
)
def packaging(window_size:int = 1,key_id:str = 'alpha',key:str = 'beta',token:str = 'gama',endpoint:str = 'delta'):
    return create_workflow(window_size,key_id,key,token,endpoint)

#Happens outside UPA UI
def createPackage():
    kfp.compiler.Compiler().compile(packaging, 'anomaly_detection_workflow_definition.zip')

#During model upload or rather configure model step apart from usual parameter capturing for selected ml model
# ,only extra thing that happens
# in contrast to now is attaching the definition to it based on the selected product segment/domain
#During model deployment as usual the model gets deployed for each instance and after the model deployment
# the endpoint name is
# available
#once all info which is needed for pipeline is available,after deployment an experiment will be created and the exp info
#,workflow def(based on which prod model it belongs to)+arguments or model pramas will be attached to each instance
#during prediction/serving based on instance in question the above info is pulled and pipeline execution is triggered
def run_workflow(key_id,key,token,window_size,endpoint,exp_name,run_name):
    client = kfp.Client()
    cnnnab_exp = client.create_experiment(name=exp_name)
    arguments = {"window_size": window_size,
                 "key_id": key_id,
                 "key":key,
                 "token":token,
                 "endpoint":endpoint}
    #in actual scenario the pipeline definition zip file will not be hardcoded but will be downloaded
    #from the s3 location based on the passed details
    cnnnab_exp_run = client.run_pipeline(
                    experiment_id=cnnnab_exp.id,
                    job_name=run_name,
                    pipeline_package_path='anomaly_detection_workflow_definition.zip',
                    params=arguments)

    print('successfully triggered workflow')

def upload_workflow(key_id,key,token):
    s3 = boto3.client("s3",
                      aws_access_key_id=key_id,
                      aws_secret_access_key=key,
                      aws_session_token=token
                      )
    acl = 'public-read'
    bucket_name = '995745291103-devdemo-analytics-model-deployment'
    ml_model_file = open('ano_detection_pipeline_cnn.zip', 'rb+')

    # key = str(uuid.uuid4())
    file_name = 'anomaly_detection_workflow_definition' + ".zip"
    try:
        s3.put_object(
            Body=ml_model_file,
            Bucket=bucket_name,
            Key=file_name,
            ACL=acl,
            ContentType="application/zip"
        )
        print("233")
    except Exception as e:
        print(e)

    print("{}{}".format('s3://{}/'.format(bucket_name), file_name))

def provision_workflow_definition():

    try:
        wflow_def = get_workflow_Definition('anomalydetection')
        pipeline_id = ''
        if len(wflow_def) != 0:
            if wflow_def['workflowId']:
                pipeline_id = wflow_def['workflowId']
            else:
                pipeline_id = str(uuid.uuid4())

        location = "{}{}".format('s3://{}/'.format('995745291103-devdemo-analytics-model-deployment'), 'anomaly_detection_workflow_definition' + ".zip")
        _data = '{"Name":"' + 'anomalydetection' + '","PipelineId": "' + pipeline_id + '","Client":"' + 'Uptime' + '","Meta_pipeline_def": "' + location + '","Env": "' +'Development'+'","Status": "' +'Active'+'"}'
        print(_data)
        headers = {"content-type": "application/json"}
        _response = requests.post('https://724tnwvjm8.execute-api.eu-west-1.amazonaws.com/dev/rest/v1/uptime/pipeline',
                                  data=_data,
                                  headers=headers)

        _res_dict = _response.json()
        print(_res_dict)
    except Exception:
        print('Error in getting data from consumer ')
        raise Exception

def get_workflow_Definition(name):
    wflow_def_resp = requests.get(
        'https://724tnwvjm8.execute-api.eu-west-1.amazonaws.com/dev/rest/v1/uptime/pipeline')
    wflow_def_resp_list = wflow_def_resp.json()
    print(type(wflow_def_resp_list))
    _wflow_def_data = {}
    for wflo_def in wflow_def_resp_list:
        if wflo_def['Name'] == name:
            print(wflo_def['Name'])
            _wflow_def_data = {
                'workflowId': wflo_def['PipelineId'],
                'workflowName': wflo_def['Name'],
                'workflowloc': wflo_def['Meta_pipeline_def']
            }
    return _wflow_def_data;

createPackage()