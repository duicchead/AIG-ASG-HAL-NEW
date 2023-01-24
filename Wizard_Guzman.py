import pygame

from random import randint, random
from Graph import *

from Character import *
from State import *
from GameEntity import *


class Wizard_Guzman(Character):

    def __init__(self, world, image, projectile_image, base, position, explosion_image=None):

        Character.__init__(self, world, "Mywizard", image)

        self.entities = {}
        self.entity_id = 0

        self.projectile_image = projectile_image
        self.explosion_image = explosion_image

        self.path = []
        self.base = base
        self.position = position
        self.move_target = GameEntity(world, "wizard_move_target", None)
        self.target = None
        self.level = 0

        self.maxSpeed = 50
        self.min_target_distance = 100
        self.projectile_range = 100
        self.projectile_speed = 100

        seeking_state = WizardStateSeeking_Guzman(self)
        attacking_state = WizardStateAttacking_Guzman(self)
        ko_state = WizardStateKO_Guzman(self)

        self.brain.add_state(seeking_state)
        self.brain.add_state(attacking_state)
        self.brain.add_state(ko_state)

        self.brain.set_state("seeking")

    def render(self, surface):

        Character.render(self, surface)

    def process(self, time_passed):

        Character.process(self, time_passed)

        level_up_stats = ["hp", "speed", "ranged damage",
                          "ranged cooldown", "projectile range"]
        if self.can_level_up():
            self.level += 1
            if self.level >= 2:
                self.level_up(level_up_stats[3])
            else:
                self.level_up(level_up_stats[3])

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

    def get_knight(self, char):
        for entity in self.world.entities.values():
            if entity.name == "Myknight" and entity.team_id == char.team_id:
                return entity


class WizardStateSeeking_Guzman(State):

    def __init__(self, wizard):

        State.__init__(self, "seeking")
        self.wizard = wizard
        self.path = []

        self.wizard.path_graph = self.wizard.world.paths[1]

    def do_actions(self):

        knight = self.wizard.world.get_entity("Myknight")
        enemy_base = self.wizard.enemy_base(self.wizard)
        my_base = self.wizard.my_base(self.wizard)

        knight_base_pos = (my_base.position - knight.position).length()
        wizard_base_pos = (my_base.position - self.wizard.position).length()

        knight_ebase_pos = (enemy_base.position - knight.position).length()
        wizard_ebase_pos = (enemy_base.position -
                            self.wizard.position).length()

        if my_base.team_id == 0:
            range1 = 565
            range2 = 490

        elif my_base.team_id == 1:
            range1 = 850
            range2 = 340

        # if wizard and knight are close, move
        if (knight_base_pos < range1 and wizard_base_pos < range1):
            self.wizard.velocity = knight.position - self.wizard.position

        elif (knight_base_pos >= range1 and wizard_base_pos >= range1):
            self.wizard.velocity = knight.position - self.wizard.position

        else:
            # astar =============================================================
            nearest_node = self.wizard.path_graph.get_nearest_node(
                self.wizard.position)

            self.path = pathFindAStar(self.wizard.path_graph,
                                      nearest_node,
                                      self.wizard.path_graph.nodes[self.wizard.base.target_node_index])

            self.path_length = len(self.path)

            if (self.path_length > 0):
                self.current_connection = 0
                self.wizard.move_target.position = self.path[0].fromNode.position

            else:
                self.wizard.move_target.position = self.wizard.path_graph.nodes[
                    self.wizard.base.target_node_index].position
            # astar ===========================================================
            self.wizard.velocity = self.wizard.move_target.position - self.wizard.position

        if (wizard_ebase_pos < range2):
            # astar =============================================================
            nearest_node = self.wizard.path_graph.get_nearest_node(
                self.wizard.position)

            self.path = pathFindAStar(self.wizard.path_graph,
                                      nearest_node,
                                      self.wizard.path_graph.nodes[self.wizard.base.target_node_index])

            self.path_length = len(self.path)

            if (self.path_length > 0):
                self.current_connection = 0
                self.wizard.move_target.position = self.path[0].fromNode.position

            else:
                self.wizard.move_target.position = self.wizard.path_graph.nodes[
                    self.wizard.base.target_node_index].position
            # astar ===========================================================
            self.wizard.velocity = self.wizard.move_target.position - self.wizard.position

        if self.wizard.velocity.length() > 0:
            self.wizard.velocity.normalize_ip()
            self.wizard.velocity *= self.wizard.maxSpeed

        nearest_opponent = self.wizard.world.get_nearest_opponent(self.wizard)
        opponent_distance = (self.wizard.position -
                             nearest_opponent.position).length()

        if opponent_distance > 200 and self.wizard.current_hp < self.wizard.max_hp:
            self.wizard.heal()

    def check_conditions(self):
        nearest_opponent = self.wizard.world.get_nearest_opponent(self.wizard)
        opponent_distance = (self.wizard.position -
                             nearest_opponent.position).length()

        # check if opponent is in range
        nearest_opponent = self.wizard.world.get_nearest_opponent(self.wizard)
        if nearest_opponent is not None:
            opponent_distance = (self.wizard.position -
                                 nearest_opponent.position).length()
            if opponent_distance <= self.wizard.min_target_distance:
                self.wizard.target = nearest_opponent
                return "attacking"

        if (self.wizard.position - self.wizard.move_target.position).length() < 8:

            # continue on path
            if self.current_connection < self.path_length:
                self.wizard.move_target.position = self.path[self.current_connection].toNode.position
                self.current_connection += 1

        return None

    def entry_actions(self):

        nearest_node = self.wizard.path_graph.get_nearest_node(
            self.wizard.position)

        self.path = pathFindAStar(self.wizard.path_graph,
                                  nearest_node,
                                  self.wizard.path_graph.nodes[self.wizard.base.target_node_index])

        self.path_length = len(self.path)

        if (self.path_length > 0):
            self.current_connection = 0
            self.wizard.move_target.position = self.path[0].fromNode.position

        else:
            self.wizard.move_target.position = self.wizard.path_graph.nodes[
                self.wizard.base.target_node_index].position


