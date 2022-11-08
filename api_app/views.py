from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartItemSerializer
from .models import CartItem
import psycopg2
import json


class CartItemViews(APIView):

    def get(self, request, id=None):
        if id:
            item = CartItem.objects.get(id=id)
            serializer = CartItemSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        
        serializer = CartItemSerializer(data=request.data)

        print(request.data)
            # Path: ki.py
        a = request.data
        # b = json.dumps(a)
        
        varient_type = ''
        varient_id = ''
        sku = ''
        varient_name = ''
        price_amount = ''
        cost_price_amount = ''
        quantity  = ''
        quantity_allocated = ''
        is_published = ''
        a = request.data

        for i in a:
            for j in i['variants']:
                varient_type = j['type']
                varient_id = j['id']
                sku = j['sku']
                varient_name = j['name']
                price_amount = j['price_amount']
                cost_price_amount = j['cost_price_amount']
                quantity = j['quantity']
                quantity_allocated = j['quantity_allocated']
                is_published = i['is_published']
                print(varient_type)
                print(varient_id)
                print(sku)
                print(varient_name)
                print(price_amount)
                print(cost_price_amount)
                print(quantity)
                print(quantity_allocated)
                print(is_published)
        
                conn = psycopg2.connect(
                    host="database-crm.cazl4vulkacd.ap-south-1.rds.amazonaws.com",
                    database="database_crm",
                    user="database_gg_crm",
                    password="Crmpostgres123"
                )
                # create a cursor
                cur = conn.cursor()
                # cur.execute("select * from inventory")
                # print(cur.fetchall())
                # insert_query = "insert into inventory (varient_type, varient_id, sku, varient_name, price_amount, cost_price_amount, quantity, quantity_allocated, is_published) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (varient_type, varient_id, sku, varient_name, price_amount, cost_price_amount, quantity, quantity_allocated, is_published)"
                cur.execute("INSERT INTO inventory (varient_type, varient_id, sku, varient_name, price_amount, cost_price_amount, quantity, quantity_allocated, is_published) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (varient_type, varient_id, sku, varient_name, price_amount, cost_price_amount, quantity, quantity_allocated, is_published))
                # cur.execute(insert_query)
                conn.commit()
                # cur.execute("select * from product")
                cur.execute("select * from inventory")
                print(cur.fetchall())
    
            
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "sucess", "data": "successfull inserted into db"}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = CartItem.objects.get(id=id)
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        item = get_object_or_404(CartItem, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
