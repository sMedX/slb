import aiohttp.web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import logging
import pandas as pd
import numpy as np

log = logging.getLogger(__name__)


async def get_attributes_handler(request: Request) -> Response:
    log.debug('Start get_attributes_handler')

    ia_df = request.app['data']['ia_df']

    reverse_rename = {'WETTED_MATERIAL': 'ACTIVE FLOW WETTED MATERIAL - YIELD STRENGTH (KSI)',
                      'CASING_SIZE': 'CASING SIZE (IN)',
                      'WEIGHT_RANGE': 'CASING WEIGHT RANGE (PPF)',
                      'CERTIFICATION': 'CERTIFICATION STATUS',
                      'PRESSURE_RATING': 'DIFFERENTIAL PRESSURE RATING (PSI)',
                      'EXTERNAL_PRESSURE': 'EXTERNAL WORKING PRESSURE (PSI) - EOEC AT SPECIFIED TEMP (F)',
                      'ID_DRIFT': 'I.D. - DRIFT (IN)',
                      'INTERNAL_PRESSURE': 'INTERNAL WORKING PRESSURE (PSI) - EOEC AT SPECIFIED TEMP (F)',
                      'LOWER_THREAD': 'LOWER THREAD CONNECTING - SIZE (IN), WT (PPF), TYPE, CONFIG',
                      'MATERIAL_ELEMENTS': 'MATERIAL/ELEMENTS',
                      'MATERIAL_O_RING': 'MATERIAL/O-RING(S)',
                      'OD_MAX': 'O.D. - MAX. (IN)',
                      'QCG': 'QUALITY CONTROL GRADE',
                      'QCP': 'QUALITY CONTROL PLAN - QCP',
                      'SERVICE_NACE': 'SERVICE NACE (YES/NO)',
                      'SETTING_PRESSURE': 'SETTING DIFFERENTIAL PRESSURE - RECOMMENDED (MIN)(PSI)',
                      'RELEASE_FORCE': 'SHEAR RELEASE FORCE (LB)',
                      'TENSILE_STRENGTH': 'TENSILE STRENGTH (LBS) - EOEC AT SPECIFIED TEMP (F)',
                      'UPPER_THREAD': 'UPPER THREAD CONNECTING - SIZE (IN), WT (PPF), TYPE, CONFIG'}

    result = {}

    for col in ia_df.columns:
        main_col = col[0]
        sub_col = col[1]
        if main_col not in result:
            result[main_col] = {}

        result[main_col][sub_col] = {}
        result[main_col]['name'] = reverse_rename[main_col]

        if ia_df[col].dtype == 'object':
            result[main_col][sub_col]['type'] = 'string'
        else:
            result[main_col][sub_col]['type'] = str(ia_df[col].dtype)

        if ia_df[col].dtype == 'float64':
            result[main_col][sub_col]['min'] = str(np.min(ia_df[col]))
            result[main_col][sub_col]['max'] = str(np.max(ia_df[col]))
        else:
            result[main_col][sub_col]['values'] = [str(val) for val in ia_df[col].unique()]

    return aiohttp.web.json_response(result, status=200)


async def filter_packers_by_ied_handler(request: Request) -> Response:
    log.debug('Start filter_packers_by_ied_handler')

    # reading and checking request data
    if not request.body_exists:
        message = 'Request Body is empty'
        log.error("Error during filtering packers: %s", message)
        return aiohttp.web.json_response({'message': message}, status=400)

    # reading and checking request data
    if not request.can_read_body:
        message = "Can't read Request Body"
        log.error("Error during filtering packers: %s", message)
        return aiohttp.web.json_response({'message': message}, status=400)

    # user_ia = await request.json()

    # if len(user_ia) == 0:
    #     message = 'No attributes set'
    #     log.error("Error during filtering packers: %s", message)
    #     return aiohttp.web.json_response({'message': message}, status=400)

    # domains and features should be unique to be able to used as keys
    ia_df = request.app['data']['ia_df']
    attributes = request.app['config']['attributes']

    ia_df_filter_result = pd.DataFrame().reindex_like(ia_df)

    # # Так задаем правила фильтра
    # ia_rules = {('WETTED_MATERIAL', 'MATERIAL'): 'ia_df.WETTED_MATERIAL.MATERIAL == x',
    #             ('CASING_SIZE', 'value'): 'ia_df.CASING_SIZE.value <= x',
    #             ('WEIGHT_RANGE', 'MAX'): 'ia_df.WEIGHT_RANGE.MAX >= x',
    #             ('WEIGHT_RANGE', 'MIN'): 'ia_df.WEIGHT_RANGE.MIN <= x'}

    # Так задаем параметры от пользователя
    user_ia = {('WETTED_MATERIAL', 'MATERIAL'): '41XX',
               ('CASING_SIZE', 'value'): 7.0,
               ('WEIGHT_RANGE', 'MAX'): 25,
               ('WEIGHT_RANGE', 'MIN'): 24}

    ia_criteries = []

    for key, x in user_ia.items():
        if key[0] in attributes and key[1] in attributes[key[0]]:
            rule = attributes[key[0]][key[1]]['rule']
            ia_df_filter_result[key] = pd.eval(rule)
            ia_criteries.append(key)

    ia_criteries = set(ia_criteries)
    s_filter_result_sum = ia_df_filter_result[ia_criteries].sum(axis=1)

    # Полностью устраивающие варианты
    ia_full_match_df = ia_df[s_filter_result_sum == len(ia_criteries)]

    # остальные варианты в порядке убывания совпадающих элементов
    ia_other_df = ia_df.loc[
        s_filter_result_sum[s_filter_result_sum < len(ia_criteries)].sort_values(ascending=False).index]

    dict_df = ia_full_match_df.to_dict('index')

    return aiohttp.web.json_response(
        {'full_match': {rec_id: {str(col_id): dict_df[rec_id][col_id] for col_id in dict_df[rec_id]} for rec_id in
                        dict_df.keys()}},
        status=201)

    # return aiohttp.web.json_response(
    #     {'full_match' : ia_full_match_df.to_dict('index'),
    #      'other': ia_other_df.to_dict('index')},
    #     status=201)