class WizardStateAttacking_Guzman(State):

    def __init__(self, wizard):

        State.__init__(self, "attacking")
        self.wizard = wizard
        self.spam_middle = False
        self.prime_position = Vector2(0, 0)

    def do_actions(self):
        knight = self.wizard.get_knight(self.wizard)
        Ebase = self.wizard.enemy_base(self.wizard)

        temp = self.wizard.pos_between_enemy_towers(self.wizard)
        if temp.x != 0 and temp.y != 0:
            self.prime_position = temp
            prime_spot = temp

        else:
            prime_spot = self.prime_position

        opponent_distance = (self.wizard.position -
                             self.wizard.target.position).length()

        # opponent within range
        if opponent_distance <= self.wizard.min_target_distance:

            prime_pos_distance = (self.wizard.position - prime_spot).length()

            self.wizard.velocity = Vector2(0, 0)
            if self.wizard.current_ranged_cooldown <= 0:  # if ready to fire

                # if near the prime hitting spot, move towards the spot
                if prime_pos_distance <= 250 and knight.level >= 2:
                    self.wizard.velocity = prime_spot - self.wizard.position
                    if self.wizard.velocity.length() > 0:
                        self.wizard.velocity.normalize_ip()
                        self.wizard.velocity *= self.wizard.maxSpeed

                    # if prime hitting spot is in my target range, attack it; IMPORTANT; can just replace targetpos with prime_spot
                    if prime_pos_distance <= self.wizard.min_target_distance and (knight.position - self.wizard.position).length() <= self.wizard.min_target_distance:
                        self.wizard.target = knight
                        self.wizard.velocity = self.wizard.position - self.wizard.position

                        self.wizard.spam_middle = True
                        self.wizard.ranged_attack(
                            self.wizard.target.position, self.wizard.explosion_image)

                    # if not near prime hitting spot, hit whatever is in range of me
                    if (knight.position - self.wizard.position).length() >= 275:
                        self.wizard.spam_middle = False
                        nearest_opponent = self.wizard.world.get_nearest_opponent(
                            self.wizard)
                        if nearest_opponent is not None:
                            opponent_distance = (self.wizard.position -
                                                 nearest_opponent.position).length()
                            if opponent_distance <= self.wizard.min_target_distance:
                                self.wizard.target = nearest_opponent

                        self.wizard.spam_middle = False
                        self.wizard.ranged_attack(
                            self.wizard.target.position, self.wizard.explosion_image)

                else:  # if not near prime hitting spot, hit whatever is in range of me
                    self.wizard.spam_middle = False
                    nearest_opponent = self.wizard.world.get_nearest_opponent(
                        self.wizard)
                    if nearest_opponent is not None:
                        opponent_distance = (self.wizard.position -
                                             nearest_opponent.position).length()
                        if opponent_distance <= self.wizard.min_target_distance:
                            self.wizard.target = nearest_opponent

                    self.wizard.spam_middle = False
                    self.wizard.ranged_attack(
                        self.wizard.target.position, self.wizard.explosion_image)

    def check_conditions(self):

        # target is gone
        if self.wizard.world.get(self.wizard.target.id) is None and self.wizard.spam_middle == False or self.wizard.target.ko:
            self.wizard.target = None
            return "seeking"

        return None

    def entry_actions(self):

        return None


class WizardStateKO_Guzman(State):

    def __init__(self, wizard):

        State.__init__(self, "ko")
        self.wizard = wizard

    def do_actions(self):

        return None

    def check_conditions(self):

        # respawned
        if self.wizard.current_respawn_time <= 0:
            self.wizard.current_respawn_time = self.wizard.respawn_time
            self.wizard.ko = False
            self.wizard.path_graph = self.wizard.world.paths[1]
            return "seeking"

        return None

    def entry_actions(self):

        self.wizard.current_hp = self.wizard.max_hp
        self.wizard.position = Vector2(self.wizard.base.spawn_position)
        self.wizard.velocity = Vector2(0, 0)
        self.wizard.target = None

        return None
