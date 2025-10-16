# Sistema de Permissões do Sistema de Condomínios

# Permissões por Role
ROLE_PERMISSIONS = {
    'admin': [
        'all'  # Admin tem acesso total
    ],
    'sindico': [
        'view_users',
        'create_users',
        'edit_users',
        'view_units',
        'create_units',
        'edit_units',
        'view_reservations',
        'create_reservations',
        'edit_reservations',
        'cancel_reservations',
        'view_visitors',
        'create_visitors',
        'edit_visitors',
        'view_maintenance',
        'create_maintenance',
        'edit_maintenance',
        'assign_maintenance',
        'complete_maintenance',
        'view_reports',
        'generate_reports',
        'export_data'
    ],
    'morador': [
        'view_own_profile',
        'edit_own_profile',
        'view_own_units',
        'view_reservations',
        'create_reservations',
        'cancel_own_reservations',
        'view_own_visitors',
        'create_visitors',
        'view_own_maintenance',
        'create_maintenance'
    ]
}

# Permissões específicas por módulo
MODULE_PERMISSIONS = {
    'users': [
        'view_users',
        'create_users',
        'edit_users',
        'delete_users',
        'view_own_profile',
        'edit_own_profile'
    ],
    'units': [
        'view_units',
        'create_units',
        'edit_units',
        'delete_units',
        'view_own_units'
    ],
    'reservations': [
        'view_reservations',
        'create_reservations',
        'edit_reservations',
        'cancel_reservations',
        'cancel_own_reservations'
    ],
    'visitors': [
        'view_visitors',
        'create_visitors',
        'edit_visitors',
        'delete_visitors',
        'view_own_visitors',
        'check_in_visitors',
        'check_out_visitors'
    ],
    'maintenance': [
        'view_maintenance',
        'create_maintenance',
        'edit_maintenance',
        'delete_maintenance',
        'assign_maintenance',
        'complete_maintenance',
        'view_own_maintenance'
    ],
    'reports': [
        'view_reports',
        'generate_reports',
        'export_data'
    ]
}

def get_permissions_for_role(role: str) -> list:
    """Retorna as permissões para um role específico"""
    return ROLE_PERMISSIONS.get(role, [])

def has_permission(user_permissions: list, required_permission: str) -> bool:
    """Verifica se o usuário tem uma permissão específica"""
    return 'all' in user_permissions or required_permission in user_permissions

def get_module_permissions(module: str) -> list:
    """Retorna as permissões para um módulo específico"""
    return MODULE_PERMISSIONS.get(module, [])
