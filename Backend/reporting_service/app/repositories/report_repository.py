from typing import List, Tuple, Dict, Any
from datetime import datetime
from ..core.db import get_conn


def get_visitor_stats(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    
    # Total visitors
    cur.execute('''SELECT COUNT(*) FROM visitors 
                   WHERE visit_date BETWEEN %s AND %s''', (start_date, end_date))
    total_visitors = cur.fetchone()[0]
    
    # Visitors by status
    cur.execute('''SELECT status, COUNT(*) FROM visitors 
                   WHERE visit_date BETWEEN %s AND %s 
                   GROUP BY status''', (start_date, end_date))
    status_counts = dict(cur.fetchall())
    
    # Visitors by unit
    cur.execute('''SELECT u.block, u.number, COUNT(v.id) as visitor_count
                   FROM visitors v
                   JOIN units u ON v.unit_id = u.id
                   WHERE v.visit_date BETWEEN %s AND %s
                   GROUP BY u.block, u.number
                   ORDER BY visitor_count DESC''', (start_date, end_date))
    unit_stats = [{'block': r[0], 'number': r[1], 'count': r[2]} for r in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return {
        'total_visitors': total_visitors,
        'status_breakdown': status_counts,
        'top_units': unit_stats[:10]
    }


def get_maintenance_stats(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    
    # Total maintenance orders
    cur.execute('''SELECT COUNT(*) FROM maintenance_orders 
                   WHERE created_at BETWEEN %s AND %s''', (start_date, end_date))
    total_orders = cur.fetchone()[0]
    
    # Orders by status
    cur.execute('''SELECT status, COUNT(*) FROM maintenance_orders 
                   WHERE created_at BETWEEN %s AND %s 
                   GROUP BY status''', (start_date, end_date))
    status_counts = dict(cur.fetchall())
    
    # Orders by category
    cur.execute('''SELECT category, COUNT(*) FROM maintenance_orders 
                   WHERE created_at BETWEEN %s AND %s 
                   GROUP BY category''', (start_date, end_date))
    category_counts = dict(cur.fetchall())
    
    # Orders by priority
    cur.execute('''SELECT priority, COUNT(*) FROM maintenance_orders 
                   WHERE created_at BETWEEN %s AND %s 
                   GROUP BY priority''', (start_date, end_date))
    priority_counts = dict(cur.fetchall())
    
    cur.close()
    conn.close()
    
    return {
        'total_orders': total_orders,
        'status_breakdown': status_counts,
        'category_breakdown': category_counts,
        'priority_breakdown': priority_counts
    }


def get_reservation_stats(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    
    # Total reservations
    cur.execute('''SELECT COUNT(*) FROM reservations 
                   WHERE start_time BETWEEN %s AND %s''', (start_date, end_date))
    total_reservations = cur.fetchone()[0]
    
    # Reservations by status
    cur.execute('''SELECT status, COUNT(*) FROM reservations 
                   WHERE start_time BETWEEN %s AND %s 
                   GROUP BY status''', (start_date, end_date))
    status_counts = dict(cur.fetchall())
    
    # Reservations by area
    cur.execute('''SELECT area, COUNT(*) FROM reservations 
                   WHERE start_time BETWEEN %s AND %s 
                   GROUP BY area''', (start_date, end_date))
    area_counts = dict(cur.fetchall())
    
    cur.close()
    conn.close()
    
    return {
        'total_reservations': total_reservations,
        'status_breakdown': status_counts,
        'area_breakdown': area_counts
    }


def get_financial_stats(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    # Placeholder for financial data - would need financial tables
    return {
        'total_revenue': 0,
        'maintenance_costs': 0,
        'utilities': 0,
        'net_profit': 0
    }

