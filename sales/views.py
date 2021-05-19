from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_custome_from_id,get_salesman_from_id, get_chart
# Create your views here.
def home_view(request):
    search_form= SalesSearchForm(request.POST or None)
    report_from = ReportForm()
    sales_df = None
    positions_df =None
    merge_df = None
    df  = None
    chart = None
    no_data=None
    if request.method == "POST":


        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_type= request.POST.get('results_by')

        sales_qs= Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if sales_qs.exists():
            qs_values=sales_qs.values()
            positions=[]
            for sale_item in sales_qs:
                for positions_item in sale_item.get_positions():
                    temp_data={
                        'id':positions_item.id,
                        'product':positions_item.product.name,
                        'price':positions_item.price,
                        'created':positions_item.created,
                        'sales_id':sale_item.id
                    }
                    positions.append(temp_data)
            
            sales_df = pd.DataFrame(qs_values)
            positions_df=pd.DataFrame(positions)
            sales_df['customer_id']=sales_df['customer_id'].apply(get_custome_from_id)
            sales_df['salesman_id']=sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'customer_id':'customer','salesman_id':'salesman','id':'sales_id'}, axis=1,inplace=True)

            merge_df = pd.merge(sales_df,positions_df,on='sales_id')
            df = merge_df.groupby('transaction_id', as_index=False)['price'].agg('sum')


            chart =get_chart(chart_type, sales_df, result_type)

            sales_df=sales_df.to_html()
            positions_df = positions_df.to_html()
            merge_df=merge_df.to_html()
            df = df.to_html()
        else:
            no_data="NO data avilabel in this range"
            
            
       
        
      


    context = {
        'search_form': search_form,
        'sales_df':sales_df,
        'positions_df':positions_df,
        'merge_df':merge_df,
        'df':df,
        'chart':chart,
        'report_form':report_from,
        'no_data':no_data
        }

    return render(request,'sales/home.html', context)


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'