import random
import pygame as pg

from cards import Card, ElmntType, Shape, CARD_WIDTH, CARD_HEIGHT, GAME_FONT, Splitterland
from goal import Gruenflaeche, Duesterwald, Pfad_des_Waldes, Bastionen, Metropole, \
    Schillernde_Ebene, Schild_des_Reichs, Schildwald
from tiles import empty_tile, mntn_tile, ruins_tile, error_tile

base_tilemap = [
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, mntn_tile, empty_tile, ruins_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, ruins_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     mntn_tile, ruins_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, mntn_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, ruins_tile, mntn_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, ruins_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, ruins_tile, empty_tile, mntn_tile,
     empty_tile, empty_tile, empty_tile],
    [empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile, empty_tile,
     empty_tile, empty_tile, empty_tile]]

mod_base_tilemap = [[y for y in x] for x in base_tilemap]

PADDING_L = 32
PADDING_T = 32

CARD_X_OFFSET = 64 * 11 + PADDING_L * 2
CARD_Y_OFFSET = PADDING_T + 128

SCREENRECT = pg.Rect(0, 0, 25 * 64 + PADDING_L, 800)

background_area = pg.Rect(PADDING_L, PADDING_T, 11 * 64, 11 * 64)

active_card = None

gold = 0
element_gold = 0
covered_mountains = 0

SPLITTERLAND = Splitterland("Splitterland",
                            [ElmntType.city, ElmntType.water, ElmntType.plains, ElmntType.forest,
                             ElmntType.monster], [Shape.splitterland], 0)

base_cards = [Card("Gehöft", [ElmntType.city, ElmntType.plains], [Shape.gehoeft], 2),
              Card("Ackerland", [ElmntType.plains], [Shape.ackerland_1, Shape.ackerland_2], 1),
              Card("Baumwipfeldorf", [ElmntType.city, ElmntType.forest], [Shape.baumwipfel], 2),
              Card("Hinterlandfluss", [ElmntType.water, ElmntType.plains], [Shape.hinterland], 2),
              Card("Weiler", [ElmntType.city], [Shape.weiler_1, Shape.weiler_2], 1),
              Card("Obsthain", [ElmntType.forest, ElmntType.plains], [Shape.obsthain], 2),
              Card("Grosser Strom", [ElmntType.water], [Shape.strom_1, Shape.strom_2], 1),
              Card("Vergessener Wald", [ElmntType.forest], [Shape.wald_1, Shape.wald_2], 1),
              Card("Sumpf", [ElmntType.forest, ElmntType.water], [Shape.sumpf], 2),
              Card("Fischerdorf", [ElmntType.city, ElmntType.water], [Shape.fischerdorf], 2),
              SPLITTERLAND,
              "RUINS", "RUINS"]

base_monster = [Card("Gnollangriff", [ElmntType.monster], [Shape.gnollangriff], 0, is_monster=True),
                Card("Goblinattacke", [ElmntType.monster], [Shape.goblinattacke], 0,
                     is_monster=True),
                Card("Koboldansturm", [ElmntType.monster], [Shape.koboldansturm], 0,
                     is_monster=True),
                Card("Grottenschratueberfall", [ElmntType.monster], [Shape.grottenschratueberfall],
                     0, is_monster=True)
                ]

forest_goals = [Gruenflaeche("Gruenflaeche"),
                Duesterwald("Duesterwald"),
                Pfad_des_Waldes("Pfad des Waldes"),
                Schildwald("Schildwald")]

city_goals = [Bastionen("Bastionen in der Wildnis"),
              Metropole("Metropole"),
              Schillernde_Ebene("Schillernde Ebene"),
              Schild_des_Reichs("Schild des Reiches")]

water_plains_goals = []

landscape_goals = []

base_goals = [Schillernde_Ebene("Schillernd"), Schild_des_Reichs("Schild des Reiches")]

# TODO implement random choice for each when goals are implemented
forest_goal = base_goals[0]
city_goal = base_goals[0]
water_plains_goal = base_goals[1]
landscape_goal = base_goals[1]

active_goals = [forest_goal, city_goal, water_plains_goal, landscape_goal]
random.shuffle(active_goals)

active_monster = []

cards = []


def fill_up_cards():
    cards.clear()
    for x in base_cards:
        cards.append(x)

    active_monster.append(base_monster.pop())

    print("Active monster:", [x.name for x in active_monster])

    cards.extend(active_monster)

    random.shuffle(cards)
    print("Cards after shuffle:")
    print([x.name if isinstance(x, Card) else "Ruins" for x in cards])


