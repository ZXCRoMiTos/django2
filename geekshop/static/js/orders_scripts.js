"use strict";


let totalForms, orderTotalQuantity, orderTotalCost, orderItemNum, deltaQuantity, orderItemQuantity, orderItemPrice;
let deltaCost;
let quantityArr = [];
let priceArr = [];
let $orderTotalQuantityDOM, $orderTotalCost, $orderForm;


function deleteOrderItem(row) {
   let target_name= row[0].querySelector('input[type="number"]').name;
   orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-qty', ''));
   delta_quantity = -quantity_arr[orderitem_num];
   orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
}




function renderSummary(orderTotalQuantity, orderTotalCost) {
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $orderTotalCost.html(Number(orderTotalCost.toFixed(2)).toString().replace('.', ','));
}


function orderSummaryUpdate(orderItemPrice, deltaQuantity) {
    orderTotalQuantity += deltaQuantity;
    deltaCost = orderItemPrice * deltaQuantity;
    orderTotalCost += deltaCost;
    renderSummary(orderTotalQuantity, orderTotalCost);
}


function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
        let quantity = parseInt($('input[name="orderitems-' + i + '-qty"]').val());
        let price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = quantity;
        priceArr[i] = (price) ? price : 0;
    }
}


function updateTotalQuantity() {
    orderTotalQuantity = 0;
    orderTotalCost = 0;
    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    renderSummary(orderTotalQuantity, orderTotalCost);
}


window.onload = function () {

    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val())

    $orderTotalQuantityDOM = $('.order_total_quantity');
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text()) || 0;

    $orderTotalCost = $('.order_total_cost');
    orderTotalCost = parseFloat($orderTotalCost.text().replace(',', '.')) || 0;

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm = $('.order_form');
    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderItemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-qty', ''));
        console.log('test', orderItemNum);
        if (priceArr[orderItemNum]) {
            orderItemQuantity = parseInt(event.target.value);
            deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
            quantityArr[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
        }
    });

    $('.formset_row').formset({
       addText: 'добавить продукт',
       deleteText: 'удалить',
       prefix: 'orderitems',
       removed: deleteOrderItem
    });
}
