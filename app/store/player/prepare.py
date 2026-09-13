def prepare_player(player_data, team_slug):
    return {
        'nickname': player_data['nickname'],
        'fullname': player_data['fullname'],
        'team_slug': team_slug,
    }