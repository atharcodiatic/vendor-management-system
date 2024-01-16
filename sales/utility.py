def calc_fulfilment_rate(fulfillment_rate , completed_po , vendor_total_po):
    fulfillment_rate = 0.0
    try:
        fulfillment_rate = completed_po.count() / vendor_total_po.count()
    except ZeroDivisionError:
        fulfillment_rate = 0.0
    return fulfillment_rate

def calc_on_time_delivery(on_time_delivery_rate, vendor_total_po):
    try:
        on_time_delivery_rate = vendor_total_po.filter(delivered_ontime=True).count()/completed_po.count()
    except ZeroDivisionError:
        on_time_delivery_rate = 0.0
    return on_time_delivery_rate