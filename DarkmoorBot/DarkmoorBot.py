import asyncio
import os
from time import time

from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from utils import decide_heal, go_through_dialog


async def main(sprinter):

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
        await asyncio.sleep(0.5)

    print()

    total_count = 0
    total = time()
    while True:

        # Buy potions if needed
        await asyncio.gather(*[decide_heal(p) for p in clients])

        start = time()

        # Entering Dungeon
        await asyncio.gather(*[p.send_key(Keycode.X, 0.1) for p in clients])
        await asyncio.sleep(11)
        await asyncio.gather(*[p.wait_for_zone_change() for p in clients])

        # Going through first section of dialogue
        await asyncio.sleep(1)
        await p1.send_key(Keycode.W, 3)
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        # Moving to first boss fight (Yevgeny)
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.1)

        # Yevgeny fight
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("sideboss_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat with Yevgeny")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # Go through second section of dialogue after Yevgeny
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        # Unghosting
        for p in clients[1:]:
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.2)

        # Moving through door to Shane Von Shane

        shane_door = XYZ(-57.675254821777344, 3008.5703125, 0.51971435546875)
        await p1.teleport(shane_door)
        await p1.send_key(Keycode.W, 0.1)
        await p1.wait_for_zone_change()
        await asyncio.sleep(1)

        # clear dialogue after p1 walks through door
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(0.1)

        # p2-p4 ports through door
        for p in clients[1:]:
            await p.teleport(shane_door)
            await p.send_key(Keycode.W, 0.1)
            await p.wait_for_zone_change()
            await asyncio.sleep(1)

        # Moving to make Shane Von Shane appear
        await asyncio.gather(*[p.goto(116.53296661376953, 1298.63916015625) for p in clients])
        # Go through dialogue triggered by Shane appearance
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        # Moving to second boss fight (Shane von Shane)
        for p in clients:
            await p.tp_to_closest_mob()
            await asyncio.sleep(1)

        # Second boss fight (Shane Von Shane):
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("sideboss_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat with Shane von Shane")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1.5)

        # Moving to Mali fight room

        await p1.goto(4.960016250610352, 2900.962158203125)
        await p1.wait_for_zone_change()
        await p1.send_key(Keycode.W, 2)
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        for p in clients[1:]:
            await p.goto(-467.0201416015625, 369.74102783203125)
            await p.goto(4.960016250610352, 2900.962158203125)
            await p.wait_for_zone_change()
            await asyncio.sleep(1)

        # Moving to Bone Dragon Animation
        await p1.goto(116.53296661376953, 1298.63916015625)
        await asyncio.sleep(20)
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=10) for p in clients])
        await asyncio.sleep(1)

        # Engaging mali fight
        for p in clients:
            await p.tp_to_closest_mob()
            await p.send_key(Keycode.W, 0.1)
            await asyncio.sleep(0.1)

        # Mali fight
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("mainboss_configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat with Malistaire")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # Clear mali dialogue (post-fight)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(5)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(60)
        print("Returning to sigil.")
        print()

        # resetting
        # port to gateway orb
        gateway_orb = XYZ(-22.866426467895508, -2142.700439453125, 0.0)
        for p in clients:
            await p.teleport(gateway_orb)
            await asyncio.sleep(3)
            await p.send_key(Keycode.X, 0.1)
            await p.wait_for_zone_change()
            await asyncio.sleep(0.5)
            await p.send_key(Keycode.W, 1.25)

        # Healing

        await p1.use_potion_if_needed(health_percent=70, mana_percent=33)

        for p in clients[1:]:
            await p.use_potion_if_needed(health_percent=70, mana_percent=10)
            await asyncio.sleep(0.2)

        await asyncio.sleep(3.5)

        # Time
        total_count += 1
        print("The Total Amount of Runs: ", total_count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / total_count, 2), "minutes")
        print()


# Error Handling
async def run():
    sprinter = WizSprinter()

    try:
        await main(sprinter)
    except:
        import traceback

        traceback.print_exc()

    await sprinter.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())
