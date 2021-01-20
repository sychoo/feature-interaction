# Simon Chu
# Mon Jan 18 12:29:10 EST 2021
# demo showing ego drone flying checkpoint mission

# condition:
# 20 x 20 map
# ego drone checkpoints (0, 10) <init> --> (10, 20) --> (20, 0)
# chaser drone (0, 0) <init>

from src.obj.map import Coord
from src.mission.checkpoint import Checkpoint_Mission


def main():
    ################################
    # configure mission parameters #
    ################################

    map_width: int = 20
    map_height: int = 20

    ego_init_loc: Coord = Coord(1, 10)
    chaser_init_loc: Coord = Coord(1, 1)

    checkpoints: list[Coord] = [Coord(10, 19), Coord(19, 1)]

    ####################
    # initiate mission #
    ####################

    cm = Checkpoint_Mission(map_width=map_width,
                            map_height=map_height,
                            ego_init_loc=ego_init_loc,
                            chaser_init_loc=chaser_init_loc,
                            checkpoints=checkpoints)

    cm.start()


if __name__ == "__main__":
    main()
