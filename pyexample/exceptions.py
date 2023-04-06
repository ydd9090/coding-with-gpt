import traceback
try:
    a = 1/0
except Exception as e:
    raise Exception("0不能作为除数,error info:\n{}".format(traceback.format_exc()))