def draw_tilemap_seasons(tilemap):
    screen.fill((125, 90, 82))
    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            screen.blit(tilemap[row][column].draw(),
                        (PADDING_L + column * 64, PADDING_T + row * 64))

    draw_seasons()


def draw_sprite_at_mouse_pos(element):
    ele_sprite = pg.sprite.RenderPlain(element)
    ele_sprite.update()
    draw_tilemap_seasons(base_tilemap)
    screen.blit(active_card.draw(), (CARD_X_OFFSET, CARD_Y_OFFSET))
    draw_score_and_goals()
    ele_sprite.draw(screen)


def draw_seasons():
    global active_card
    seasons_surface = pg.Surface((6 * 64, 64))
    seasons_surface.fill((96, 50, 40))
    GAME_FONT.render_to(seasons_surface, (10, 12), active_season, (200, 200, 100))
    GAME_FONT.render_to(seasons_surface, (5 * 64, 12),
                        str(season_active_value) + "/" + str(seasons[active_season]),
                        (200, 200, 100))
    screen.blit(seasons_surface, (CARD_X_OFFSET, PADDING_T))

    # blit gold values
    GAME_FONT.render_to(screen, (PADDING_L, PADDING_T + 64 * 11 + PADDING_T // 2),
                        "Gold: {0}".format(gold))

    # TODO das hier sauber machen, global zeug auch sauber machen
    if active_card and not isinstance(active_card, str) and active_card.needs_ruins:
        ruins_surface = pg.Surface((6 * 64, 64))
        ruins_surface.fill((100, 60, 70))
        GAME_FONT.render_to(ruins_surface, (10, 12), "PLACE ON RUINS!", (200, 200, 100))
        screen.blit(ruins_surface, (CARD_X_OFFSET, PADDING_T + 64))


# 3am code :>
def check_season_over():
    global active_season, season_active_value, ruins_this_season
    if season_active_value >= seasons[active_season]:
        print("New Season!")
        # TODO das geht schöner ....
        if active_season == "Fruehling":
            active_season = "Sommer"
            score_counter = 0
        elif active_season == "Sommer":
            active_season = "Herbst"
            score_counter = 1
        elif active_season == "Herbst":
            active_season = "Winter"
            score_counter = 2
        elif active_season == "Winter":
            print("Wertung und Spielende!")
            score_counter = 3

        quad = scores_quads[score_counter]
        quad.gold = gold

        monster_count = check_monster_count()
        quad.monster = monster_count

        print("--------------- COMPUTING GOAL 1 ---------------")
        quad.first = active_goals[score_counter % 4].points_for_goal(base_tilemap)
        print("--------------- COMPUTING GOAL 2 ---------------")
        quad.second = active_goals[(score_counter + 1) % 4].points_for_goal(base_tilemap)

        season_active_value = 0
        ruins_this_season = 0
        fill_up_cards()


def check_monster_count():
    empty_monster_neighbours = []
    neighbours_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for row_i, base_row in enumerate(base_tilemap):
        for col_i, base_col in enumerate(base_row):
            if base_col.name == "Monster":

                monster_neighbours = [base_tilemap[row_i + x][col_i + y] for
                                      (x, y) in neighbours_list
                                      if
                                      10 >= row_i + x >= 0 and 10 >= col_i + y >= 0]

                for i, neighbour in enumerate(monster_neighbours):
                    if neighbour.name in ["Empty", "Ruins"]:
                        empty_monster_neighbours.append(
                            (row_i + neighbours_list[i][0], col_i + neighbours_list[i][1]))
    print("monster list:", empty_monster_neighbours)
    monster_count = len(set(empty_monster_neighbours))
    return monster_count


def get_new_card():
    card = cards.pop()
    if isinstance(card, str):
        print("--------------RUINS---------------")
        card = cards.pop()
        if isinstance(card, str):
            card = cards.pop()  # TODO hardcoded for two ruins...
        card.needs_ruins = True
    else:
        card.needs_ruins = False  # I dont know why this is needed, but without sometimes needs_ruins ist wrongfully True ???
    return card


def compute_placeable_positions(base_shape):
    placeable_positions = []
    rotated_shapes = []
    all_shapes = []
    rotated_shapes.append(base_shape)
    all_shapes.append(base_shape)
    for o in range(3):
        base_shape = list(list(x) for x in zip(*base_shape[::-1]))
        rotated_shapes.append(base_shape)
        all_shapes.append(base_shape)

    for r_shape in rotated_shapes:
        mirrored = [x[::-1] for x in r_shape]
        all_shapes.append(mirrored)
    # TODO remove duplicates

    # sick magic! (not really, just loopy code)
    # Loops over all 11x11 fields and tries to fit the shape in its current rotation on the field
    # if this is possible, the x,y coordinates + current shape get returned
    for shape in all_shapes:
        for map_row in range(11):
            for map_col in range(11):
                point_valid = True

                if map_row + len(shape) > 11 or map_col + len((shape[0])) > 11:
                    continue

                for row_index, ele_row in enumerate(shape):
                    if point_valid == False:
                        break
                    for col_index, ele_col in enumerate(ele_row):
                        if ele_col == 1:

                            if base_tilemap[map_row + row_index][
                                map_col + col_index].name not in ["Empty", "Ruins"]:
                                point_valid = False
                if point_valid:
                    placeable_positions.append(((map_row, map_col), shape))

    return placeable_positions


class ScoreQuad:

    def __init__(self):
        self.surface = pg.Surface((128, 128))
        self.set_base()

        self.first = 0
        self.second = 0
        self.gold = 0
        self.monster = 0

    def set_base(self):
        self.surface.fill((101, 60, 60))
        outline = (0, 0, 127, 127)
        pg.draw.rect(self.surface, (0, 0, 0), outline, 2)
        pg.draw.line(self.surface, (0, 0, 0), (64, 0), (64, 128), 2)
        pg.draw.line(self.surface, (0, 0, 0), (0, 64), (128, 64), 2)

    def draw(self):
        self.set_base()
        font = pg.font.SysFont('arial', 40)

        gold_val = font.render(str(self.gold), True, (0, 0, 0))
        monster_val = font.render(str(self.monster), True, (255, 0, 0))
        first_val = font.render(str(self.first), True, (0, 0, 0))
        second_val = font.render(str(self.second), True, (0, 0, 0))

        self.surface.blit(gold_val, (28, 64 + 16))
        self.surface.blit(monster_val, ((64 + 28, 64 + 16)))
        self.surface.blit(first_val, (28, 16))
        self.surface.blit(second_val, (64 + 28, 16))

        return self.surface


scores_quads = [ScoreQuad(), ScoreQuad(), ScoreQuad(), ScoreQuad()]


def draw_score_and_goals():
    score_padding = 32

    score_screen = pg.Surface((3 * 64, 8 * 64 + 5 * score_padding))
    score_screen.fill((96, 50, 40))

    for i, quad in enumerate(scores_quads):
        score_screen.blit(quad.draw(), (score_padding, score_padding + i * (128 + score_padding)))

    screen.blit(score_screen, (7 * 64 + 11 * 64 + PADDING_L, PADDING_T))

    goals_screen = pg.Surface((3 * 64, 8 * 64 + 5 * score_padding))
    goals_screen.fill((96, 50, 40))

    abcd = "ABCD"
    for i, goal in enumerate(active_goals):
        font = pg.font.SysFont('arial', 28)
        abcd_font = font.render(abcd[i] + ":", True, (100, 220, 40))
        goal_name = font.render(goal.name, True, (0, 0, 0))
        goals_screen.blit(abcd_font, (score_padding, score_padding + i * (128 + score_padding)))
        goals_screen.blit(goal_name, (
            score_padding, score_padding + i * (128 + score_padding) + score_padding))

    screen.blit(goals_screen, (7 * 64 + 11 * 64 + PADDING_L + 3 * 64 + PADDING_L, PADDING_T))


if __name__ == '__main__':

    pg.init()

    fullscreen = False
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pg.display.set_caption("Kartograph")

    # season counter:
    seasons = {"Fruehling": 7, "Sommer": 7, "Herbst": 6, "Winter": 5}

    season_active_value = 0
    active_season = "Fruehling"

    ruins_this_season = 0

    fill_up_cards()
    active_card = get_new_card()

    draw_tilemap_seasons(base_tilemap)
    pg.display.flip()

    game_active = True

    card_area = pg.Rect(CARD_X_OFFSET, CARD_Y_OFFSET, CARD_WIDTH, CARD_HEIGHT)

    # initial card
    screen.blit(active_card.draw(), (CARD_X_OFFSET, CARD_Y_OFFSET))
    draw_score_and_goals()

    # tells whether the user has a card picked up at the moment
    is_card_picked_up = False
    # the element that the user has picked up
    picked_up_element = None

    while game_active:

        for event in pg.event.get():

            mouse = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                game_active = False

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[
                0] and not is_card_picked_up:

                # there should not be any string left, still checking :>
                if not isinstance(active_card, Splitterland) and isinstance(active_card,
                                                                            Card) and not active_card.is_monster:

                    x, y, xl, yl = active_card.area1
                    area1_rect = pg.Rect(x + CARD_X_OFFSET, y + CARD_Y_OFFSET, xl, yl)
                    x, y, xl, yl = active_card.area2
                    area2_rect = pg.Rect(x + CARD_X_OFFSET, y + CARD_Y_OFFSET, xl, yl)

                    if area1_rect.collidepoint(mouse):
                        is_card_picked_up = True
                        picked_up_element = active_card.ele1

                    if area2_rect.collidepoint(mouse):
                        is_card_picked_up = True
                        picked_up_element = active_card.ele2

                # TODO refactor the whole monster thing, its just hacky right now
                elif active_card.is_monster:
                    active_card.needs_ruins = False
                    x, y, xl, yl = active_card.area1
                    area1_rect = pg.Rect(x + CARD_X_OFFSET, y + CARD_Y_OFFSET, xl, yl)
                    if area1_rect.collidepoint(mouse):
                        is_card_picked_up = True
                        picked_up_element = active_card.ele1

                # card is a splitterland, which is a unique case for pick up
                elif isinstance(active_card, Splitterland):

                    outlines = active_card.area1

                    for i, outline in enumerate(outlines):
                        x, y, xl, yl = outline
                        rect = pg.Rect(x + CARD_X_OFFSET, y + CARD_Y_OFFSET, xl, yl)
                        if rect.collidepoint(mouse):
                            is_card_picked_up = True
                            picked_up_element = active_card.ele1[i]
                else:
                    print("ERROR: This should never be reached, card type:", type(active_card))

            if is_card_picked_up:
                # card is picked up, user right clicks -> put element back (not picked up anymore)
                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]:
                    is_card_picked_up = False
                    draw_tilemap_seasons(base_tilemap)
                    screen.blit(active_card.draw(), (CARD_X_OFFSET, CARD_Y_OFFSET))
                    draw_score_and_goals()
                    # draw_seasons() # TODO alles in eine methode? mit card und tile set?
                    picked_up_element = None
                    break

                # outside of the playing field, just draw the sprite at mouse pos
                if not background_area.collidepoint(mouse):
                    draw_sprite_at_mouse_pos(picked_up_element)

                # rotating/mirroring
                if event.type == pg.KEYDOWN:
                    # rotate by pressing R
                    if event.key == pg.K_r:
                        ele_shape = picked_up_element.shape
                        new_shape = list(zip(*ele_shape[::-1]))
                        picked_up_element.shape = new_shape
                    # mirror by pressing E
                    if event.key == pg.K_e:
                        def mirror(seq):
                            return [x[::-1] for x in seq]


                        ele_shape = picked_up_element.shape
                        new_shape = mirror(ele_shape)
                        picked_up_element.shape = new_shape

                # mouse is over the playing field -> element should lock to tiles
                elif background_area.collidepoint(mouse):
                    is_placeable = True
                    temp_tiles = mod_base_tilemap

                    m_x, m_y = mouse

                    map_col = (m_x - PADDING_L) // 64
                    map_row = (m_y - PADDING_T) // 64

                    ele_shape = picked_up_element.shape
                    # check if parts of the tile are outside the playing field
                    if map_row + len(ele_shape) > 11 or map_col + len((ele_shape[0])) > 11:
                        draw_sprite_at_mouse_pos(picked_up_element)
                        continue

                    # if all parts are inside, check all positions
                    for row_index, ele_row in enumerate(ele_shape):
                        for col_index, ele_col in enumerate(ele_row):
                            if ele_col == 1:
                                # if a tile is occupied already -> show Error tile
                                if base_tilemap[map_row + row_index][
                                    map_col + col_index].name not in ["Empty", "Ruins"]:
                                    temp_tiles[map_row + row_index][
                                        map_col + col_index] = error_tile
                                    is_placeable = False
                                # else lock the tile in place (temporarily)
                                else:
                                    temp_tiles[map_row + row_index][
                                        map_col + col_index] = picked_up_element.elmnt_type

                    # user clicks and card is at a valid spot:
                    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[
                        0] and is_placeable:

                        if active_card.needs_ruins:
                            is_ruins_satisfied = False
                            # TODO loopen in methode auslagern, die genau die felder zurckgibt oder so
                            for row_index, ele_row in enumerate(ele_shape):
                                for col_index, ele_col in enumerate(ele_row):
                                    if ele_col == 1:
                                        if base_tilemap[map_row + row_index][
                                            map_col + col_index].name == "Ruins":
                                            is_ruins_satisfied = True
                            if not is_ruins_satisfied:
                                break

                        # store the new tiles in the base tilemap
                        for row_index, ele_row in enumerate(ele_shape):
                            for col_index, ele_col in enumerate(ele_row):
                                if ele_col == 1:
                                    base_tilemap[map_row + row_index][
                                        map_col + col_index] = picked_up_element.elmnt_type
                        is_card_picked_up = False

                        if picked_up_element.gives_gold:
                            element_gold += 1

                        # check if tile covers a mountain
                        covered_mountains = 0
                        for row_i, base_row in enumerate(base_tilemap):
                            for col_i, base_col in enumerate(base_row):
                                if base_col.name == "Mountain":
                                    # TODO make this more generic for maps where mountains could be at the edge
                                    mountain_neighbours = [base_tilemap[row_i + x][col_i + y] for
                                                           (x, y) in
                                                           [(1, 0), (0, 1), (-1, 0), (0, -1)]]

                                    covered = all(
                                        [True if tile.name not in ["Empty", "Ruins"] else False for
                                         tile
                                         in mountain_neighbours])
                                    if covered:
                                        covered_mountains += 1

                        gold = element_gold + covered_mountains

                        # add season value of active card
                        season_active_value += active_card.value

                        check_season_over()

                        # get new card
                        active_card = get_new_card()
                        print("Name", active_card.name)
                        print("Need ruins?", active_card.needs_ruins)

                        if not isinstance(active_card, Splitterland) and isinstance(active_card,
                                                                                    Card) and not active_card.is_monster:
                            print("Not monster not splitterland checking for shape:")
                            placeable_positions = compute_placeable_positions(
                                active_card.ele1.shape)
                            placeable_positions += compute_placeable_positions(
                                active_card.ele2.shape)

                            if not placeable_positions:
                                print(
                                    "No placeable positions (without regard to ruins, changing to Splitterland")
                                active_card = SPLITTERLAND
                                active_card.needs_ruins = False
                            else:
                                print("Card can be placed!")

                        elif active_card.is_monster:
                            active_card.needs_ruins = False
                            print("Monster shape:")
                            print(active_card.ele1.shape)
                            placeable_positions = compute_placeable_positions(
                                active_card.ele1.shape)

                            active_monster.remove(active_card)

                            if not placeable_positions:
                                print("Cant place monster, creating new 1x1 Monster")
                                active_card = Card("1x1 Monster", [ElmntType.monster],
                                                   [Shape.splitterland], 0, is_monster=True)
                                active_card.needs_ruins = False

                        if active_card.needs_ruins:
                            # there are no ruins left on the field, so ruins card needs to be exchanged for splitterland
                            if "Ruins" not in [x.name for row in base_tilemap for x in row]:
                                active_card = SPLITTERLAND
                                active_card.needs_ruins = False
                                print("No ruins left on field, change to Splitterland.")
                            # there are still ruins left, but maybe the active card still cant be played over ruins/or at all
                            else:
                                if not isinstance(active_card, Splitterland):
                                    valid_found = False
                                    for pos, shape in placeable_positions:
                                        if valid_found:
                                            print(
                                                "There is at least 1 valid position with RUINS left")
                                            break
                                        for row_index, ele_row in enumerate(shape):
                                            for col_index, ele_col in enumerate(ele_row):
                                                if ele_col == 1:
                                                    if base_tilemap[pos[0] + row_index][
                                                        pos[1] + col_index].name == "Ruins":
                                                        valid_found = True

                                    if not valid_found:
                                        print(
                                            "There are still ruins left, but not compatible for shape!")
                                        print("Changing card to splitterland.")
                                        active_card = SPLITTERLAND
                                        active_card.needs_ruins = False
                                else:
                                    print("Player needs to put the Splitterland on a ruin field!")

                    draw_tilemap_seasons(base_tilemap)
                    draw_tilemap_seasons(temp_tiles)

                    screen.blit(active_card.draw(), (CARD_X_OFFSET, CARD_Y_OFFSET))
                    draw_score_and_goals()

                    # FIXME! cant use deepcopy, so we need to individually reset mod_base_tilemap
                    for r in range(len(mod_base_tilemap)):
                        for c in range(len(mod_base_tilemap)):
                            mod_base_tilemap[r][c] = base_tilemap[r][c]

        pg.display.flip()
