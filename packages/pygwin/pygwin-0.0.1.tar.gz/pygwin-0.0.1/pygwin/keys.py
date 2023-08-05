#!/usr/bin/env python3

'''@TODO@'''


class Keys:
    '''@TODO@'''

    ACT_ACTIVATE_FOCUS = 'activate'
    ACT_CLOSE_WINDOW = 'close-window'
    ACT_MOVE_FOCUS_FORWARD = 'move-focus-forward'
    ACT_MOVE_FOCUS_BACKWARD = 'move-focus-backward'
    ACT_USER_DEFINED = 'user-defined'

    __MAP = dict()

    @classmethod
    def bind(cls, key, action, pressed=None, fun=None):
        '''@TODO@'''
        if pressed is None:
            pressed = tuple()
        else:
            pressed = tuple(sorted(pressed))
        if action is None:
            if key in Keys.__MAP:
                if pressed in Keys.__MAP[key]:
                    del Keys.__MAP[key][pressed]
                if Keys.__MAP[key] == 0:
                    del Keys.__MAP[key]
        else:
            if key not in Keys.__MAP:
                Keys.__MAP[key] = dict()
            Keys.__MAP[key][pressed] = action, fun

    @classmethod
    def action(cls, key, pressed):
        '''@TODO@'''
        acts = Keys.__MAP.get(key)
        if acts is not None:
            for keys in acts:
                if all(pressed[key] for key in keys):
                    ok = True
                    for i, p in enumerate(pressed):
                        if p and i != key and i not in keys:
                            ok = False
                    if ok:
                        return acts[keys]
        return None
