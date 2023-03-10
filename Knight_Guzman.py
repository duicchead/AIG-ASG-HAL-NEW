import pygame

from random import randint, random
from Graph import *

from Character import *
from State import *


class Knight_Guzman(Character):

    def __init__(self, world, image, base, position):

        Character.__init__(self, world, "Myknight", image)

        self.entities = {}
        self.entity_id = 0

        self.base = base
        self.position = position
        self.move_target = GameEntity(world, "knight_move_target", None)
        self.target = None
        self.level = 0

        self.maxSpeed = 80
        self.min_target_distance = 100
        self.melee_damage = 20
        self.melee_cooldown = 2.

        self.seeking_state = KnightStateSeeking_Guzman(self)
        attacking_state = KnightStateAttacking_Guzman(self)
        ko_state = KnightStateKO_Guzman(self)
        waiting_state = KnightStateWaiting_Guzman(self)

        self.brain.add_state(self.seeking_state)
        self.brain.add_state(attacking_state)
        self.brain.add_state(ko_state)
        self.brain.add_state(waiting_state)

        self.brain.set_state("seeking")

    def render(self, surface):

        Character.render(self, surface)

    def process(self, time_passed):

        Character.process(self, time_passed)

        level_up_stats = ["hp", "speed",
                          "melee damage", "melee cooldown", "healing"]
        if self.can_level_up():
            self.level += 1
            choice = 4
            self.level_up(level_up_stats[choice])

    def enemy_base(self, char):
        for entity in self.world.entities.values():
            if entity.name == "base" and entity.team_id == 1 - char.team_id:
                return entity

    def my_base(self, char):
        for entity in self.world.entities.values():
            if entity.name == "base" and entity.team_id == char.team_id:
                return entity

    def pos_between_enemy_towers(self, char):
        temp = 0
        for entity in self.world.entities.values():
            if entity.name == "tower" and entity.team_id == 1 - char.team_id:
                temp += 1
                if temp == 1:
                    tower1 = entity
                if temp == 2:
                    tower2 = entity
            if entity.name == "base" and entity.team_id == 1 - char.team_id:
                spawnposx = entity.spawn_position[0]
                spawnposy = entity.spawn_position[1]

        if temp == 2:
            tempxvalue = (tower1.position.x - tower2.position.x) / \
                2 + tower2.position.x
            tempyvalue = (tower1.position.y - tower2.position.y) / \
                2 + tower2.position.y

            xvalue = (spawnposx - tempxvalue)/2 + tempxvalue - 7.5
            yvalue = (spawnposy - tempyvalue)/2 + tempyvalue + 8

        else:
            xvalue = 0
            yvalue = 0

        pos = Vector2(xvalue, yvalue)
        return pos

    def is_tower_down(self, char):
        temp = False
        for entity in self.world.entities.values():
            if entity.name == "tower" and entity.team_id == 1 - char.team_id and entity.current_hp <= 0:
                temp = True

        return temp


class KnightStateSeeking_Guzman(State):

    def __init__(self, knight):

        State.__init__(self, "seeking")
        self.knight = knight

        self.knight.path_graph = self.knight.world.paths[1]

    def do_actions(self):
        wizard = self.knight.world.get_entity("Mywizard")
        enemy_base = self.knight.enemy_base(self.knight)
        knight_ebase_pos = (enemy_base.position -
                            self.knight.position).length()
        wizard_ebase_pos = (enemy_base.position - wizard.position).length()
        my_base = self.knight.my_base(self.knight)
        knight_base_pos = (my_base.position - self.knight.position).length()
        wizard_base_pos = (my_base.position - wizard.position).length()

        if my_base.team_id == 0:
            range1 = 620
            #range2 = 600

        elif my_base.team_id == 1:
            range1 = 870
            #range2 = 870

        # if wizard n knight both on bot lane, rush ebase and dont return to node behind
        if (knight_base_pos >= range1 and wizard_base_pos >= range1):
            self.knight.move_target.position = enemy_base.position

        self.knight.velocity = self.knight.move_target.position - self.knight.position

        if self.knight.velocity.length() > 0:
            self.knight.velocity.normalize_ip()
            self.knight.velocity *= self.knight.maxSpeed

    def check_conditions(self):

        wizard = self.knight.world.get_entity("Mywizard")
        my_base = self.knight.my_base(self.knight)
        knight_base_pos = (my_base.position - self.knight.position).length()

        if my_base.team_id == 0:
            range1 = 620
            #range2 = 600

        elif my_base.team_id == 1:
            range1 = 870
            #range2 = 870

        # check if opponent is in range
        nearest_opponent = self.knight.world.get_nearest_opponent(self.knight)
        if nearest_opponent is not None:
            opponent_distance = (self.knight.position -
                                 nearest_opponent.position).length()

            if self.knight.current_hp < 350 and opponent_distance >= 150:
                self.knight.heal()

            if opponent_distance <= self.knight.min_target_distance:
                self.knight.target = nearest_opponent
                return "attacking"

        if (self.knight.position - self.knight.move_target.position).length() < 8:

            # continue on path
            if self.current_connection < self.path_length:
                self.knight.move_target.position = self.path[self.current_connection].toNode.position
                self.current_connection += 1

        if knight_base_pos < range1 and wizard.brain.active_state.name == "ko":
            return "waiting"

        return None

    def entry_actions(self):

        nearest_node = self.knight.path_graph.get_nearest_node(
            self.knight.position)

        self.path = pathFindAStar(self.knight.path_graph,
                                  nearest_node,
                                  self.knight.path_graph.nodes[self.knight.base.target_node_index])

        self.path_length = len(self.path)

        if (self.path_length > 0):
            self.current_connection = 0
            self.knight.move_target.position = self.path[0].fromNode.position

        else:
            self.knight.move_target.position = self.knight.path_graph.nodes[
                self.knight.base.target_node_index].position


