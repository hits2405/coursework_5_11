from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from unit import BaseUnit, PlayerUnit, EnemyUnit
from base import Arena
from classes import unit_classes
from equipment import Equipment

app = Flask(__name__, template_folder='templates')

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()  # TODO инициализируем класс арены


@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template("index.html", heroes=heroes)


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])

    # TODO рендерим экран боя (шаблон fight.html)
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.

    if request.method == "GET":
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            "header": "Выберите героя",
            "weapons": weapons,
            "armors": armors,
            "classes": classes
        }

        return render_template('hero_choosing.html', result=result)

    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy

    elif request.method == "POST":
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']

        player_unit_class = unit_classes.get(unit_class)
        if not player_unit_class:
            return 'Ошибка героя', 300

        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        player.equip_armor(equipment.get_armor(armor_name))
        player.equip_weapon(equipment.get_weapon(weapon_name))

        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    if request.method == "GET":
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            "header": "Выберите героя",
            "weapons": weapons,
            "armors": armors,
            "classes": classes
        }

        return render_template('hero_choosing.html', result=result)

    # TODO а на POST отправляем форму и делаем редирект на начало битвы

    elif request.method == "POST":
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']

        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        enemy.equip_armor(equipment.get_armor(armor_name))

        heroes['enemy'] = enemy

        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
