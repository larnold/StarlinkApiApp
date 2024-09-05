import azure.functions as func
import datetime
import json
import logging
import starlink 
import configparser

app = func.FunctionApp()

@app.route(route="StarlinkInfo", auth_level=func.AuthLevel.FUNCTION)
def StarlinkInfo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('StarlinkInfo HTTP trigger: Starting')

    s = starlink.Starlink()
    obj = s.getAllInfo()

    return func.HttpResponse(
        json.dumps(obj),
        mimetype="application/json",
        status_code=200                     
        )


@app.route(route="StarlinkPause", auth_level=func.AuthLevel.FUNCTION)
def StarlinkPause(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('StarlinkPause HTTP trigger: Starting')

    s = starlink.Starlink()
    obj = s.pause(req.params.get('serviceLineNumber'), req.params.get('accountNumber'))

    return func.HttpResponse(
        json.dumps(obj),
        mimetype="application/json",
        status_code=200                     
        )


@app.route(route="StarlinkResume", auth_level=func.AuthLevel.FUNCTION)
def StarlinkResume(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('StarlinkResume HTTP trigger: Starting')

    s = starlink.Starlink()
    obj = s.resume(req.params.get('subscriptionReferenceId'), req.params.get('accountNumber'))

    return func.HttpResponse(
        json.dumps(obj),
        mimetype="application/json",
        status_code=200                     
        )
