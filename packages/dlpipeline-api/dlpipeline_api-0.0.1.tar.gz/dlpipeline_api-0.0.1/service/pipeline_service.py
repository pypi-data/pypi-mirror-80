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
    kfp.compiler.Compiler().compile(packaging, 'ano_detection_pipeline_cnn.zip')

#During model upload or rather configure model step apart from usual parameter capturing for selected ml model
# ,only extra thing that happens
# in contrast to now is attaching the definition to it based on the selected product segment/domain
#During model deployment as usual the model gets deployed for each instance and after the model deployment
# the endpoint name is
# available
#once all info which is needed for pipeline is available,after deployment an experiment will be created and the exp info
#,workflow def(based on which prod model it belongs to)+arguments will be attached to each instance
#during prediction/serving based on instance in question the above info is pulled and pipeline is executed
def run_workflow():
    client = kfp.Client()
    cnnnab_exp = client.create_experiment(name='tsanodetc')
    arguments = {"window_size": 288,
                 "key_id": 'ASIA6PVYLLNPROFL3LXZ',
                 "key":'z1khyGEqWRPoIyvbFMIuv0hFbTgNZLj1/bApLm/t',
                 "token":'IQoJb3JpZ2luX2VjEFEaCXVzLWVhc3QtMSJGMEQCID10wC+OQb9d9Zcw6lFCSy0+YrEwXY62pxLDF1DkjFXQAiB779QDf8bKOmc1ev2f1asKXxMQtJkSVG8W69+MaS+4PCrVAghqEAAaDDk5NTc0NTI5MTEwMyIMFdHtU3rLqGu4TmLRKrICdW9Y8RCWKrgJfQf4kPkA31i45Z0UEjmigfH1TwSZ4YVsy70lQEg9iOGj2z6Rkr8auuuSgUO/+Q+Ud3fTN+2XG935xRnlnJafoWx9vWCPyOCFpCKbOtk90g5h1qSx6n/eSkY8fNxYT0HnTSFm6+srA/lNvT1yZNVEGmVKGk3xvmZhNqhDftfAkg4YHRrNhHq8Ad2Mw/fCFsJvZDBcvqY9ZRWGuR/SVuY6IDnTycwpsn0XK42GFR1aROFsriwy9rVb3PHa6cTIL2Xv3S0rIQP3gfoq5dFBjOaNg8tnSxRpQz/hpWX2Unbuzr2JzZqhh2p0QgumQOtyV8Wuj5o7TQKpCeDcssaHH7m44zAzAaiY6MqwQn+GHUnnbHKfElF2KuHOqDLuvqOzcwy1Vif5oEVkI1hrMLP0n/sFOqQBGVrA4dHAK7ozLu9i0CDeeH6mRjLq+3Oo0ASzR9Hk+f4bnfd3uSD9NtesHP+H7hyXTuYtir2jW117SqcAGT2hOAlX9HWSlwqT1KNNK30N7ePTcxQVK90+bhgPmPb7QkrUwsfVbhVlyYZNkHjPDh0pbmmJ+zsChSHQ1PfbOVGAK5kG9Iuig/r5e0ukPyCli2qlPGpO7CGOHarLy64V3HKWi+WSzyc=',
                 "endpoint":'TSNABANODET-end-point'}
    cnnnab_exp_run = client.run_pipeline(
                    experiment_id=cnnnab_exp.id,
                    job_name='ano_detection_pipeline_cnn',
                    pipeline_package_path='ano_detection_pipeline_cnn.zip',
                    params=arguments)

    print('successfully triggered workflow')

def upload_workflow():
    s3 = boto3.client("s3",
                      aws_access_key_id='ASIA6PVYLLNP5TOOSTOF',
                      aws_secret_access_key='tl086Sqnr1jVvCDTXbyHEDpO8hEJ3ag95RQTmIqe',
                      aws_session_token='IQoJb3JpZ2luX2VjEA4aCXVzLWVhc3QtMSJGMEQCIES/1pEpvbIqoIqozxkqa+Jw+TLgUQNje4OHDVEay15FAiAbKKgndQgEJfvI8+yQ7l8RRMzDlsBbaOCBfXB4LH1/8SrVAggnEAAaDDk5NTc0NTI5MTEwMyIMeLMsf28r/f8GWgesKrICYzybz21R25eWfcU/TwbdimZfPT16F2bZhrSBpR7099lgc/PwMfdKs03hszpNhMI79O/ckG1cx4G5xCc19f2bI3B5SkH4doBbeeaDoSErlOdiLO6VAGs/zOnBM+qDiKfx2tV4J8cEflNGc6i/KAEME2NNmgPz15cqud//w9TFaVTDB+l3rgzAKIpRFXzlenIP8Yj+4mQxyokCunkzjda0gCjditYQaDGirr85Jf+TFeseRQ9cgYT/jJsEzKfhvye6i32MiAAkAX16jX6qm6QQ3hg10sX+G1RxJ+Ux4TkkG2wMq0grbKtAhj3RlOVYh/tGrW1fNYFrgrbyInNUZOV12P8H+jyfFw54qHMwZ+XLMvn8LTfqPwf0ro892xRkXFa53nJpg1SMfDYjRRy5Yl1ypKadMMuVkfsFOqQBHZocKVyPejwFnSo5wqSPySyU3KR+9ERqKbIHhVyOdGIuV2NU44rh/MxCiX2r0pfa+sQredj4P7UW02wljXI+gXIWH8jzOdISb1Pano6MuTcghHb6/cSsYwygpUTbF1k4CvWARaRTFzFiKuXd+22v9HIZg8X23OPSkWqXkx1fmmSX/IA09/CEbf1ZkGwAKgZTBGF4H4lmnIxNYukcMNX0u5P+tvc='
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

        location = "{}{}".format('s3://{}/'.format('995745291103-devdemo-analytics-model-deployment'), 'ano_detection_pipeline_cnn' + ".zip")
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