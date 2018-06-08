from aiohttp import web
from data_gathering import WebAPIExportManager
routes = web.RouteTableDef()

@routes.get('/get_acc/{account}')
async def get_acc_imported(request):
    account = request.match_info.get('account')
    web_api = WebAPIExportManager()
    web_api.get_account(account)
    return web.Response(text='Account received')

app = web.Application()
app.add_routes(routes)
web.run_app(app)


#import requests
#requests.get('http://127.0.0.1:8080/get_acc/avon_ua')
