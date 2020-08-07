def extract_data(parameters):
    result=dict()
    for param in parameters:
        if 'value' in param:
            result[param['name']] = param[value]
    return result


def extract_other(paramteres):
    url_type = list()
    for param in parameters:
        if 'value' in param:
            url_type = param['value']
    return url_type


