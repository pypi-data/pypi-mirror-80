from . import __GamayunResult_pb2_grpc as GamayunResult_pb2_grpc
from . import __GamayunResult_pb2 as GamayunResult_pb2
import grpc
import traceback
import os

def report_result(results):
    job_name = __get_job_name()
    channel = grpc.insecure_channel('localhost:16656')
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    res = GamayunResult_pb2.JobResult(name = job_name, results = results)
    stub.ReportResult(res)

def report_error(error):
    job_name = __get_job_name()
    channel = grpc.insecure_channel('localhost:16656')
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    err = GamayunResult_pb2.JobError(name = job_name, error = error)
    stub.ReportError(err)

def __report_non_job_specific_error(error):
    job_name = "Gamayun generic error"
    channel = grpc.insecure_channel('localhost:16656')
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    err = GamayunResult_pb2.JobError(name = job_name, error = error)
    stub.ReportError(err)

def __get_job_name():
    try:
        return os.environ["GAMAYUN_JOB_NAME"]
    except:
        __report_non_job_specific_error("Cannot find GAMAYUN_JOB_NAME in environment, script cannot execute!")
        raise

def run_gamayun_script_logic(callback):
    try:
        callback()
    except:
        report_error(traceback.format_exc())