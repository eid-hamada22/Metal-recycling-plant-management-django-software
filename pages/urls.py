from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('money_box', views.money_box, name="money_box"),
    path('money_box_print', views.money_box_print, name="money_box_print"),

    path('iron_purchases', views.iron_purchases, name="iron_purchases"),
    path('iron_purchases/<int:id>', views.iron_purchases_child, name="iron_purchases"),
    path('iron_purchases/print', views.iron_purchases_print, name="iron_purchases_print"),


    path('iron_sales', views.iron_sales, name="iron_sales"),
    path('iron_sales/<int:id>', views.iron_sales_child, name="iron_sales"),

    path('income', views.income, name="income"),
    path('income/print', views.income_print, name="income_print"),


    path('expenses', views.expenses, name="expenses"),
    path('expenses/print_iron', views.expenses_print, name="expenses_print"),
    path('expenses/print_noiron', views.expenses_print_noiron, name="expenses_print_noiron"),

    path('pistons', views.pistons, name="pistons"),
    path('pistons_print', views.pistons_print, name="pistons_print"),

    path('weight_gain', views.weight_gain, name="weight_gain"),
    # path('weight_gain/<int:id>', views.weight_gain_child, name="weight_gain"),

    path('export', views.export, name="export"),

    path('fuel_box', views.fuel_box, name="fuel_box"),
    path('fuel_box_print', views.fuel_box_print, name="fuel_box_print"),

    path('fuel', views.fuel, name="fuel"),
    path('fuel_incom', views.fuel_incom, name="fuel_incom"),

    path('accounts', views.accounts, name="accounts"),
    path('accounts/<int:id>', views.accounts_child, name="accounts"),

    path('week_sum', views.week_sum, name="week_sum"),
    path('week_pyn', views.week_pyn, name="week_pyn"),
    # path('sum', views.sum, name="sum"),

]
