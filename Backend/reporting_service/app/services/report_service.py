from datetime import datetime
from ..repositories import report_repository as repo


def generate_visitor_report(start_date: datetime, end_date: datetime):
    data = repo.get_visitor_stats(start_date, end_date)
    summary = {
        'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'total_visitors': data['total_visitors'],
        'most_active_unit': data['top_units'][0] if data['top_units'] else None
    }
    return {
        'report_type': 'visitors',
        'title': f'Visitor Report - {summary["period"]}',
        'generated_at': datetime.now(),
        'data': data,
        'summary': summary
    }


def generate_maintenance_report(start_date: datetime, end_date: datetime):
    data = repo.get_maintenance_stats(start_date, end_date)
    summary = {
        'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'total_orders': data['total_orders'],
        'completion_rate': (data['status_breakdown'].get('completed', 0) / data['total_orders'] * 100) if data['total_orders'] > 0 else 0
    }
    return {
        'report_type': 'maintenance',
        'title': f'Maintenance Report - {summary["period"]}',
        'generated_at': datetime.now(),
        'data': data,
        'summary': summary
    }


def generate_reservation_report(start_date: datetime, end_date: datetime):
    data = repo.get_reservation_stats(start_date, end_date)
    summary = {
        'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'total_reservations': data['total_reservations'],
        'most_popular_area': max(data['area_breakdown'].items(), key=lambda x: x[1])[0] if data['area_breakdown'] else None
    }
    return {
        'report_type': 'reservations',
        'title': f'Reservation Report - {summary["period"]}',
        'generated_at': datetime.now(),
        'data': data,
        'summary': summary
    }


def generate_financial_report(start_date: datetime, end_date: datetime):
    data = repo.get_financial_stats(start_date, end_date)
    summary = {
        'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'total_revenue': data['total_revenue'],
        'net_profit': data['net_profit']
    }
    return {
        'report_type': 'financial',
        'title': f'Financial Report - {summary["period"]}',
        'generated_at': datetime.now(),
        'data': data,
        'summary': summary
    }


def generate_report(report_type: str, start_date: datetime, end_date: datetime):
    if report_type == 'visitors':
        return generate_visitor_report(start_date, end_date)
    elif report_type == 'maintenance':
        return generate_maintenance_report(start_date, end_date)
    elif report_type == 'reservations':
        return generate_reservation_report(start_date, end_date)
    elif report_type == 'financial':
        return generate_financial_report(start_date, end_date)
    else:
        raise ValueError(f"Unknown report type: {report_type}")

