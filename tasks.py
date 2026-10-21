tasks = {
    'souls': {
        'name': 'Farm Souls',
        'steps': [
            {'action': 'find_click', 'target': 'souls_button', 'desc': 'Nhấn nút Souls'},
            {'action': 'find_click', 'target': 'start_button', 'desc': 'Nhấn nút Start'},
            {'action': 'wait', 'time': 2, 'desc': 'Chờ chút'},
            {'action': 'repeat', 'desc': 'Lặp lại'}
        ],
        'current_step': 0
    },
    'realm_raid': {
        'name': 'Realm Raid',
        'mode': 'dynamic',
        'steps': [
            {'action': 'find_click', 'target': 'realm_raid_button', 'desc': 'Nhấn nút Realm Raid', 'optional': True},
            {'action': 'find_click', 'target': 'refresh_button', 'desc': 'Làm mới danh sách kẻ địch', 'optional': True},
            {'action': 'find_click', 'target': 'enemy_button', 'desc': 'Chọn kẻ địch'},
            {'action': 'find_click', 'target': 'start_button', 'desc': 'Nhấn nút Start'},
            {'action': 'wait_for', 'target': 'battle_screen', 'desc': 'Chờ vào trận', 'timeout': 10},
            {'action': 'find_click', 'target': 'auto_button', 'desc': 'Bật chế độ tự động'},
            {'action': 'wait_for', 'target': 'victory_screen', 'desc': 'Chờ chiến thắng', 'timeout': 120},
            {'action': 'find_click', 'target': 'reward_screen', 'desc': 'Nhận thưởng'},
            {'action': 'find_click', 'target': 'exit_button', 'desc': 'Thoát màn hình kết thúc', 'optional': True},
            {'action': 'wait', 'time': 2, 'desc': 'Chờ chút'},
            {'action': 'repeat', 'desc': 'Lặp lại'}
        ],
        'current_step': 0
    }
}