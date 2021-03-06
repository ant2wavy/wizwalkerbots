import asyncio
import os
import threading

import PySimpleGUI as ARB

from time import time

from pymem.exception import WinAPIError, MemoryReadError
from wizwalker import XYZ, MemoryReadError
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from wizwalker.extensions.scripting.utils import teleport_to_friend_from_list
from utils import decide_heal, go_through_dialog


async def abandoned_house(sprinter):
    """ Uses WizWalker API (cred StarrFox) and WizSprinter (cred SirOlaf) \n
        Registers clients with WizSprinter \n
        Handles walking, dialogue, potions, fighting while continuously looping the Abandoned House Dungeon"""

    # Register clients
    sprinter.get_new_clients()

    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients:
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()
        await p.send_key(Keycode.PAGE_DOWN, 0.1)

    print()
    total_count = 0
    total = time()
    while True:

        # Buy potions if needed
        await asyncio.gather(*[decide_heal(p) for p in clients])

        # Entering Dungeon
        for p in clients:
            while await p.is_in_npc_range():
                print(f"[{p.title}] is now entering the instance.")
                await asyncio.sleep(0.4)
                await p.send_key(Keycode.X, 0.1)
        await asyncio.gather(*[p.wait_for_zone_change() for p in clients])
        await asyncio.sleep(1.4)
        print()

        start = time()

        # first dialogue
        await asyncio.gather(*[p.send_key(Keycode.W, 3) for p in clients])
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        # initiate first combat
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.1)

        # First mob fight:
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/house_configs/mob_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # second dialogue
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.1)
        await asyncio.gather(*[p.goto(-18.830564498901367, -2207.352783203125) for p in clients])
        await asyncio.sleep(0.1)
        await asyncio.gather(*[p.goto(16.070451736450195, -1462.8040771484375) for p in clients])
        await asyncio.sleep(0.1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.1)
        near_second_mob = XYZ(x=-1433.9608154296875, y=238.08489990234375, z=0.399993896484375)
        for p in clients:
            await p.teleport(near_second_mob)
            await asyncio.sleep(0.1)

        # initiating second combat
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.1)

        # second mob fight:
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/house_configs/mob_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # Dialogue after second fight
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1.5)

        # Talking to Belgrim

        await p1.goto(-893.4644775390625, 745.897216796875)
        await asyncio.sleep(1)
        await p1.send_key(Keycode.X, 0.1)
        await asyncio.sleep(1)
        await go_through_dialog(p1)
        await asyncio.sleep(1)

        # Moving to boss fight
        await p1.goto(-4.737403869628906, 1129.42529296875)  # walks to detritus door
        await p1.wait_for_zone_change()
        await p1.send_key(Keycode.W, 0.6)  # walks to trigger dialogue
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        for p in clients[1:]:
            await p.goto(-4.737403869628906, 1129.42529296875)
            await p.wait_for_zone_change()
            await p.send_key(Keycode.W, 0.2)

        # Initiating boss fight
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.1)

        # Boss fight:
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/house_configs/boss_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # Return to sigil

        await asyncio.sleep(1)
        await p1.send_key(Keycode.PAGE_UP, 0.1)
        await p1.wait_for_zone_change()

        for p in clients[1:]:
            await p.send_key(Keycode.F, 0.1)
            await asyncio.sleep(0.5)
            await teleport_to_friend_from_list(client=p, icon_list=2, icon_index=0, name=None)
            await p.wait_for_zone_change()
            await asyncio.sleep(1)

        # Checking for healing
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=25) for p in clients])
        await asyncio.sleep(1)
        await p1.send_key(Keycode.PAGE_DOWN, 0.1)

        # Time
        total_count += 1
        print("The Total Amount of Runs: ", total_count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / total_count, 2), "minutes")
        print()


async def viggor(sprinter):
    """ Uses WizWalker API (cred StarrFox) and WizSprinter (cred SirOlaf) \n
        Registers clients with WizSprinter \n
        Handles walking, dialogue, potions, fighting while continuously looping the Viggor Dungeon"""
    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients:
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()
        await p.send_key(Keycode.PAGE_DOWN, 0.1)

    print()
    total_count = 0
    total = time()
    while True:

        # Buy potions if needed
        await asyncio.gather(*[decide_heal(p) for p in clients])
        await asyncio.sleep(2)

        start = time()

        # Entering Dungeon
        print()
        for p in clients:
            while await p.is_in_npc_range():
                print(f"[{p.title}] is now entering the instance.")
                await asyncio.sleep(0.4)
                await p.send_key(Keycode.X, 0.1)
        await asyncio.gather(*[p.wait_for_zone_change() for p in clients])
        await asyncio.sleep(1.4)
        print()

        # get within mob range / clear dialogue
        await asyncio.gather(*[p.send_key(Keycode.W, 3) for p in clients])
        await asyncio.sleep(0.5)
        await asyncio.gather(*[p.send_key(Keycode.W, 15) for p in clients])
        await asyncio.sleep(0.5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.gather(*[p.send_key(Keycode.W, 1) for p in clients])
        await asyncio.sleep(0.5)

        # initiate fight
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.2)
            await asyncio.sleep(0.1)

        # mob fight
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/viggor_configs/mob_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # getting to viggor / dialogue
        search_for_viggor = await p1.quest_position.position()
        await asyncio.gather(*[p.teleport(search_for_viggor) for p in clients])
        await asyncio.sleep(2)
        find_viggor = await p1.quest_position.position()
        await asyncio.gather(*[p.teleport(find_viggor) for p in clients])
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        # initiating combat with prince viggor
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.1)

        # viggor fight
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/viggor_configs/boss_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # resetting

        await asyncio.sleep(1)
        await p1.send_key(Keycode.PAGE_UP, 0.1)
        await p1.wait_for_zone_change()

        for p in clients[1:]:
            await p.send_key(Keycode.F, 0.1)
            await asyncio.sleep(0.5)
            await teleport_to_friend_from_list(client=p, icon_list=2, icon_index=0, name=None)
            await p.wait_for_zone_change()
            await asyncio.sleep(1)

        # Checking for healing
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=25) for p in clients])
        await asyncio.sleep(1)
        await p1.send_key(Keycode.PAGE_DOWN, 0.1)

        # Time
        total_count += 1
        print("The Total Amount of Runs: ", total_count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / total_count, 2), "minutes")
        print()


