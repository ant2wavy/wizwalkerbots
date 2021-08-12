import asyncio
import pathlib
from time import time

from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from wizwalker.extensions.scripting.utils import teleport_to_friend_from_list
from utils import decide_heal, go_through_dialog, exit_out, go_to_closest_mob


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

    Total_Count = 0
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
            await asyncio.gather(*[go_to_closest_mob(p)])

        # Yevgeny fight
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            combat_handlers.append(
                SprintyCombat(p, CombatConfigProvider(f'sideboss_configs/{p.title}spellconfig.txt', cast_time=1)))
        print("Starting Yevgeny fight.")
        await asyncio.sleep(0.5)
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])  # Battle
        print("Combat ended")
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

        await p1.goto(15.308456420898438, 2946.2978515621)
        await p1.wait_for_zone_change()
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        for p in clients[1:]:
            await p.goto(15.308456420898438, 2946.2978515621)
            await p.wait_for_zone_change()
            await p.send_key(Keycode.S, 0.1)

        # Moving to make Shane Von Shane appear

        await p1.goto(116.53296661376953, 1298.63916015625)
        await asyncio.sleep(1)
        # Go through dialogue triggered by Shane appearance
        await asyncio.sleep(1)
        await asyncio.gather(*[go_through_dialog(p) for p in clients])
        await asyncio.sleep(1)

        # Moving to second boss fight (Shane von Shane)
        for p in clients:
            await asyncio.gather(*[go_to_closest_mob(p)])

        # Second boss fight (Shane Von Shane):
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            combat_handlers.append(
                SprintyCombat(p, CombatConfigProvider(f'sideboss_configs/{p.title}spellconfig.txt', cast_time=1)))
        print("Starting Shane fight.")
        await asyncio.sleep(0.5)
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers])  # Battle
        print("Combat ended")
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
        await asyncio.gather(*[p.use_potion_if_needed(health_percent=80, mana_percent=10) for p in clients])
        await asyncio.sleep(1)

        # Engaging mali fight
        for p in clients:
            await asyncio.gather(*[go_to_closest_mob(p)])

        # Final boss fight (Malistaire)
        print("Preparing combat configs")
        combat_handlers = []
        for p in clients:  # Setting up the parsed configs to combat_handlers
            combat_handlers.append(
                SprintyCombat(p, CombatConfigProvider(f'mainboss_configs/{p.title}spellconfig.txt', cast_time=1)))
        print("Starting Malistaire fight.")
        await asyncio.sleep(0.5)
        await asyncio.gather(*[h.wait_for_combat() for h in combat_handlers]) # Battle
        print("Combat ended")
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

        # Return to p1 to sigil
        await asyncio.gather(*[exit_out(p1)])
        await asyncio.sleep(1)

        # p2-p4 port to p1 after conclusion of run (fish icon)
        for p in clients[1:]:
            await p.send_key(Keycode.F, 0.1)
            await teleport_to_friend_from_list(client=p, icon_list=2, icon_index=0, name=None)
            await p.wait_for_zone_change()
            await asyncio.sleep(1)
            await p.send_key(Keycode.PAGE_DOWN, 0.1)

        await asyncio.sleep(2)

        # Healing

        await p1.use_potion_if_needed(health_percent=70, mana_percent=33)

        for p in clients[1:]:
            await p.use_potion_if_needed(health_percent=70, mana_percent=10)
            await asyncio.sleep(0.2)

        await asyncio.sleep(3.5)
        await p1.send_key(Keycode.PAGE_DOWN, 0.1)
        await asyncio.sleep(1)

        # Time
        Total_Count += 1
        print("The Total Amount of Runs: ", Total_Count)
        print("Time Taken for run: ", round((time() - start) / 60, 2), "minutes")
        print("Total time elapsed: ", round((time() - total) / 60, 2), "minutes")
        print("Average time per run: ", round(((time() - total) / 60) / Total_Count, 2), "minutes")
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