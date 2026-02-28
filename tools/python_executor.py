import traceback

def execute_python(code:str):
    try:
        local_scope={}
        exec(code,{},local_scope)
        return {
            "success":True,
            "output":local_scope
        }
    except Exception as e:
        return {
            "success":False,
            "error":str(e),
            "traceback":traceback.format_exc()
        }
