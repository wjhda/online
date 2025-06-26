1. GET 请求 获取产品信息

   ```
   url = 'http://127.0.0.1:9000/api/product/product-info/'
   参数：
   product_name
   请求示例：
   http://127.0.0.1:9000/api/product/product-info/?product_name=iphone
   响应示例：
   {
   	"code": 200,
   	"msg": "OK",
   	"data": [
   		{
   			"id": 1,
   			"create_at": "2025-06-25T16:00:54",
   			"update_at": "2025-06-25T16:17:38.395184",
   			"name": "iphone 15",
   			"description": "手机",
   			"price": "1000.00",
   			"stock": 90
   		}
   	]
   }
   ```

   2. POST 请求 批量处理订单信息

      ```
      url = http://127.0.0.1:9000/api/order/order-info/
      参数
      {
      	"order_items": [
      		{
      			"product_id": 1,
      			"quantity": 10
      		},
      	]
      }
      请求示例：http://127.0.0.1:9000/api/order/order-info/
      {
          "order_items": [
              {
                  "product_id": 1,
                  "quantity": 100000
              },
              {
                  "product_id": 2,
                  "quantity": 10000000
              }
          ]
      }
      响应示例：
      {
      	"code": 400,
      	"msg": "Bad Request",
      	"data": {
      		"error": "[ErrorDetail(string='库存不足', code='invalid')]"
      	}
      }
      请求示例：http://127.0.0.1:9000/api/order/order-info/
      {
          "order_items": [
              {
                  "product_id": 1,
                  "quantity": 1
              },
              {
                  "product_id": 2,
                  "quantity": 10
              }
          ]
      }
      相应示例：
      {
      	"code": 201,
      	"msg": "Created",
      	"data": {
      		"order_number": "20250625163952"
      	}
      }
      ```

      