async def sepulcher(sprinter):
    """ Uses WizWalker API (cred StarrFox) and WizSprinter (cred SirOlaf) \n
        Registers clients with WizSprinter \n
        Handles walking, dialogue, potions, fighting while continuously looping the Viggor Dungeon"""

    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients:
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()
        await p.send_key(Keycode.PAGE_DOWN, 0.1)

    print()
    total_count = 0
    total = time()
    while True:

        # Buy potions if needed
        await asyncio.gather(*[decide_heal(p) for p in clients])

        start = time()

        # Entering Dungeon
        print()
        for p in clients:
            while await p.is_in_npc_range():
                print(f"[{p.title}] is now entering the instance.")
                await asyncio.sleep(0.4)
                await p.send_key(Keycode.X, 0.1)
        await asyncio.gather(*[p.wait_for_zone_change() for p in clients])
        await asyncio.sleep(1.4)
        print()

        # dialogue 1
        dialogue_1 = await p1.quest_position.position()
        await asyncio.gather(*[p.teleport(dialogue_1) for p in clients])
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.2)
        await asyncio.gather(*[p.send_key(Keycode.W, 0.75) for p in clients])

        # initiating combat
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(1)

        # first mob
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/sepulcher_configs/mob_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # dialogue 2
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.2)

        # unghosting
        for p in clients:
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(1)

        dialogue_2 = await p1.quest_position.position()
        await asyncio.gather(*[p.teleport(dialogue_2) for p in clients])
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.2)

        # initiating combat
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(1)

        # second mob
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/sepulcher_configs/mob_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # unghosting
        for p in clients:
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(1)

        # third fight
        dialogue_3 = await p1.quest_position.position()
        await asyncio.gather(*[p.teleport(dialogue_3) for p in clients])
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.2)

        # initiating combat
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.2)
            await asyncio.sleep(1)

        # viggor's drake fight
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/sepulcher_configs/boss_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # Resetting
        await p1.send_key(Keycode.PAGE_UP, 0.1)
        await p1.wait_for_zone_change()

        for p in clients[1:]:
            await p.send_key(Keycode.F, 0.1)
            await asyncio.sleep(0.5)
            await teleport_to_friend_from_list(client=p, icon_list=2, icon_index=0, name=None)
            await p.wait_for_zone_change()
            await asyncio.sleep(1)

        # Checking for healing
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=25) for p in clients])
        await asyncio.sleep(1)
        await p1.send_key(Keycode.PAGE_DOWN, 0.1)


async def main():

    # setting up GUI

    ARB.theme('DarkAmber')  # Add a touch of color
    keys = ['House', 'Viggor', 'Sepulcher']

    # All the stuff inside your window.
    col_1 = [[ARB.Text('ARB', font=('Arial', 20))]]
    col_2 = [[ARB.Text('Copyright 2021, Author: ant2wavy', font=('Arial', 14))]]
    col_3 = [[ARB.Radio('Abandoned House', "R1", key=keys[0]),
              ARB.Radio('Viggor', "R1", key=keys[1]),
              ARB.Radio('Sepulcher', "R1", key=keys[2])]]
    col_4 = [[ARB.Button("Start"),
              ARB.Button("Stop")]]

    layout = [[ARB.Frame(layout=col_1, title='')],
              [ARB.Frame(layout=col_2, title='')],
              [ARB.Frame(layout=col_3, title='')],
              [ARB.Frame(layout=col_4, title='')],
              [ARB.Output(size=(60, 20))]]

    # Create the Window
    window = ARB.Window('Alchemical Reagent Bot', layout, resizable=True, element_justification='center',
                        enable_close_attempted_event=True)
    sprinter = WizSprinter()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == "Start":
            user_selection = str([key for key in keys if values[key]][0])
            print("You selected: " + user_selection)
            print()
            if user_selection == "House":
                _thread = threading.Thread(target=asyncio.run, args=(abandoned_house(sprinter),))
                _thread.start()
            elif user_selection == "Viggor":
                _thread = threading.Thread(target=asyncio.run, args=(viggor(sprinter),))
                _thread.start()
            elif user_selection == "Sepulcher":
                _thread = threading.Thread(target=asyncio.run, args=(sepulcher(sprinter),))
                _thread.start()
        elif event == "Stop":
            print("Killing ARB. Please close the exe before using wiz clients.")
            await sprinter.close()
            raise KeyboardInterrupt
        elif event == ARB.WINDOW_CLOSE_ATTEMPTED_EVENT and ARB.popup_yes_no('Do you really want to exit?') == 'Yes':
            await sprinter.close()
            break


async def run():
    try:
        await main()
    except:
        import traceback
        traceback.print_exc()

# Start
if __name__ == "__main__":
    asyncio.run(run())
