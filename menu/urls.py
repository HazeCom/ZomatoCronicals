from django.urls import path
from . import views

urlpatterns = {
    # ... (existing URLs)
    path('add_dish/', views.add_dish, name='add_dish'),
    path('update_availability/<int:dish_id>/', views.update_availability, name='update_availability'),
    path('take_order/', views.take_order, name='take_order'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('review_orders/', views.review_orders, name='review_orders'),
    path('end_operations/', views.end_operations, name='end_operations'),
    path('filter_orders_by_status/<str:status>/', views.filter_orders_by_status, name='filter_orders_by_status'),
    path('menu/', views.display_menu, name='my_menu'),
}
