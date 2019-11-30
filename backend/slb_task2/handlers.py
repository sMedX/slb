import aiohttp.web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import logging
import pandas as pd

log = logging.getLogger(__name__)


async def get_attributes_handler(request: Request) -> Response:
    log.debug('Start get_attributes_handler')
    attributes = request.app['config']['attributes']
    return aiohttp.web.json_response(attributes, status=200)


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

    user_ia = await request.json()

    if len(user_ia) == 0:
        message = 'No attributes set'
        log.error("Error during filtering packers: %s", message)
        return aiohttp.web.json_response({'message': message}, status=400)

    ia_df = request.app['data']['ia_df']
    attributes = request.app['config']['attributes']

    ia_df_filter_result = pd.DataFrame().reindex_like(ia_df)
    ia_criteries = []

    for user_attr_value in user_ia:
        if user_attr_value[0] in attributes and user_attr_value[1] in attributes[user_attr_value[0]]:
            rule = attributes[user_attr_value[0]][user_attr_value[1]]['rule']
            x = user_attr_value[2]
            ia_df_filter_result[(user_attr_value[0], user_attr_value[1])] = pd.eval(rule)
            ia_criteries.append((user_attr_value[0], user_attr_value[1]))

    ia_criteries = set(ia_criteries)
    s_filter_result_sum = ia_df_filter_result[ia_criteries].sum(axis=1)

    # Полностью устраивающие варианты
    ia_full_match_df = ia_df[s_filter_result_sum == len(ia_criteries)]

    # остальные варианты в порядке убывания совпадающих элементов
    ia_other_matсh_df = ia_df.loc[
        s_filter_result_sum[s_filter_result_sum < len(ia_criteries)].sort_values(ascending=False).index]

    ia_other_matсh_flag_df = ia_df_filter_result[ia_criteries].loc[
        s_filter_result_sum[s_filter_result_sum < len(ia_criteries)].sort_values(ascending=False).index]

    full_match_df = ia_full_match_df.to_dict('index')
    other_match_df = ia_other_matсh_df.to_dict('index')
    other_match_flag_df = ia_other_matсh_flag_df.to_dict('index')

    return aiohttp.web.json_response(
        {'full_match': {rec_id: {str(list(col_id)): full_match_df[rec_id][col_id]
                                 for col_id
                                 in full_match_df[rec_id]}
                        for rec_id in full_match_df.keys()},
         'other_match': {rec_id: {str(col_id): other_match_df[rec_id][col_id]
                                  for col_id
                                  in other_match_df[rec_id]}
                         for rec_id in other_match_df.keys()},
         'other_match_flag': {rec_id: {str(col_id): other_match_flag_df[rec_id][col_id]
                                       for col_id
                                       in other_match_flag_df[rec_id]}
                              for rec_id in other_match_flag_df.keys()}
         },
        dumps=request.app['dumps'],
        status=201)
