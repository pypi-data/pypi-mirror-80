#!/usr/bin/python

import time

# Import OKAPI routines. If you use the script with OKAPI installed by PIP,
# adapt it (see below)
from okapi_init import okapi_init
from okapi_send_request import okapi_send_request
from okapi_get_result import okapi_get_result
from okapi_wait_and_get_result import okapi_wait_and_get_result
from okapi_send_request_and_wait_for_result import okapi_send_request_and_wait_for_result
from okapi_add_object import okapi_add_object
from okapi_change_object import okapi_change_object
from okapi_delete_object import okapi_delete_object
from okapi_get_objects import okapi_get_objects

# when using OKAPI installed with PIP:
# from okapi_pkg.okapi_init import okapi_init
# from okapi_pkg.okapi_send_request import okapi_send_request
# from okapi_pkg.okapi_get_result import okapi_get_result
# from okapi_pkg.okapi_wait_and_get_result import okapi_wait_and_get_result
# from okapi_pkg.okapi_send_request_and_wait_for_result import okapi_send_request_and_wait_for_result
# from okapi_pkg.okapi_add_object import okapi_add_object
# from okapi_pkg.okapi_change_object import okapi_change_object
# from okapi_pkg.okapi_delete_object import okapi_delete_object
# from okapi_pkg.okapi_get_objects import okapi_get_objects

#
# Init --> Get a token to run the analyses
#
# For auth info: See www.okapiorbits.space or contact us. Standard url is: https://platform.okapiorbits.com/api/
okapi_login, error = okapi_init("https://platform.okapiorbits.com/api/",
                                "jonas.radtke@okapiorbits.com",
                                "g+s\?gi%vUp=/C$4+'%t")

# check for the error status
if (error.get('status','') == 'FATAL'):
    print(error)
    exit('Error during authentification.')
# print(okapi_login)

#
# Pass predictions
#

#
# # Prepare your request
# pass_pred_request_body = {
#     "orbit":{
#       "type": "tle.txt",
#       "content": "1 25544U 98067A   18218.76369510  .00001449  00000-0  29472-4 0  9993\n2 25544  51.6423 126.6422 0005481  33.3092  62.9075 15.53806849126382"
#     },
#     "ground_location": {
#       "type": "ground_loc.json",
#       "content": {
#         "altitude": 0.17012,
#         "longitude": 10.07,
#         "latitude": 50.2
#       }
#     },
#     "time_window": {
#       "type": "tw.json",
#       "content": {
#         "start": "2018-08-07T18:00:00.000Z",
#         "end": "2018-08-08T00:00:00.000Z"
#       }
#     }
# }

# #
# # # send different pass prediction pass prediction requests, use the bare functions to send and get results
# #
# # # send a request to use SGP4 for pass prediction
# request_sgp4, error = okapi_send_request(okapi_login, pass_pred_request_body,
#                                          'predict-passes/sgp4/requests')
# if (error.get('status','') == 'FATAL'):
#     print(error)
#     exit()

# # loop until the result has been fully processed. Alternatively, you could
# # also just "sleep" for a while
# counter = 0
# while ((counter < 15) and (error.get('web_status','') == 202)):

#   # get the result from SGP4
#   result_sgp4, error = okapi_get_result(okapi_login, request_sgp4,
#                                         'predict-passes/sgp4/results/{}/simple')

#   if (error.get('status','') == 'FATAL'):
#       print(error)
#       exit()
#   elif(error.get('status','') == 'WARNING'):
#       print(error)

#   counter = counter + 1

# # print(result_sgp4)


# #
# # # First alternative: Send the result yourself, but use a dedicated function to wait for and get the result
# #
# # # send a request to use SGP4 for pass prediction
# request_sgp4, error = okapi_send_request(okapi_login, pass_pred_request_body,
#                                          'predict-passes/sgp4/requests')
# if (error.get('status','') == 'FATAL'):
#     print(error)
#     exit()

# # call the function to wait for and get the result
# result_sgp4, error = okapi_wait_and_get_result(okapi_login, request_sgp4,
#                                       'predict-passes/sgp4/results/{}/simple', 15)

# if (error.get('status','') == 'FATAL'):
#     print(error)
#     exit()
# elif(error.get('status','') == 'WARNING'):
#     print(error)

# # print(result_sgp4)

# #
# # # Third alternative: Use a function to send, wait-for and get the result. Note that this might block your code while running
# #
# # # send a request to use SGP4 for pass prediction
# result_sgp4, error = okapi_send_request_and_wait_for_result(okapi_login, pass_pred_request_body,
#                                       'predict-passes/sgp4/requests',
#                                       'predict-passes/sgp4/results/{}/simple', 15)

# if (error.get('status','') == 'FATAL'):
#     print(error)
#     exit()
# elif(error.get('status','') == 'WARNING'):
#     print(error)

#
# Get all the satellites
#
satellites, error = okapi_get_objects(okapi_login,'satellites')

#
# Get all conjunctions
#
conjunctions, error = okapi_get_objects(okapi_login,'conjunctions')

#
# Get the CDMs for a conjunction
#
cdms, error = okapi_get_objects(okapi_login,'conjunctions/{}/cdms', conjunctions["elements"][0]["conjunction_id"])

# get all maneuver evals for that conjunction
maneuvers, error = okapi_get_objects(okapi_login,'conjunctions/{}/maneuver-evals', conjunctions["elements"][0]["conjunction_id"])
print(maneuvers)