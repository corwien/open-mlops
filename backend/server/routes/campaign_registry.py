from .. import app,auth,sql_db
from flask import request
from flask_cors import cross_origin
import datetime
import traceback

from ..models.models import (SDataCampaign,
                                  SAbExpCase,
                                  SAbExpOps)
from sqlalchemy_paginator import Paginator
from pyjackson import deserialize, serialize

from .response import Response
from structlog import get_logger

logger = get_logger(__name__)

rsp = Response()


@app.route('/api/campaigns',methods=['GET'])  
@cross_origin()
@auth.login_required
def registered_campaigns():
    page_size = 10
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    user_name = request.args.get('user_key','')

    with sql_db._session() as s:          
        q = s.query(SDataCampaign)
        if name:
            q=q.filter(SDataCampaign.name.like('%{}%'.format(name)))
        paginator = Paginator(q, page_size)
        _page = paginator.page(page)
        total_pages = _page.paginator.total_pages
        data = [serialize(o.to_obj()) for o in _page.object_list]
   
    result = {"data":data,
            "page": page,
            "total": total_pages}
    return rsp.success(result)

@app.route('/api/campaigns/add_campaign',methods=['POST'])  
@cross_origin()
@auth.login_required
def add_campaign():
    try:
        campaign_name = request.get_json()['name']
        description = request.get_json()['description']
        campaign_type = request.get_json()['type']
        user_name = request.get_json()['user']
        
        obj = SDataCampaign(name=str(campaign_name),
                            description = description,
                            data_campaign_type = campaign_type,
                            author= user_name,
                            campaign_status = 0,
                            online_date= datetime.datetime.utcnow(),
                            expire_date= datetime.datetime.utcnow(),
                            creation_date= datetime.datetime.utcnow())
        sql_db._create_object(obj)
        

        return rsp.success('campaign added success!')
    except:
        exc_traceback = str(traceback.format_exc())
        return rsp.failed(exc_traceback)
    
@app.route('/api/campaigns/abexps',methods=['GET'])  
@cross_origin()
@auth.login_required
def registered_abexps():
    page_size = 10
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    user_name = request.args.get('user_key','')
    campaign_id = request.args.get('campaign_id',1)
    _data = []
    with sql_db._session() as s:          
        q = s.query(SAbExpCase)
        q=q.filter(SAbExpCase.data_campaign_id==campaign_id)
        if name:
            q=q.filter(SAbExpCase.name.like('%{}%'.format(name)))
        paginator = Paginator(q, page_size)
        _page = paginator.page(page)
        total_pages = _page.paginator.total_pages
        data = [serialize(o.to_obj()) for o in _page.object_list]
        for abgroup in data:
            ops = sql_db._get_objects(SAbExpOps,SAbExpOps.ab_id==abgroup["id"])
            abgroup["abalt_cnt"] = len(ops)
            _data.append(abgroup)
   
    result = {"data":_data,
            "page": page,
            "total": total_pages}
    return rsp.success(result)

@app.route('/api/campaigns/get_campaign_metadata',methods=['GET'])  
@cross_origin()
@auth.login_required
def get_campaign_metadata():
    try:
        campaign_id = request.args.get('campaign_id', '')
        
        data = sql_db._get_objects(SDataCampaign,SDataCampaign.id==campaign_id)
        data2 = sql_db._get_objects(SAbExpCase,SAbExpCase.data_campaign_id==campaign_id)
        
        meta_campaign = {}
        meta_campaign["campaign"] = [serialize(o) for o in data][0]
        meta_campaign["strategy_cnt"] = len(data2)
        results = {"data": meta_campaign}
        return rsp.success(results)
    except:
        exc_traceback = str(traceback.format_exc())
        # print(exc_traceback,"exc_traceback")
        return rsp.failed(exc_traceback)

@app.route('/api/campaigns/add_ab_exp',methods=['POST'])  
@cross_origin()
@auth.login_required
def add_ab_exp():
    try:
        ab_name = request.get_json()['name']
        campaign_id = request.get_json()['campaign_id']
        description = request.get_json()['description']
        user_name = request.get_json()['user_key']
        logger.debug('Getting %ss', ab_name=ab_name)
        obj = SAbExpCase(name=str(ab_name),
                         description = description,
                         data_campaign_id = campaign_id,
                         user_id= 1,
                         app_type = '基于数据策略',
                         creation_date= datetime.datetime.utcnow())
        sql_db._create_object(obj)
        return rsp.success('abexp added success!')
    except:
        exc_traceback = str(traceback.format_exc())
        return rsp.failed(exc_traceback)