from typing import Optional

from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        Проверка здоровья игрока и соперника
        """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Результат игры: Ничья"

        if self.player.hp <= 0:
            self.battle_result = "Результат игры: Игрок проиграл битву"

        if self.enemy.hp <= 0:
            self.battle_result = "Результат игры: Игрок выиграл битву"

        return self._end_game()

    def _stamina_regeneration(self):
        """
        регенерация выносливости для игрока и врага за ход
        """
        if self.player.stamina + (self.STAMINA_PER_ROUND * self.player.unit_class.stamina_mltplr) >= self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        else:
            self.player.stamina += self.STAMINA_PER_ROUND * self.player.unit_class.stamina_mltplr

        if self.enemy.stamina + (self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina_mltplr) >= self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        else:
            self.enemy.stamina += self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina_mltplr

    def next_turn(self):
        """
        Срабатывает когда игрок пропускает ход или когда игрок наносит удар
        """
        # Проверка здоровья игрока и соперника
        result = self._check_players_hp()
        # если есть результат битвы, возвращается строкой итог битвы и информация о победителе.
        if result:
            return result

        # если бой продолжается, то каждый игрок регенерирует выносливость за ход
        self._stamina_regeneration()
        # вызывается функция по ответному удару врага
        return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):

        # Проверка здоровья игрока и соперника и наличие итога боя.
        result = self._check_players_hp()
        if result:
            return result

        # если бой не закончен, игрок наносит удар и в ответ получает удар соперника.
        result_by_player = self.player.hit(self.enemy)
        result_by_enemy = self.next_turn()
        return f"{result_by_player} {result_by_enemy} "

    def player_use_skill(self):
        # Проверка здоровья игрока и соперника и наличие итога боя.
        result = self._check_players_hp()
        if result:
            return result

        # если бой не закончен, игрок использует умение, а соперник выполняет свою атаку.
        result_by_player = self.player.use_skill(self.enemy)
        result_by_enemy = self.next_turn()
        return f"{result_by_player} {result_by_enemy} "