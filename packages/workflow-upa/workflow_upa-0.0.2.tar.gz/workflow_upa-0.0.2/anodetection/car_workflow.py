import json
import kfp
from kfp import components
from kfp import dsl
import os
import requests
import uuid
import boto3
import pandas
import numpy

data_fetch_comp_resp = requests.get('https://glb6erqwgd.execute-api.eu-west-1.amazonaws.com/dev/rest/v1/uptime/component/datafetch')
_data_fetch_comp_res_dict = data_fetch_comp_resp.json()
print(_data_fetch_comp_res_dict['Comp_container_loc'])

pred_serv_comp_resp = requests.get('https://glb6erqwgd.execute-api.eu-west-1.amazonaws.com/dev/rest/v1/uptime/component/predictionserving')
pred_serv_comp_resp_dict = pred_serv_comp_resp.json()
print(pred_serv_comp_resp_dict['Comp_container_loc'])

#datafetc_comp_op = components.load_component_from_url('https://raw.githubusercontent.com/igw2014/poc/master/component.yaml')
#sagemaker_predictor_comp_op = components.load_component_from_url('https://raw.githubusercontent.com/igw2014/smpredictor/master/component.yaml')
datafetc_comp_op = components.load_component_from_url(_data_fetch_comp_res_dict['Comp_container_loc'])
sagemaker_predictor_comp_op = components.load_component_from_url(pred_serv_comp_resp_dict['Comp_container_loc'])

def create_workflow(window_size,key_id,key,token,endpoint):
  df_fe_win_step = datafetc_comp_op(
      window_size=window_size,
      aws_access_key_id=key_id,
      aws_secret_access_key=key,
      aws_session_token=token,
      input_file_path='s3://995745291103-devdemo-analytics-model-deployment'
  )

  sm_prediction_step = sagemaker_predictor_comp_op(
      input_file_name='input.pkl',
      endpoint_name=endpoint,
      aws_access_key_id=key_id,
      aws_secret_access_key=key,
      aws_session_token=token
  ).after(df_fe_win_step).set_display_name('Sagemaker Predictor')

  return sm_prediction_step