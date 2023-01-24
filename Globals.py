DEBUG = True
SHOW_PATHS = False
SHOW_SPLASH = True
SPEED_MULTIPLIER = 2.0

RED_MULTIPLIER = 1.15       # Set this to 1.0 for Easy Mode
# Set this to 1.15 for Hard Mode

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

TIME_LIMIT = 180 * 1 / SPEED_MULTIPLIER

TEAM_NAME = ["Guzman", "TeamB"]

RESPAWN_TIME = 5. * 1 / SPEED_MULTIPLIER
HEALING_COOLDOWN = 2. * 1 / SPEED_MULTIPLIER
HEALING_PERCENTAGE = 20

# --- Unit initial values ---
BASE_MAX_HP = 1000
BASE_MIN_TARGET_DISTANCE = 220
BASE_PROJECTILE_RANGE = BASE_MIN_TARGET_DISTANCE
BASE_PROJECTILE_SPEED = 300 * SPEED_MULTIPLIER
BASE_RANGED_DAMAGE = 50     # buffed from 40
BASE_RANGED_COOLDOWN = 3. * 1 / SPEED_MULTIPLIER
BASE_SPAWN_COOLDOWN = 4. * 1 / SPEED_MULTIPLIER

TOWER_MAX_HP = 500
TOWER_MIN_TARGET_DISTANCE = 160
TOWER_PROJECTILE_RANGE = BASE_MIN_TARGET_DISTANCE
TOWER_PROJECTILE_SPEED = 200 * SPEED_MULTIPLIER
TOWER_RANGED_DAMAGE = 40    # buffed from 30
TOWER_RANGED_COOLDOWN = 3. * 1 / SPEED_MULTIPLIER

GREY_TOWER_MIN_TARGET_DISTANCE = 220
GREY_TOWER_PROJECTILE_RANGE = BASE_MIN_TARGET_DISTANCE
GREY_TOWER_PROJECTILE_SPEED = 300 * SPEED_MULTIPLIER
GREY_TOWER_RANGED_DAMAGE = 40   # buffed from 30
GREY_TOWER_RANGED_COOLDOWN = 3. * 1 / SPEED_MULTIPLIER

ORC_MAX_HP = 100
ORC_MAX_SPEED = 50 * SPEED_MULTIPLIER
ORC_MIN_TARGET_DISTANCE = 120
ORC_MELEE_DAMAGE = 20
ORC_MELEE_COOLDOWN = 2. * 1 / SPEED_MULTIPLIER

KNIGHT_MAX_HP = 400     # nerfed from 450
KNIGHT_MAX_SPEED = 80 * SPEED_MULTIPLIER
KNIGHT_MIN_TARGET_DISTANCE = 150
KNIGHT_MELEE_DAMAGE = 40
KNIGHT_MELEE_COOLDOWN = 1.5 * 1 / SPEED_MULTIPLIER

ARCHER_MAX_HP = 200
ARCHER_MAX_SPEED = 100 * SPEED_MULTIPLIER
ARCHER_MIN_TARGET_DISTANCE = 150
ARCHER_PROJECTILE_RANGE = BASE_MIN_TARGET_DISTANCE
ARCHER_PROJECTILE_SPEED = 300 * SPEED_MULTIPLIER
ARCHER_RANGED_DAMAGE = 35   # buffed from 30
ARCHER_RANGED_COOLDOWN = 1. * 1 / SPEED_MULTIPLIER

WIZARD_MAX_HP = 150
WIZARD_MAX_SPEED = 60 * SPEED_MULTIPLIER
WIZARD_MIN_TARGET_DISTANCE = 150
WIZARD_PROJECTILE_RANGE = BASE_MIN_TARGET_DISTANCE
WIZARD_PROJECTILE_SPEED = 200 * SPEED_MULTIPLIER
WIZARD_RANGED_DAMAGE = 50
WIZARD_RANGED_COOLDOWN = 2. * 1 / SPEED_MULTIPLIER  # buffed from 2.5

# --- Level up values ---
XP_TO_LEVEL = 100
UP_PERCENTAGE_HP = 10
UP_PERCENTAGE_SPEED = 10
UP_PERCENTAGE_MELEE_DAMAGE = 10
UP_PERCENTAGE_MELEE_COOLDOWN = 10
UP_PERCENTAGE_RANGED_DAMAGE = 10
UP_PERCENTAGE_RANGED_COOLDOWN = 10
UP_PERCENTAGE_PROJECTILE_RANGE = 10
UP_PERCENTAGE_HEALING = 20
UP_PERCENTAGE_HEALING_COOLDOWN = 10
