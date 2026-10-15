"""Эталонный симулятор учебного процессора (главы 4–5).

Исходник хранится строкой: его вставляют в скрытые драйверы задач, чтобы
проверять программы учеников на «настоящем» процессоре внутри песочницы.
"""

TOY_SIM = '''
def toy_run(program, regs=None, memory=None, limit=100000):
    r = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
    if regs:
        r.update(regs)
    mem = list(memory) if memory is not None else [0] * 256
    z = n = c = 0
    pc = steps = 0
    while True:
        if steps >= limit:
            raise RuntimeError("слишком много шагов")
        op, *a = program[pc]
        pc += 1
        steps += 1
        if op == "HLT":
            break
        if op == "LDI":
            r[a[0]] = a[1] & 255
        elif op == "MOV":
            r[a[0]] = r[a[1]]
        elif op in ("ADD", "SUB", "CMP", "AND", "OR", "XOR"):
            x, y = r[a[0]], r[a[1]]
            if op == "ADD":
                raw = x + y
                c = raw >> 8 & 1
            elif op in ("SUB", "CMP"):
                raw = x - y
                c = int(x < y)
            else:
                raw = x & y if op == "AND" else x | y if op == "OR" else x ^ y
                c = 0
            res = raw & 255
            z, n = int(res == 0), res >> 7
            if op != "CMP":
                r[a[0]] = res
        elif op in ("SHL", "SHR"):
            x = r[a[0]]
            if op == "SHL":
                c, res = x >> 7, (x << 1) & 255
            else:
                c, res = x & 1, x >> 1
            z, n = int(res == 0), res >> 7
            r[a[0]] = res
        elif op == "LD":
            r[a[0]] = mem[a[1]]
        elif op == "ST":
            mem[a[1]] = r[a[0]]
        elif op == "JMP":
            pc = a[0]
        elif op == "JZ":
            if z:
                pc = a[0]
        elif op == "JNZ":
            if not z:
                pc = a[0]
        elif op == "JC":
            if c:
                pc = a[0]
        elif op == "JN":
            if n:
                pc = a[0]
        else:
            raise ValueError("неизвестная команда " + op)
    return r, mem, steps
'''
