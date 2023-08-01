from datetime import datetime

basic_templates = {
    '.gym_set': {
        'type': 'gym_set',
        'warmup': False,
        'weight': 0,
        'reps': 10,
    },
    '.gym_exc': {
        'type': 'gym_exc',
        'name': 'unk',
        'sets_num': 4,
        'sets': [
            '.gym_set',
            '.gym_rest',
            '.gym_set',
            '.gym_rest',
            '.gym_set',
            '.gym_rest',
            '.gym_set',
        ]
    },
    '.gym_rest': {
        'type': 'gym_rest',
        'time': '1m0s'
    },
    '.gym_workout': {
        'type': 'gym_workout',
        'date': datetime.today().date().strftime('%Y-%m-%d'),
        'program': [
            '.gym_exc', #1
            '.gym_rest',
            '.gym_exc', #2
            '.gym_rest',
            '.gym_exc', #3
            '.gym_rest',
            '.gym_exc', #4
            '.gym_rest',
            '.gym_exc', #5
            '.gym_rest',
            '.gym_exc', #6
            '.gym_rest',
            '.gym_exc', #7
            '.gym_rest',
            '.gym_exc', #8
            '.gym_rest',
        ]
    },
    '.running': {
        'type': 'running',
        'date': datetime.today().date().strftime('%Y-%m-%d'),
        'starting_time': '10h00m00s',
        'tempo': '6m0s',
        'avg_speed': '10.3kmh',
        'max_speed': '15.8kmh',
        'uphill': '317m',
        'downhill': '312m',
        'max_height': '616m',
        'lost_water': '700ml',
    }
}

'''
    '.gym_exc': {
        'name': 'unk',
        'sets_num': 4,
        'sets': [
            {
                'warmup': True,
                'weight': 0,
                'reps': 10,
            },
            {
                'warmup': False,
                'weight': 0,
                'reps': 10,
            },
            {
                'warmup': False,
                'weight': 0,
                'reps': 10,
            },
            {
                'warmup': False,
                'weight': 0,
                'reps': 10,
            },
        ]
    },
    '''