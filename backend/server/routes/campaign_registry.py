from server import app,auth,sql_db
from flask import request
from flask_cors import cross_origin
import datetime
import traceback

from server.models.models import SDataCampaign
from sqlalchemy_paginator import Paginator
from pyjackson import deserialize, serialize

from .response import Response

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