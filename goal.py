# TODO Use english names for goals, rethink whole goal class system
class Goal:
    def __init__(self, name):
        self.name = name

    def points_for_goal(self, tilemap):
        return None

    def get_chunks(self, tilemap, tile_type):

        tiles_of_type = []

        for row_i, base_row in enumerate(tilemap):
            for col_i, base_col in enumerate(base_row):
                if base_col.name == tile_type:
                    tiles_of_type.append((row_i, col_i))

        already_seen = []

        def find_chunk(tiles):

            already_seen.extend(tiles)
            all_neighbours = []

            for tile in tiles:
                row, col = tile
                neighbours_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                neighbours = [(row + y, col + x) for
                              (y, x) in neighbours_list
                              if
                              10 >= row + y >= 0 and 10 >= col + x >= 0 and (
                                  row + y, col + x) in tiles_of_type and (
                                  row + y, col + x) not in tiles and (
                                  row + y, col + x) not in already_seen
                              ]
                all_neighbours.extend(neighbours)

            if not all_neighbours:
                return tiles

            return tiles + list(set(find_chunk(all_neighbours)))

        all_chunks = []
        tiles_part_of_chunk = []
        print("Tiles of type", tiles_of_type)
        for tile in tiles_of_type:

            if tile in tiles_part_of_chunk:
                continue

            print("Starting search from", tile)
            already_seen.clear()
            active_chunk = find_chunk([tile])
            all_chunks.append(active_chunk)

            tiles_part_of_chunk.extend(active_chunk)

        return all_chunks

    # gets all neighbours of a chunk that are not of the same type as the chunk
    def get_neighbours_of_chunk(self, tilemap, chunk, chunk_type):

        def get_neighbours_not_of_type(row_y, col_x, tile_type):
            neighbours_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            neighbours = [(row_y + y, col_x + x) for
                          (y, x) in neighbours_list
                          if
                          10 >= row_y + y >= 0 and 10 >= col_x + x >= 0 and tilemap[row_y + y][
                              col_x + x].name != tile_type]
            return neighbours

        neighbours = []
        for tile in chunk:
            for n in get_neighbours_not_of_type(tile[0], tile[1], chunk_type):
                if n not in neighbours:
                    neighbours.append(tilemap[n[0]][n[1]])

        return neighbours


class ForestGoal(Goal):

    def points_for_goal(self, tilemap):
        return None


class CityGoal(Goal):

    def points_for_goal(self, tilemap):
        return None


class Bastionen(CityGoal):
    def points_for_goal(self, tilemap):
        points = 0

        city_chunks = self.get_chunks(tilemap, "City")

        for chunk in city_chunks:
            if len(chunk) >= 6:
                points += 8

        return points


class Metropole(CityGoal):
    def points_for_goal(self, tilemap):

        city_chunks = self.get_chunks(tilemap, "City")

        points = [0]
        for chunk in city_chunks:
            neighbours = self.get_neighbours_of_chunk(tilemap, chunk, "City")
            if "Mountain" not in [x.name for x in neighbours]:
                points.append(len(chunk))

        return max(points)


class Schillernde_Ebene(CityGoal):
    def points_for_goal(self, tilemap):

        points = 0
        city_chunks = self.get_chunks(tilemap, "City")
        for chunk in city_chunks:
            neighbours = self.get_neighbours_of_chunk(tilemap, chunk, "City")
            neighbours_names = [x.name for x in neighbours if x.name not in ["Empty", "Ruins"]]

            if len(set(neighbours_names)) >= 3:
                points += 3

        return points


class Schild_des_Reichs(CityGoal):
    def points_for_goal(self, tilemap):
        city_chunks = self.get_chunks(tilemap, "City")
        lengths = set([len(x) for x in city_chunks])
        lengths.remove(max(lengths))
        return max(lengths) * 2


class WaterPlainsGoal(Goal):

    def points_for_goal(self, tilemap):
        return None


class LandscapeGoal(Goal):

    def points_for_goal(self, tilemap):
        return None


class Gruenflaeche(ForestGoal):

    def points_for_goal(self, tilemap):

        points = 0

        for row in tilemap:
            if "Forest" in [x.name for x in row]:
                points += 1

        rotated = list(list(x) for x in zip(*tilemap[::-1]))
        for row in rotated:
            if "Forest" in [x.name for x in row]:
                points += 1

        return points


class Duesterwald(ForestGoal):

    def points_for_goal(self, tilemap):
        points = 0

        neighbours_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for row_i, base_row in enumerate(tilemap):
            for col_i, base_col in enumerate(base_row):
                if base_col.name == "Forest":

                    forest_neighbours = [tilemap[row_i + x][col_i + y] for
                                         (x, y) in neighbours_list
                                         if
                                         10 >= row_i + x >= 0 and 10 >= col_i + y >= 0]

                    if all(True if x.name not in ["Empty", "Ruins"] else False for x in
                           forest_neighbours):
                        print("Giving FOREST point for ", row_i, col_i)
                        points += 1

        return points


class Schildwald(ForestGoal):
    def points_for_goal(self, tilemap):
        points = 0

        upper = tilemap[0]
        lower = tilemap[-1]
        left_no_corners = [x[0] for x in tilemap[1:-1]]
        right_no_corners = [x[-1] for x in tilemap[1:-1]]

        for line_to_check in [upper, lower, left_no_corners, right_no_corners]:
            for tile in line_to_check:
                if tile.name == "Forest":
                    points += 1

        return points


# TODO refactor this, there is probably a nicer way to use recursion here (2am code this time :>)
# TODO use chunk/neighbour mechanism instead of this horrible code
class Pfad_des_Waldes(ForestGoal):
    def points_for_goal(self, tilemap):

        def get_neighbours_of_type(row_y, col_x, tile_type):
            neighbours_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            neighbours = [(row_y + y, col_x + x) for
                          (y, x) in neighbours_list
                          if
                          10 >= row_y + y >= 0 and 10 >= col_x + x >= 0 and tilemap[row_y + y][
                              col_x + x].name == tile_type]
            return neighbours

        points = 0

        def get_path_from_mountain(row, col):

            already_visited = []

            initial_forest_neighbours = get_neighbours_of_type(row, col, "Forest")

            def recursion(row_r, col_r):
                potential_mountain_neighbours = get_neighbours_of_type(row_r, col_r,
                                                                       "Mountain")

                for pot_mtn in potential_mountain_neighbours:
                    if pot_mtn != (row, col):
                        print("Mountain path found from ", row, col, "to", pot_mtn)
                        return True

                forest_neighbours = get_neighbours_of_type(row_r, col_r, "Forest")
                for n in forest_neighbours:
                    if n in already_visited:
                        forest_neighbours.remove(n)
                already_visited.extend(forest_neighbours)

                if not forest_neighbours:
                    return False

                for n in forest_neighbours:
                    has_path = recursion(n[0], n[1])
                    if has_path:
                        return True

            for pos_path in initial_forest_neighbours:
                return recursion(pos_path[0], pos_path[1])

        for row, base_row in enumerate(tilemap):
            for col, base_col in enumerate(base_row):
                if base_col.name == "Mountain":

                    has_path = get_path_from_mountain(row, col)
                    if has_path:
                        points += 3

        return points
