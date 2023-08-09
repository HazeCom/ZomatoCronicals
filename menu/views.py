from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

menu_data = {
    1: {'id': 1, 'name': 'Pizza', 'price': 10.99, 'availability': True},
    2: {'id': 2, 'name': 'Burger', 'price': 5.99, 'availability': True},
    3: {'id': 3, 'name': 'Pasta', 'price': 7.99, 'availability': False},
}

orders = {}
order_counter = 1


def load_data():
    global menu_data, orders, order_counter
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            menu_data = data.get('menu', {})
            orders = data.get('orders', {})
            order_counter = max(orders.keys(), default=0) + "1"
    except FileNotFoundError:
        pass


load_data()


def display_menu(request):
    return JsonResponse(menu_data, safe=False)


@csrf_exempt
def add_dish(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dish_id = int(data.get('dish_id'))
        print(dish_id)
        if dish_id not in menu_data:
            return JsonResponse({'error': 'Dish not found'}, status=404)
        orders[dish_id] = orders.get(dish_id, 0) + 1
        return JsonResponse({'message': 'Dish added to order'})


@csrf_exempt
def update_availability(request, dish_id):
    if dish_id in menu_data:
        data = json.loads(request.body)
        availability = data.get('availability')
        menu_data[dish_id]['availability'] = availability == 'true'
        return JsonResponse({'message': 'Availability updated'})
    else:
        return JsonResponse({'error': 'Dish not found'}, status=404)


@csrf_exempt
def take_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_name = data.get('customer_name')
        order_items = data.get('order_items')
        print(data)

        # Check dish availability before processing the order
        unavailable_items = [item for item in order_items if not menu_data.get(int(item))['availability']]
        if unavailable_items:
            return JsonResponse({'error': f'Dishes not available: {", ".join(unavailable_items)}'}, status=400)

        global order_counter
        order_id = order_counter
        order_counter += 1
        total_price = sum([menu_data[int(item)]['price'] for item in order_items])
        orders[order_id] = {
            'customer_name': customer_name,
            'order_items': order_items,
            'status': 'received',
            'total_price': total_price,
        }
        return JsonResponse({'message': 'Order taken', 'order_id': order_id, 'total_price': total_price})


@csrf_exempt
def update_order_status(request, order_id):
    if order_id in orders:
        data = json.loads(request.body)
        status = data.get('status')
        orders[order_id]['status'] = status
        return JsonResponse({'message': 'Order status updated'})
    else:
        return JsonResponse({'error': 'Order not found'}, status=404)


def review_orders(request):
    return JsonResponse({'orders': orders})


@csrf_exempt
def end_operations(request):
    save_data()
    orders.clear()
    return JsonResponse({'message': 'Operations ended'})


@csrf_exempt
def filter_orders_by_status(request, status):
    filtered_orders = {order_id: order for order_id, order in orders.items() if order['status'] == status}
    return JsonResponse({'filtered_orders': filtered_orders})


def save_data():
    with open('data.json', 'w') as f:
        json.dump({'menu': menu_data, 'orders': orders}, f)
