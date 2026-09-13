def prepare_team(team_info):
    return {
        'name': team_info['title'],
        'link': team_info['link'],
        'slug': team_info['slug'],
    }