
def parse_slice(selector):
    l = selector.split(':')

    def f(x):
        return None if x == '' else int(x)
    return slice(f(l[0]), f(l[1]))


indice = [(slice(0, 20, None), slice(20, 36, None)),
          (slice(36, 56, None), slice(56, 72, None)),
          (slice(72, 92, None), slice(92, 108, None)),
          (slice(108, 128, None), slice(128, 144, None)),
          (slice(144, 164, None), slice(164, 180, None))]
