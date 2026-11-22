import random
N=random.randint(5,15)
print(f"Лабиринт {N}x{N}")
room_types=["empty", "chest","monster","trap"]
weights=[50,15,15,10]
#генерация карты
maze=[
    [random.choices(room_types, weights=weights)[0]
     for _ in range(N)]
    for _ in range(N)
]
#выход и ключ
maze[0][0]="empty"
position=[(r,c) for r in range(N) for c in range(N) if (r,c)!=(0,0)]
key_pos, exite_pos=random.sample(position,2)
maze[key_pos[0]][key_pos[1]]="key"
maze[exite_pos[0]][exite_pos[1]]="exit"

#for row in maze:
 #   print(row)

#игрок
player={
    "row": 0,
    "col": 0,
    "prev_row": 0,
    "prev_col": 0,
    "hp": 5,
    "inventary": [],
    "has_key": False,
}
#предметы
RU={
    "Меч":"Меч",
    "Броня":"Броня",
    "Зелье":"Зелье",
    "Золото":"Золото",
    }
def make_item():
    kind=random.choice(["Меч", "Броня","Зелье","Золото"])
    return {"type": kind}
def show_inventary():
    if not player["inventary"]:
        print("Предметов нет")
        return
    for i, it in enumerate(player["inventary"]):
        print(f" [{i}]{RU[it['type']]}")


#движение    
def move(direction):
    old_r,old_c=player["row"],player["col"]
    r,c=old_r,old_c
    if direction =="w" and r>0:
        r-=1
    elif direction =="s" and r<N-1:
        r+=1
    elif direction =="a" and c>0:
        c-=1
    elif direction =="d" and c<N-1:
        c+=1
    else:
        print("Стенка! Туда нельзя!")
        return False

    player["prev_row"],player["prev_col"]=old_r,old_c
    player["row"],player["col"]=r,c
    return True

#отображение карты
symbols={
    "empty":".","chest":"C","monster":"M","trap":"T", "key":"K", "exit":"E",
    }
def show_map():
    print()
    for r in range(N):
        line=""
        for c in range(N):
            if (r,c)==(player["row"],player["col"]):
                line+="*"
            elif (r,c)==(0,0):
                line+="S"
            elif seen[r][c]!="?":
                line+=f"{symbols[seen[r][c]]}"
            else:
                line+="?"
        print(line)
    print(f"Позиция:({player["row"]},{player["col"]}) | "
          f"HP: {player['hp']} | Ключ: {player['has_key']}")
    if player["inventary"]:
        names=[RU[it["type"]]for it in player["inventary"]]
        print("Инвентарь: "+", ".join(names))
    else:
        print("Инвентарь: пусто")

#комнаты
def enter_chest():
    item=make_item()
    player["inventary"].append(item)
    print(f"В сундуке: {RU[item['type']]}")
def enter_monster():
    print("Монстр! Что будешь делать?")
    print(" 1) Cражаться-нужен меч")
    print(" 2) Защищаться-нужна броня")
    print(" 3) Откупиться-нужно золото")
    print(" 4) У меня ничего нет")

    choice=input("Выбор(1/2/3/4): ").strip()
    if choice=="1":
        need_type="Меч"
        for it in player["inventary"]:
            if it["type"]==need_type:
                player["inventary"].remove(it)
                print("Ты убил монстра")
                break
            else:
                player["hp"]-=1
                print("Сегодня не твой день. HP={player['hp']}")
    elif choice=="2":
        need_type="Броня"
        for it in player["inventary"]:
            if it["type"]==need_type:
                player["inventary"].remove(it)
                print("Ты защитился монстра")
                break
            else:
                player["hp"]-=1
                print("Сегодня не твой день. HP={player['hp']}")

    elif choice=="3":
        need_type="Золото"
        for it in player["inventary"]:
            if it["type"]==need_type:
                player["inventary"].remove(it)
                print("Ты откупился от монстра")
                break
            else:
                player["hp"]-=1
                print("Сегодня не твой день. HP={player['hp']}")

    elif choice=="4":
        print("Сорри, бро... Монстр напал на тебя!")
        player["hp"]-=1
        return
    
def enter_trap():
    if player["inventary"]:
        idx=random.randrange(len(player["inventary"]))
        lost=player["inventary"].pop(idx)
        print(f"Ловушка! Потерян: {RU[lost['type']]}")
    else:
        player["hp"]-=1
        print(f"Ловушка! Предметов нет. HP={player['hp']}")

def use_potion():
    for i,it in enumerate(player["inventary"]):
        if it["type"]=="Зелье":
            player["inventary"].pop(i)
            player["hp"]+=1
            print(f"Выпил зелье. HP={player['hp']}")
            return
    print("Зелий нет.")

seen=[["?" for _ in range(N)] for _ in range(N)]
seen[0][0]=="empty"
def enter_room():
    r,c=player["row"], player["col"]
    room=maze[r][c]
    if seen[r][c]=="?":
        seen[r][c]=room
    print(f"\n>> Комната: {room}")

    if room=="empty":
        print("Пустая комната.")
    elif room=="chest":
        enter_chest()
        maze[r][c]="empty"
    elif room=="monster":
        enter_monster()
        maze[r][c]="empty"
    elif room=="trap":
        enter_trap()
        maze[r][c]="empty"
    elif room=="key":
        player["has_key"]=True
        print("Взял ключ! Иди к выходу!")
        maze[r][c]="empty"
    elif room=="exit":
        if player["has_key"]:
            print("ВЫХОД! ПОБЕДА!")
            return True
        else:
            print("Это выход, но нужен ключ!")
    return False
        
        
        

#главный цикл
print(f"Лабиринт {N}x{N}. Управление: w/a/s/d, q-выход, h-зелье, i-инвентарь.")
print("Обозначения: *-игрок, S-старт, .-пусто, С-сундук,")
print("             M-монстр, T-ловушка, К-ключ, Е-выход, ?-неизвестно")
show_map()
while True:
    if player["hp"]<=0:
        print("Ты погиб.Игра окончена.")
        break
    cmd=input("Ход: ").strip().lower()
    #if cmd=="q":
        #print("До встречи!")
        #break
    if cmd=="h":
        use_potion()
    elif cmd=="i":
        print("Инвентарь:")
        show_inventary()
    elif cmd in ("w","a","s","d"):
        if move(cmd):
            if enter_room():
                break
            show_map()
    else:
        print("Неизвестная команда.")
    
    