class KnightStateWaiting_Guzman(State):

    def __init__(self, knight):

        State.__init__(self, "waiting")
        self.knight = knight

    def do_actions(self):

        my_base = self.knight.my_base(self.knight)

        self.knight.velocity = my_base.position - self.knight.position
        if self.knight.velocity.length() > 0:
            self.knight.velocity.normalize_ip()
            self.knight.velocity *= self.knight.maxSpeed

    def check_conditions(self):

        wizard = self.knight.world.get_entity("Mywizard")

        # if wizard is ko & knight was along the left lane aft leaving the base, return back to base first
        if wizard.brain.active_state.name != "ko":
            return "seeking"

        else:
            return None

    def entry_actions(self):

        return None

    def exit_actions(self):

        return None


class KnightStateAttacking_Guzman(State):

    def __init__(self, knight):

        State.__init__(self, "attacking")
        self.knight = knight
        self.prime_position = Vector2(0, 0)

    def do_actions(self):

        wizard = self.knight.world.get_entity("Mywizard")
        wizard_distance = (self.knight.position -
                           wizard.position).length()

        temp = self.knight.pos_between_enemy_towers(self.knight)
        if temp.x != 0 and temp.y != 0:
            self.prime_position = temp
            prime_spot = temp

        else:
            prime_spot = self.prime_position

        prime_pos_distance = (
            self.knight.position - prime_spot).length()

        # if near base, move towards the enemy spawn point, once enemy spawn point is in range, fire at it
        if prime_pos_distance <= 200 and self.knight.level >= 2 and wizard_distance <= 160:
            self.knight.velocity = prime_spot - self.knight.position
            if self.knight.velocity.length() > 0:
                self.knight.velocity.normalize_ip()
                self.knight.velocity *= self.knight.maxSpeed

        else:

            # colliding with target
            if pygame.sprite.collide_rect(self.knight, self.knight.target):
                self.knight.velocity = Vector2(0, 0)
                self.knight.melee_attack(self.knight.target)

            else:
                self.knight.velocity = self.knight.target.position - self.knight.position
                if self.knight.velocity.length() > 0:
                    self.knight.velocity.normalize_ip()
                    self.knight.velocity *= self.knight.maxSpeed

    def check_conditions(self):

        wizard = self.knight.world.get_entity("Mywizard")
        pos_from_wizard = (wizard.position - self.knight.position).length()

        if self.knight.current_hp < 280 and self.knight.level >= 2 and pos_from_wizard <= 300:
            self.knight.heal()

        # target is gone
        if self.knight.world.get(self.knight.target.id) is None or self.knight.target.ko:
            self.knight.target = None
            return "seeking"

        return None

    def entry_actions(self):

        return None

    def exit_actions(self):

        return None


class KnightStateKO_Guzman(State):

    def __init__(self, knight):

        State.__init__(self, "ko")
        self.knight = knight

    def do_actions(self):

        return None

    def check_conditions(self):

        # respawned
        if self.knight.current_respawn_time <= 0:
            self.knight.current_respawn_time = self.knight.respawn_time
            self.knight.ko = False
            self.knight.path_graph = self.knight.world.paths[1]
            return "seeking"

        return None

    def entry_actions(self):

        self.knight.current_hp = self.knight.max_hp
        self.knight.position = Vector2(self.knight.base.spawn_position)
        self.knight.velocity = Vector2(0, 0)
        self.knight.target = None

        return None
