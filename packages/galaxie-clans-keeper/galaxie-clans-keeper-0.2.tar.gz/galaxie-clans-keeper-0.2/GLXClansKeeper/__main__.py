#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Clans Keeper Team, all rights reserved

import argparse
import GLXClansKeeper

__authors__ = ["Mo", "Tuxa"]
__date__ = 20200915
__version__ = "0.1"
__description__ = "Galaxie Clans Keeper"


def keeper():
    keeper_obj = GLXClansKeeper.Keeper()
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by Galaxie under GPLv3+ license"
    )
    parser.add_argument('--lang',
                        dest='lang',
                        default='en',
                        help="HTTP_ACCEPT_LANGUAGE"
                        )

    parser.add_argument('--charset',
                        dest='charset',
                        default='utf-8',
                        help="character sets"
                        )

    args = parser.parse_args()
    keeper_obj.lang = args.lang
    keeper_obj.charset = args.charset

    #print(args)
    keeper_obj.run()
