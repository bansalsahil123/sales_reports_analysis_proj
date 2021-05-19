import uuid,base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_salesman_from_id(val):
    salesman=Profile.objects.get(pk=val)
    return salesman.user.username

def get_custome_from_id(val):
    customer=Customer.objects.get(pk=val)
    return customer

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    imgae_png=buffer.getvalue()
    graph=base64.b64encode(imgae_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_key(res_type):
    if res_type == "#1":
        return "transaction_id"
    else:
        return "created"


def get_chart(chart_type,data,result_by,**kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    key=get_key(result_by)
    data=data.groupby(key,as_index=False)['total_price'].agg('sum')
    if chart_type == "#1":
        print("Bar chart")
        sns.barplot(x=key, y='total_price',data=data)
    elif chart_type == "#2":
        print("pie chart")
        labels=data[key].values
        plt.pie(x='total_price',data=data,labels=labels)
    elif chart_type == "#3":
        print("Line chart")
        plt.plot(data[key],data['total_price'],color='green', marker='o')
    else:
         print('ups... failed to identify the chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart
