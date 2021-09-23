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
        await p.use_potion_if_needed(health_percent=40, mana_percent=5)

    # initialize tp coords
    top_ramp_jade_oni = XYZ(x=-4506.56884765625, y=-38.63823699951172, z=767.7666015625)

    # Initialize time and count variables
    Total_Count = 0
    total = time()
    while True:
        start = time()

        # Determine if p1-p4 needs heals
        await asyncio.gather(*[decide_heal(p) for p in clients])

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

        # Check zone of p1
        zone = await p1.zone_name()
        if zone == "MooShu/Interiors/MS_Emperor_Palace":
            while not await p1.is_in_npc_range():
                await p1.send_key(Keycode.W, 0.1)
            await p1.send_key(Keycode.X, 0.1)
            await asyncio.gather(*[go_through_dialog(p1)])
            for p in clients:
                await p.teleport(top_ramp_jade_oni)  # top ramp coords
                await asyncio.sleep(1)
            for p in clients:
                await p.tp_to_closest_mob()
                await asyncio.sleep(1)
        elif zone == "Khrysalis/Interiors/KR_Z12_I04_MorgantheBossRoom":
            for p in clients:
                if await p.is_in_dialog():
                    await asyncio.gather(*[go_through_dialog(p)])
                else:
                    pass
            await asyncio.sleep(2)
            for p in clients:
                await p.tp_to_closest_mob()
                await asyncio.sleep(1)
        else:
            for p in clients:
                await p.tp_to_closest_mob()
                await asyncio.sleep(1)

        # Battle test 2.0:
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            p_name = f"{p.title}spellconfig.txt"
            abs_file_path = os.path.abspath("configs/" + p_name)
            combat_handlers.append(SprintyCombat(p, CombatConfigProvider(str(abs_file_path), cast_time=0.2)))
        print("Starting combat")
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])
        print("Combat ended")
        await asyncio.sleep(1.5)
        print()

        # Resetting
        # saving new quest pos
        if zone == "Khrysalis/Interiors/KR_Z12_I04_MorgantheBossRoom":
            await asyncio.gather(*[go_through_dialog(p) for p in clients])
            await asyncio.sleep(7)
            await asyncio.gather(*[go_through_dialog(p) for p in clients])
            await asyncio.gather(*[go_through_dialog(p) for p in clients])
            await asyncio.sleep(10)
            await asyncio.gather(*[go_through_dialog(p) for p in clients])
            await asyncio.sleep(3)
            # changing quest
            await p1.send_key(Keycode.Q, 0.1)
            await p1.mouse_handler.click_window_with_name("wndQuestInfo2")
            await asyncio.sleep(1)
            await p1.send_key(Keycode.Q, 0.1)
            exit_location = await p1.quest_position.position()
            for p in clients:
                await p.goto(exit_location.x, exit_location.y)
                await p.wait_for_zone_change()
                await asyncio.sleep(0.5)
                await p.send_key(Keycode.S, 0.5)
        else:
            # changing quest
            await p1.send_key(Keycode.Q, 0.1)
            await p1.mouse_handler.click_window_with_name("wndQuestInfo2")
            await asyncio.sleep(1)
            await p1.send_key(Keycode.Q, 0.1)
            exit_location = await p1.quest_position.position()
            await asyncio.gather(*[p.goto(exit_location.x, exit_location.y) for p in clients])
            await asyncio.gather(*[p.wait_for_zone_change() for p in clients])
            await asyncio.sleep(0.5)
            await asyncio.gather(*[p.send_key(Keycode.S, 0.5) for p in clients])

        # Healing
        for p in clients:
            if await p.needs_potion(health_percent=40, mana_percent=5):
                print(f"[{p.title}] Needs potion, attempting to use")
                await p.use_potion_if_needed(health_percent=40, mana_percent=5)
        await asyncio.sleep(0.2)

        # Time
        Total_Count += 1
        print("The Total Amount of Runs: ", Total_Count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")


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
