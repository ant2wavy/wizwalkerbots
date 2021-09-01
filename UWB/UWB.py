import asyncio
import os
from time import time

from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from utils import decide_heal


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
        await p.use_potion_if_needed(health_percent=35, mana_percent=5)

    # Storing safe location
    safe_location = await p1.body.position()

    Total_Count = 0
    total = time()
    while True:
        start = time()

        # Determine heals for p1-p4
        await asyncio.gather(*[decide_heal(p) for p in clients])
        print()

        # Battle starter
        await p1.tp_to_closest_mob()
        await p1.send_key(Keycode.W, 0.1)
        await asyncio.sleep(1)
        p1pos = await p1.body.position()
        # p2-p4 sent into duel circle
        for p in clients[1:]:
            await p.teleport(p1pos)
            await p.send_key(Keycode.W, 0.1)

        # Battle 2.0:
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

        # Returning to safe spot
        for p in clients:
            await p.teleport(safe_location)
            await asyncio.sleep(0.1)

        # Healing
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=35, mana_percent=5) for p in
                               clients])  # WizSprinter function now, not WizSDK
        await asyncio.sleep(5)

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
