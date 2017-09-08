from django.template import loader
from django.http import HttpResponse

import requests


def landing_page_controller(request, **kwargs):
    split_path = request.get_full_path().split('?')[0].split('/')

    path = '-'.join(filter(lambda e: e != '', split_path))

    template = loader.get_template(f"home/{path}.html")

    return HttpResponse(template.render(context=None, request=request))


def assessment_controller(request, **kwargs):
    params = request.POST

    answers = filter(lambda p: p[:2] == "Q_", params)

    prms = {}

    for a in answers:
        if len(a.split("_")) == 3:
            prms[a.split("_")[2]] = params.get(a)
        else:
            prms[params.get(a)] = ""

    if not (params.get("member_id") and params.get("traversal_id")):
        r = requests.get('http://apps.expert-24.com/WebBuilder/TraversalService/Member?callback=raw')

        response = r.json()
        member_id = response["Table"][0]["MemberID"]
        traversal_id = response["Table"][0]["TraversalID"]
    else:
        member_id = params.get("member_id")
        traversal_id = params.get("traversal_id")

    algo_id = 4648
    node_id = 0

    if params.get("node_id"):
        node_id = params.get("node_id")

    if params.get("algo_id"):
        algo_id = params.get("algo_id")

    if params.get("previous"):
        direction = params.get("previous")
    elif params.get("q_info"):
        direction = "Rerender"
        node_type_id = 32
        asset_id = params.get("q_info")
    elif params.get("a_info"):
        direction = "Rerender"
        node_type_id = 64
        asset_id = params.get("a_info")
    elif params.get("return_summary"):
        direction = params.get("return_summary")
    else:
        direction = "Next"

    url = f"http://apps.expert-24.com/WebBuilder/TraversalService/{direction}/{traversal_id}/{member_id}/{algo_id}/{node_id}?callback=raw"

    for p in prms:
        url += f"&{p}={prms[p]}"

    r2 = requests.get(url)

    template = loader.get_template(f"home/server-assessment.html")

    context = r2.json()

    context["member_id"] = member_id
    context["traversal_id"] = traversal_id

    if params.get("q_info") or params.get("a_info"):
        context["info"] = requests.get(f"http://apps.expert-24.com/WebBuilder/TraversalService/Info/{traversal_id}/{member_id}?callback=raw&@NodeTypeID={node_type_id}&@AssetID={asset_id}").json()

    return HttpResponse(template.render(context=context, request=request))


def assessment_summary_controller(request, **kwargs):
    template = loader.get_template(f"home/assessment-summary.html")

    traversal_id = request.POST.get("traversal_id")
    member_id = request.POST.get("member_id")

    context = requests.get(f"http://apps.expert-24.com/WebBuilder/TraversalService/Summary/{traversal_id}/{member_id}?callback=raw").json()

    context["member_id"] = member_id
    context["traversal_id"] = traversal_id
    context["node_id"] = request.POST.get("node_id")
    context["algo_id"] = request.POST.get("algo_id")

    return HttpResponse(template.render(context=context, request=request))
