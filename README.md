# wizwalkerbots
Simple repo to house my WizWalker bots. Everything you need to know is in the README. Please do not try to dm me.
Don't make messages in #support about my bots until you read the entire README. It's called README for a reason. If you cannot read, I'm sure I can find someone to read it to you.

Note: you need a house with a world gate behind you equipped
Running from releases

    Download from here
    Extract the zip
    Set your configs using the guide below
    Double click the exe in the desired location you want to run the script

Running from source

Run pip install -r requirements.txt to install required libraries
To run from source do py -m {name of bot} in the main github folder

Most people should run from releases. Just extract the zip, set your configs, and run the exe.
Spell Config guide

Firstly, this is the setup,{#} spell[enchant] @ target | spell[enchant] @ target | etc.

Quick note: configs will loop indefinitely which means you can have one lined configs like: lord[epic] | tempest[epic] to constantly loop storm lord and tempest indefinitely

Spells and enchants go off of the names of what the spells are in the files, you will have to run a separate script to print your cards out for you and then you can use them (You can also just guess). For example, thunder snake enchanted with epic cast at a boss can be called likethunder[epic] @ boss names don't need to be exact, as long as the word itself is contained within the actual spell.

If you do not have an enchant you want to put on the spell, leave enchant blank without brackets, i.e. thunder @ boss

This list of things you can target goes as follows:
self
enemy(#) *# = numbers 0-3 relative to turn order
ally(#) *same with enemy but it's 0-2 because self
boss
aoe *if you have an aoe, you can leave targeting blank i.e. tempest[epic] or for no enchant tempest
{name of enemy or ally}

Priority spell casting. Each line is split up by pipes. And after each pipe is another spell. This is the order of spells the script will check before giving up and passing. You can have an infinite amount of priority spells, and you don't need to use priority spells at all. Here's an example of a line using priority spell casting: lord[epic] | tempest[epic] | feint[potent] @ boss

Specific round casting. If you see back to the original format of the new spell config, you can see the {#}. This is used for casting only on specific rounds, no matter how many times the config loops. The # presents the round number the spell is cast on. Say you want to cast a potent feint on round 1 only, and then loop storm lord and tempest, {1} feint[potent] @ boss lord[epic] | tempest[epic]

Now, any<...>. The any template can be used to say that you want to cast any of a type of spell effect. i.e. any<damage> @ enemy or any<damage & aoe>[any<enchant>]. All the different kinds of specifiers you can use are damage, aoe, heal, heal self, heal other, blade, shield, trap, enchant
Example configs

An example config that will just spam cast any aoe no matter the school:
any<damage & aoe>[any<enchant>] | any<damage & aoe>
Or, if you want to feint the boss and blade, and then spam aoe:
{1} feint[potent] @ boss | any<blade> @ self
{2} feint[potent] @ boss | any<blade> @ self
any<damage & aoe>[any<enchant>] | any<damage & aoe>
