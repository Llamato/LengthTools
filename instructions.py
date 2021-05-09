class Instructions:
    inp = 9
    add = 10
    sub = 11
    dup = 12
    cond = 13
    gotou = 14
    outn = 15
    outa = 16
    rol = 17
    swap = 18
    mul = 20
    div = 21
    pop = 23
    gotos = 24
    push = 25
    ror = 27
    Opcodes = {
        "inp": inp,
        "add": add,
        "sub": sub,
        "dup": dup,
        "cond": cond,
        "gotou": gotou,
        "outn": outn,
        "outa": outa,
        "rol": rol,
        "swap": swap,
        "mul": mul,
        "div": div,
        "pop": pop,
        "gotos": gotos,
        "push": push,
        "ror": ror,
    }

    Mnemonics = {
        inp: "inp",
        add: "add",
        sub: "sub",
        dup: "dup",
        cond: "cond",
        gotou: "gotou",
        outn: "outn",
        outa: "outa",
        rol: "rol",
        swap: "swap",
        mul: "mul",
        div: "div",
        pop: "pop",
        gotos: "gotos",
        push: "push",
        ror: "ror"
    }
