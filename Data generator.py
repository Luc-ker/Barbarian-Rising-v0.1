lv = 1

hp = int(input("Input HP: "))
atk = int(input("Input atk: "))
defe = int(input("Input def: "))
spd = int(input("Input spd: "))
abil_lv = int(input("Input abil_lv: "))

for i in range(100):
    print(f"{lv},{hp},{atk},{defe},{spd},{abil_lv}")
    lv += 1
    hp += 1
    atk += 1
    defe += 1
    if lv % 5 == 0:
        spd += 1
        abil_lv += 1
