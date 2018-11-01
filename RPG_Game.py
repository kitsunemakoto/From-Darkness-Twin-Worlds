# Written by Kitsune ως ατομικο project

import random
from pygame import mixer
from threading import Thread
from configparser import ConfigParser
from io import BytesIO
import pymysql
import ftplib
import paramiko
import time
import datetime
import pickle
import os
import keyboard

playerHealth = 100
enemyHealth = 100
bossBattle = 0
startingArmorSet = 0
startingWeapon = 0
currentEnemyName = ""
enemy_isAlert = 0
e_weaponPower = 0
equipWeapon_select = ""
equipArmor_select = ""
weather = ""
area = ""
areaChanged = 0
hasRegistered = 0

INVENTORY_dict = {'Sapphire Gem': 0, 'Enhancement Stone': 0, 'Chemicals': 0, 'Shattered Blade': 0, 'Feather': 0,
                  'Steel': 0, 'Leather Piece': 0, 'Upper-Left Map Piece': 0, 'Upper-Right Map Piece': 0,
                  'Lower-Left Map Piece': 0, 'Lower-Right Map Piece': 0, 'Broken Helmet': 0, 'Mana Stone Piece': 0,
                  'Piece of Forbidden Page': 0}
ACHIEVEMENTS_dict = {'A1': 0, 'A2': 0, 'A3': 0, 'A4': 0, 'A5': 0, 'A6': 0, 'A7': 0, 'A8': 0, 'A9': 0, 'A10': 0,
                     'A11': 0, 'AchievementsCompleted': 0}
CONT2_dict = {'ULMapPiece': 0, 'URMapPiece': 0, 'LLMapPiece': 0, 'LRMapPiece': 0, 'MasgraMap': 0, 'TravelledCONT2': 0,
              'AtMasgra': 0}
SET_dict = {'WeaponName': "", 'ArmorName': "", 'WeaponLevel': 0, 'ArmorLevel': 0}
QUESTS_dict = {'active1': 0, 'killed10BN': 0, 'active2': 0, 'killed5WN': 0, 'active3': 0, 'collected6ZHeads': 0,
               'active4': 0, 'collected4PandaF': 0, 'active5': 0, 'killHarbringer': 0, 'side_active1': 0, '': 0,
               'side_active2': 0, '': 0}
SKILLS_dict = {'dChargePower': 0, 'sBashPower': 0, 'dSlashPower': 0, 'sHellPower': 0, 'bDaggerPower': 0,
               'sFangsPower': 0, 'oRollPower': 0, 'hArrowsPower': 0, 'fArrowsPower': 0, 'sPhoenixPower': 0,
               'aPentagramPower': 0, 'cElementsPower': 0, 'hLightPower': 0, 'lHammerPower': 0}
SAVE_dict = {'YourLevel': 0, 'YourHealth': 0, 'YourMana': 0, 'YourGold': 0, 'YourWeaponPower': 0, 'YourArmor': 0,
             'TotalWeight': 0, 'temp_visitedTown': 0, 'temp_weaponPower': 0, 'temp_armor': 0, 'HasHorse':0, 'Mail': 0, 'TimesDied': 0,
             'CurrentWeight': 0, 'TotalGoldAcquired': 0, 'times_VisitedTown': 0, 'GOLDEN_DIAMONDS': 0,
             'EnemiesKilled': 0, 'Parry': 0, 'Block': 0, 'ShieldEquipped': 0, 'CriticalRate': 1, 'YourExp': 0,
             'YourClass': "", 'YourName': "", 'InTown': 0, 'CurrentTownName': ""}
town_names = ["Margonia", "Vaalthorn", "Blezskor", "Trahj", "Dorryu", "Asval", "Okremar", "Snakehead Valley"]
npc_names = ["1. Sullivan the Mage", "2. Bryan the Blacksmith", "3. Wally the Potionmaker", "4. Kyle the Armorsmith",
             "5. Bob the Craftsman", "6. Colin the Captain (Story Quests)", "7. Helena the Captain's Daughter",
             "8. Takashi the Fisherman (Side Quests)", "9. Ken the Musician (SAVE GAME)",
             "10. Matthew the Boatskeeper (250 Gold fee)", "11. View Stats (Consumes 1 SAFE Turn)",
             "0. Skip 1 SAFE Turn"]
enemy_names = ["Avory", "Aaron", "Maltharok", "Biyok", "Gaerin", "Po-Po", "Jeggerin", "Nilthus", "Khazim",
               "Black Ninja", "White Ninja", "Thug", "Muul'Tir", "Zombie Astronaut", "Cursed Po-Po", "Lava Walker",
               "Snow Walker", "Subject #249", "Subject #506", "Subject #114", "Rampant Mercenary", "Xepharim"]
quest_enemyNames = ["Black Ninja", "White Ninja"]
enemy_attacks = ["Spinning Blades", "Brute Force", "Willow Chop", "Blossom Cannon", "Tiger Crush", "Hurricane Assault",
                 "Swift Kick", "Stomp", "Dark Strike"]
enemy_playerDied = ["Scumbags like you should only deserve death, prick.", "Bah, I knew you were nothing special.",
                    "And here I thought you were someone challenging. Figures.",
                    "At the wrong place at the wrong time.", "Not so tough now, huh deadman?",
                    "Dead? Already? You're no fun.."]

lootItems = ["Sapphire Gem", "Enhancement Stone", "Chemicals", "Shattered Blade", "Feather", "Steel", "Leather Piece",
             "Upper-Left Map Piece", "Upper-Right Map Piece", "Lower-Left Map Piece", "Lower-Right Map Piece",
             "Broken Helmet", "Mana Stone Piece", "Piece of Forbidden Page"]

lootWeapons_Warrior = ["Rusty Swiftblade", "Reforged Sword", "Storm Slicer", "Tooth and Claw", "Mayhem and Madness",
                       "Pain and Devastation", "Corroded Longsword and Cold-Forged Steel Guardian",
                       "Crystal Sword and Oathkeeper", "Steel Dualblade of Vindication",
                       "Worldbreaker and Thunder-Forged Shield", "Moonlit Claymore", "Star-Ascended Katana",
                       "Roaring Scimitar", "Feral Axe"]
lootArmor_Warrior = ["Twisted Vest of Ominous Wars", "Lightning Vest of the Night Sky", "Phantom Silver Cuirass",
                     "Banished Ebon Chestplate", "Battleplate of Burning Torment", "Demon Vest of Conquered Fire",
                     "Silver Chestplate of Twisted Worlds", "Hateful Demon Chestplate", "Mail Armor",
                     "Armor of Defiance", "Vest of Fallen Power", "Greatplate of Infernal Punishment",
                     "Defender of Traitors", "Cuirass of Holy Sorrow"]

lootWeapons_Rogue = ["Dragonfang", "Venom Shanker", "Stormguard Ebonsteel Reaver", "Dirk of Execution",
                     "Mercenary Ebony Knife", "Hateful Reaver", "Phantom Shortblade", "Possessed Stiletto", "Blackfang",
                     "Bloodsurge Piercer", "Desolation Kris", "Sinister Dagger", "Hatred's Bite", "Banished Slicer"]
lootArmor_Rogue = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]

lootWeapons_Archer = ["Redwood Crossbow", "Hardwood Repeater", "Iron Vulture", "Reincarnated Steel Striker",
                      "Striker's Mark", "Thunder's Talonstrike", "Dark Warbow", "Ironbark Composite Bow", "Arrowsong",
                      "Curved Driftwood Piercer", "Starstruck Crossbow", "Iron Striker", "Frenzied Warbow",
                      "Wicked Warpwood Chord"]
lootArmor_Archer = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]

lootWeapons_Mage = ["Nightmare Warden Staff", "Polished Grand Staff", "Cold-Forged Scepter",
                    "Prideful Devilwood Spiritstaff", "Thundersoul Willow Cane", "Glinting Energy Staff",
                    "Vicious Spiritstaff", "Steel Dragonwrath", "Dreambender's Staff", "Knight's Fall",
                    "Cataclysmic Nightstaff", "Shadow Spiritstaff", "Necromancer's Spire", "Thunderstorm Greatstaff"]
lootArmor_Mage = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]

enemyboss_name = ["Harbringer of Deadly Light", "Guardian of Wind and Thunder"]

harbringer_startquotes = ["I have come to end you.", "You will not dwell in this realm any longer.",
                          "The Underworld awaits and its hungry for your miserable soul."]
harbringer_attacks = ["Scythe Swipe", "Control: Blood", "Death Sentence", "Force of a Thousand Souls",
                      "Lightbreak Slash", "Trail of Death"]
harbringer_phase2_attacks = ["Soul Pain", "Deadly Light", "Lifeforce Crush", "Death"]
harbringer_phase2_deathAttack = ["NOW DIE, MORTAL!", "TIME TO DIE!", "FALL IN TO THE ETERNAL SLEEP!", "SWEET DREAMS!"]
harbringer_phase2_deadlylightAttack = ["WITNESS MY SCYTHE'S TRUE POWER!", "A BLIND SOUL IS A USELESS SOUL!",
                                       "This is how I acquired my title..", "HEAVENS WILL TREMBLE!"]
harbringer_phase2_lifeforcecrushAttack = ["Such a pity of a soul, of a LIFE!", "YOUR LIFE SHALL BE ENDED!",
                                          "Live THIS to the fullest!", "YOUR LIFE WILL COME TO ITS END!"]
harbringer_phase2_soulpainAttack = ["I WILL BRING YOU ON YOUR KNEES, BEGGING FOR MERCY!", "FEEL THE PAIN OF THE DEAD!",
                                    "FEEL TRUE PAIN!", "TREMBLE FOR YOUR LIFE, MORTAL!"]
harbringerS_quotes = ["Hm.. I would laugh at that cheap technique of yours, but even my laugh is worth more than this.",
                      "Oh no, I lost him.. too bad my Scythe finds souls.",
                      "Oh these mortals.. they never learn, right Scythe?"]
harbringer_playerDied_quotes_phase1 = ["Hmph.. you only wasted my time.",
                                       "Such mortal had such strength? Pity. You still died, haha!",
                                       "I AM DEATH INCARNATE, but hm.. did you have a deathwish? What were you thinking?",
                                       "Now.. let the darkness consume your miserable soul!"]
harbringer_death1_quotes = [
    "NOOO! How can I lose.. HOW CAN I LOSE TO A MORTAL?! I'M A GOD, I'M DEATH INCARNATE! I WILL NOT ACCEPT THIS!",
    "My Scythe.. WILL NOT LOSE!", "Did you think you can kill Death itself? Hah, these are barely a few scratches.",
    "No.. no! NO ONE WILL DEFEAT ME! I WILL CONSUME YOUR SOUL EVEN IF IT KILLS ME IN THE PROCESS"]
harbringer_death2_quotes = ["I.. must return to.. Underworld..",
                            "I feel.. pain.. I'll find you again, I PROMISE YOU THIS! NO ONE ESCAPES DEATH!",
                            "I refuse.. to die.. to you! You will NEVER escape ME!",
                            "My Scythe... must rest.. I will.. return!"]

guardian_startquotes = ["I'm lightning incarnate, you cannot face ME!",
                        "Knowledge comes as fast as WIND AND THUNDER! Haha!",
                        "I'll try to go in slow-motion, just for you."]
guardian_attacks = ["Lightning Punches", "Mocking Storm", "Ghostly Strike", "Rain", "Concentrate: Wind", "Thunderstorm"]

class_list = [
    "Warrior - Skills: Devastating Charge (Shield Required), Shield Bash (Shield Required), Decapitating Slash, Thousand Spiritual Swords of Hell.",
    "Rogue - Skills: Stealth (+2 more Skills while active), Bleeding Dagger, Dangerous Game, Shadow Fangs.",
    "(UNFINISHED) Archer - Skills: Offensive Roll, Hail of Arrows, Fire-Enhanced Arrows (+2 more Skills while active), Triple Offensive Roll.",
    "(UNFINISHED) Mage - Skills: Orb of Elements (+1 more Skills while active), Mana Power, Arcane Pentagram, Call of the Elements.",
    "(WILL GET REMOVED LATER) Healer - Skills: Hand of Light, Blessing Shield, Light Hammer, Second Chance."]
warrior_skills = ["1. Devastating Charge (5 Mana, requires shield)", "2. Shield Bash (10 Mana, requires shield)",
                  "3. Decapitating Slash (20 Mana)", "4. Thousand Spiritual Swords of Hell (60 Mana)"]
rogue_skills = ["1. Stealth (10 Mana)", "2. Bleeding Dagger (10 Mana)", "3. Dangerous Game (15 Mana)",
                "4. Shadow Fangs (70 Mana)"]
rogueS_skills = ["1. Backstab (10 Mana)", "2. Swift Assault (25 Mana)"]
archer_skills = ["1. Offensive Roll (5 Mana)", "2. Hail of Arrows (10 Mana)", "3. Fire-Enhanced Arrows (20 Mana)",
                 "4. Triple Offensive Roll (60 Mana)"]
archerF_skills = ["1. Scorched Hail of Arrows (20 Mana)", "2. Summon Phoenix (40 Mana)"]
mage_skills = ["1. Orb of Elements (10 Mana)", "2. Mana Power (100% of your Mana)", "3. Arcane Pentagram (40 Mana)",
               "4. Call of the Elements (70 Mana)"]
healer_skills = ["1. Hand of Light (10 Mana)", "2. Blessing Shield (20 Mana)", "3. Light Hammer (20 Mana)",
                 "4. Second Chance (80 Mana)"]


def ActionLog():
    global SAVE_dict
    global hasRegistered

    ActionLogDate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    if os.path.isfile("./Action Logs/ActionLog.txt"):
        ActionLogText = "./Action Logs/ActionLog.txt"
    else:
        ActionLogDate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ActionLogText = open("./Action Logs/ActionLog.txt", "w")
        ActionLogText.write("[" + ActionLogDate + "]: Action Log has initiated.\n")
        ActionLogText.close()

    ActionLogLevel = SAVE_dict['YourLevel']
    ActionLogDate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    while True:

        ActionLogDate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if ActionLogLevel != SAVE_dict['YourLevel']:
            ActionLogLevel = SAVE_dict['YourLevel']
            ActionLogText = open("./Action Logs/ActionLog.txt", "a")
            ActionLogText.write("[" + ActionLogDate + "]: " + SAVE_dict['YourName'] + " has leveled up to Level " + str(ActionLogLevel) + "\n")
            ActionLogText.close()
        else:
            pass

        if hasRegistered == 1:
            hasRegistered = 0
            ActionLogText = open("./Action Logs/ActionLog.txt", "a")
            ActionLogText.write("[" + ActionLogDate + "]: Character (" + SAVE_dict['YourName'] + ") has been created.\n")
            ActionLogText.close()
        else:
            pass
        time.sleep(2)

def SoundOnKeypress():
    while True:
        while config.get('General', 'sound') == "On":
            if keyboard.is_pressed('enter'):
                    time.sleep(0.1)
                    select = mixer.Channel(0)
                    select.play(mixer.Sound(select_sound))
        else:
            pass

def SideThreads():

    thread1 = Thread(target=ActionLog)
    thread1.start()
    thread2 = Thread(target=blockType_function)
    thread2.start()
    thread3 = Thread(target=SoundOnKeypress)
    thread3.start()


def weightSystem(itemToEquip, itemWeight, itemPower):
    global SAVE_dict
    global SET_dict
    global equipWeapon_select
    global equipArmor_select
    if equipWeapon_select == "Y" or equipWeapon_select == "y":
        if (SAVE_dict['CurrentWeight'] + itemWeight) <= SAVE_dict['TotalWeight']:
            print("You have equipped " + itemToEquip + ".")
            SET_dict['WeaponLevel'] = 0
            SAVE_dict['CurrentWeight'] += itemWeight
            SAVE_dict['YourWeaponPower'] = itemPower
            SET_dict['WeaponName'] = itemToEquip
            time.sleep(1)
            print("Equipment Weight: " + str(SAVE_dict['CurrentWeight']) + "/" + str(SAVE_dict['TotalWeight']) + ".")
            time.sleep(1)
        elif (SAVE_dict['CurrentWeight'] + itemWeight) > SAVE_dict['TotalWeight']:
            print("You cannot equip " + itemToEquip + " because your Current Equipment Weight is " + str(
                SAVE_dict['CurrentWeight']) + " out of " + str(SAVE_dict['TotalWeight']) + ".")
            time.sleep(2)
    elif equipArmor_select == "Y" or equipArmor_select == "y":
        if (SAVE_dict['CurrentWeight'] + itemWeight) <= SAVE_dict['TotalWeight']:
            print("You have equipped " + itemToEquip + ".")
            SET_dict['ArmorLevel'] = 0
            SAVE_dict['CurrentWeight'] += itemWeight
            SAVE_dict['YourWeaponPower'] = itemPower
            SET_dict['ArmorName'] = itemToEquip
            time.sleep(1)
            print("Equpment Weight: " + str(SAVE_dict['CurrentWeight']) + "/" + str(SAVE_dict['TotalWeight']) + ".")
        elif (SAVE_dict['CurrentWeight'] + itemWeight) > SAVE_dict['TotalWeight']:
            print("You cannot equip " + itemToEquip + " because your Current Equipment Weight is " + str(SAVE_dict['CurrentWeight']) + " out of " + str(SAVE_dict['TotalWeight']) + ".")
            time.sleep(2)


def SAVEGAME():
    global SAVE_dict
    global SKILLS_dict
    global QUESTS_dict
    global SET_dict
    print("GAME: Preparing to save game..")
    SAVE_out = open(SAVE_dict['YourName'] + ".dat", "wb")
    SAVE_out.seek(0)
    pickle.dump(SAVE_dict, SAVE_out)
    SAVE_out.close()
    SKILLS_out = open(SAVE_dict['YourName'] + "_Skills.set", "wb")
    SKILLS_out.seek(0)
    pickle.dump(SKILLS_dict, SKILLS_out)
    SKILLS_out.close()
    QUESTS_out = open(SAVE_dict['YourName'] + "_Progress.dat", "wb")
    QUESTS_out.seek(0)
    pickle.dump(QUESTS_dict, QUESTS_out)
    QUESTS_out.close()
    SET_out = open(SAVE_dict['YourName'] + "_Set.set", "wb")
    SET_out.seek(0)
    pickle.dump(SET_dict, SET_out)
    SET_out.close()
    INVENTORY_out = open(SAVE_dict['YourName'] + ".inv", "wb")
    INVENTORY_out.seek(0)
    pickle.dump(INVENTORY_dict, INVENTORY_out)
    INVENTORY_out.close()
    print("GAME: Saved!\n")

    print("Connecting to the FTP server..")
    ftp = ftplib.FTP('xxx', 'xxx', 'xxx')
    print("Connected")
    print("Uploading files..")  # Upload files after save
    filetosend = SAVE_dict['YourName'] + ".dat"
    filetosend2 = SAVE_dict['YourName'] + "_Progress.dat"
    filetosend3 = SAVE_dict['YourName'] + "_Set.set"
    filetosend4 = SAVE_dict['YourName'] + "_Skills.set"
    filetosend5 = SAVE_dict['YourName'] + ".inv"
    file = open(filetosend, 'rb')
    file2 = open(filetosend2, 'rb')
    file3 = open(filetosend3, 'rb')
    file4 = open(filetosend4, 'rb')
    file5 = open(filetosend5, 'rb')
    ftp.cwd("/PROFILES/")
    ftp.storbinary('STOR ' + filetosend, file, 1)
    file.close()
    ftp.storbinary('STOR ' + filetosend2, file2, 1)
    file2.close()
    ftp.storbinary('STOR ' + filetosend3, file3, 1)
    file3.close()
    ftp.storbinary('STOR ' + filetosend4, file4, 1)
    file4.close()
    ftp.storbinary('STOR ' + filetosend5, file5, 1)
    file5.close()
    print("Uploaded")
    ftp.quit()
    print("Disconnected from the FTP server")
    time.sleep(1)


def LOADGAME(USERNAME):
    global SAVE_dict
    global SKILLS_dict
    global QUESTS_dict
    global SET_dict
    print("GAME: Preparing to load profile..")
    SAVE_in = open(USERNAME + ".dat", 'rb')
    SAVE_in.seek(0)
    SAVE_dict = pickle.load(SAVE_in)
    print("GAME: Preparing to load skills..")
    SAVE_skills = open(USERNAME + "_Skills.set", 'rb')
    SAVE_skills.seek(0)
    SKILLS_dict = pickle.load(SAVE_skills)
    print("GAME: Preparing to load progress..")
    SAVE_quests = open(USERNAME + "_Progress.dat", 'rb')
    SAVE_quests.seek(0)
    QUESTS_dict = pickle.load(SAVE_quests)
    SAVE_set = open(USERNAME + "_Set.set", 'rb')
    SAVE_set.seek(0)
    SET_dict = pickle.load(SAVE_set)
    print("GAME: Preparing to load inventory..")
    SAVE_inventory = open(USERNAME + ".inv", 'rb')
    SAVE_inventory.seek(0)
    INVENTORY_dict = pickle.load(SAVE_inventory)
    print("GAME: Loaded!\n")
    time.sleep(1)
    SAVE_dict['InTown'] = 1
    blockType_function()


def continueOrTown():
    global SAVE_dict

    fight_townOption = input("Do you want to continue searching for enemies or go back to town? [Y for SEARCH ENEMIES / N for BACK TO TOWN]: ")
    print("\n")
    if fight_townOption == "Y" or fight_townOption == "y":
        time.sleep(1)
        enemyChance()
    elif fight_townOption == "N" or fight_townOption == "n":
        print("You are returning back to the nearest town.")
        time.sleep(1)
        SAVE_dict['InTown'] = 1
        blockType_function()


def achievementSystem():
    global ACHIEVEMENTS_dict
    global currentEnemyName
    global SAVE_dict

    if ACHIEVEMENTS_dict['A1'] == 0 and SAVE_dict['times_VisitedTown'] == 100:
        ACHIEVEMENTS_dict['A1'] = 1  # 0 for enabled, 1 for completed
        print("GAME: Achievement Completed - \"Howdy townie?\" (Visit a town 100 times)")
        cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        db.commit()
        SAVE_dict['GOLDEN_DIAMONDS'] += 50
        sql_updatebalance = "UPDATE ACCOUNTS SET BALANCE = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['GOLDEN_DIAMONDS'], SAVE_dict['YourName'])
        cursor.execute(sql_updatebalance)
        db.commit()
        cursor.execute("SELECT BALANCE FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        sql_totalbalance = str(cursor.fetchone()[0])
        db.commit()
        print("You have been awarded 50 Golden Diamonds and now you have " + str(sql_totalbalance) + " in total.")
        ACHIEVEMENTS_dict['AchievementsCompleted'] += 1
        time.sleep(3)
        SAVEGAME()
    if ACHIEVEMENTS_dict['A2'] == 0 and SAVE_dict['EnemiesKilled'] == 100:
        ACHIEVEMENTS_dict['A2'] = 1
        print("GAME: Achievement Completed - \"Slayer\" (Kill 100 enemies)")
        cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        db.commit()
        SAVE_dict['GOLDEN_DIAMONDS'] += 100
        sql_updatebalance = "UPDATE ACCOUNTS SET BALANCE = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['GOLDEN_DIAMONDS'], SAVE_dict['YourName'])
        cursor.execute(sql_updatebalance)
        db.commit()
        cursor.execute("SELECT BALANCE FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        sql_totalbalance = str(cursor.fetchone()[0])
        db.commit()
        print("You have been awarded 100 Golden Diamonds and now you have " + str(sql_totalbalance) + " in total.")
        ACHIEVEMENTS_dict['AchievementsCompleted'] += 1
        time.sleep(3)
        SAVEGAME()
    if ACHIEVEMENTS_dict['A3'] == 0 and CONT2_dict['TravelledCONT2'] == 1:
        ACHIEVEMENTS_dict['A3'] = 1
        print("GAME: Achievement Completed - \"New land, hi-ho!\" (Travelled to Masgra for the first time)")
        cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        db.commit()
        SAVE_dict['GOLDEN_DIAMONDS'] += 50
        sql_updatebalance = "UPDATE ACCOUNTS SET BALANCE = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['GOLDEN_DIAMONDS'], SAVE_dict['YourName'])
        cursor.execute(sql_updatebalance)
        db.commit()
        cursor.execute("SELECT BALANCE FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        sql_totalbalance = str(cursor.fetchone()[0])
        db.commit()
        print("You have been awarded 50 Golden Diamonds and now you have " + str(sql_totalbalance) + " in total.")
        ACHIEVEMENTS_dict['AchievementsCompleted'] += 1
        time.sleep(3)
        SAVEGAME()
    if ACHIEVEMENTS_dict['A4'] == 0 and SAVE_dict['YourLevel'] == 20:
        ACHIEVEMENTS_dict['A4'] = 1
        print("GAME: Achievement Completed - \"Just getting stronger\" (Reached Level 20)")
        cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        db.commit()
        SAVE_dict['GOLDEN_DIAMONDS'] += 100
        sql_updatebalance = "UPDATE ACCOUNTS SET BALANCE = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['GOLDEN_DIAMONDS'], SAVE_dict['YourName'])
        cursor.execute(sql_updatebalance)
        db.commit()
        cursor.execute("SELECT BALANCE FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        sql_totalbalance = str(cursor.fetchone()[0])
        db.commit()
        print("You have been awarded 100 Golden Diamonds and now you have " + str(sql_totalbalance) + " in total.")
        ACHIEVEMENTS_dict['AchievementsCompleted'] += 1
        time.sleep(3)
        SAVEGAME()
    if ACHIEVEMENTS_dict['A5'] == 0 and SAVE_dict['YourLevel'] == 40:
        ACHIEVEMENTS_dict['A5'] = 1
        print("GAME: Achievement Completed - \"Earth-Shatteringly Powerful\" (Reached Level 40)")
        cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        db.commit()
        SAVE_dict['GOLDEN_DIAMONDS'] += 150
        sql_updatebalance = "UPDATE ACCOUNTS SET BALANCE = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['GOLDEN_DIAMONDS'], SAVE_dict['YourName'])
        cursor.execute(sql_updatebalance)
        db.commit()
        cursor.execute("SELECT BALANCE FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        sql_totalbalance = str(cursor.fetchone()[0])
        db.commit()
        print("You have been awarded 150 Golden Diamonds and now you have " + str(sql_totalbalance) + " in total.")
        ACHIEVEMENTS_dict['AchievementsCompleted'] += 1
        time.sleep(3)
        SAVEGAME()
    if ACHIEVEMENTS_dict['A6'] == 0 and SAVE_dict['YourLevel'] == 60:
        ACHIEVEMENTS_dict['A6'] = 1
        print("GAME: Achievement Completed - \"The Future's Saviour\" (Reached Level 60)")
        cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        db.commit()
        SAVE_dict['GOLDEN_DIAMONDS'] += 200
        sql_updatebalance = "UPDATE ACCOUNTS SET BALANCE = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['GOLDEN_DIAMONDS'], SAVE_dict['YourName'])
        cursor.execute(sql_updatebalance)
        db.commit()
        cursor.execute("SELECT BALANCE FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
        sql_totalbalance = str(cursor.fetchone()[0])
        db.commit()
        print("You have been awarded 200 Golden Diamonds and now you have " + str(sql_totalbalance) + " in total.")
        ACHIEVEMENTS_dict['AchievementsCompleted'] += 1
        time.sleep(3)
        SAVEGAME()


def startingPoint():
    global SAVE_dict
    global SET_dict
    global hasRegistered

    PYTHON_USERNAME = input("Username (Up to 16 characters): ")
    PYTHON_PASSWORD = input("Password (Up to 50 characters): ")
    PYTHON_EMAIL = input("E-mail address: ")
    PYTHON_CHARNAME = input("Character name: ")
    show_classes()
    SAVE_dict['YourClass'] = input("Select a class from the shown above: ")

    # vvvvvv -- THIS FIXES THE LOWERCASE INPUT -- vvvvvv
    if SAVE_dict['YourClass'] == "warrior":
        SAVE_dict['YourClass'] = "Warrior"
    elif SAVE_dict['YourClass'] == "rogue":
        SAVE_dict['YourClass'] = "Rogue"
    elif SAVE_dict['YourClass'] == "archer":
        SAVE_dict['YourClass'] = "Archer"
    elif SAVE_dict['YourClass'] == "mage":
        SAVE_dict['YourClass'] = "Mage"

    PYTHON_CLASS = SAVE_dict['YourClass']
    SAVE_dict['YourName'] = PYTHON_CHARNAME
    print("GAME: Writing data..")
    SAVE_dict['YourLevel'] = 1  # 1 for release
    SAVE_dict['YourHealth'] = 100  #
    SAVE_dict['YourMana'] = 30  #
    SAVE_dict['YourGold'] = 10  #
    SAVE_dict['TotalGoldAcquired'] += 10  # SAVE GAME INITIALIZE VALUES
    SAVE_dict['YourWeaponPower'] = 0  #
    SAVE_dict['YourExp'] = 0  #
    SAVE_dict['CurrentWeight'] = 0  #
    SAVE_dict['TotalWeight'] = 50  #
    SAVE_dict['InTown'] = 1  #
    PYTHON_LEVEL = SAVE_dict['YourLevel']
    sql = "INSERT INTO ACCOUNTS(USERNAME, \
        PASSWORD, EMAIL, CHARACTER_NAME, CLASS, LEVEL) \
        VALUES ('%s', '%s', '%s', '%s', '%s', '%d')" % \
          (PYTHON_USERNAME, PYTHON_PASSWORD, PYTHON_EMAIL, PYTHON_CHARNAME, PYTHON_CLASS, PYTHON_LEVEL)
    try:
        cursor.execute(sql)
        db.commit()
        print("Account created")
        hasRegistered = 1
    except:
        db.rollback()
        print("An error occured. Try again later or try different info.")

    if SAVE_dict['YourClass'] == "Mage" or SAVE_dict['YourClass'] == "Healer":
        SAVE_dict['YourMana'] = 40

    if SAVE_dict['YourClass'] == "Warrior":
        SAVE_dict['TotalWeight'] = 55

    time.sleep(1)
    print("You're gonna need a weapon and some armor if you're gonna go wander around.\n")
    time.sleep(1)
    print("1. Light-Armor Set: +8 Armor Points - Adds +10 Equipment Weight.\n2. Medium-Armor Set: +13 Armor Points - Adds +15 Equipment Weight.\n3. Heavy-Armor Set: +17 Armor Points - Adds +20 Equipment Weight.\n")
    startingArmorSet = input("Select one from the above, " + SAVE_dict['YourName'] + ". (Type 1, 2 or 3): ")

    if startingArmorSet == "1":
        SAVE_dict['YourArmor'] = 8
        SET_dict['ArmorName'] = "Light-Armor Set"
        SAVE_dict['CurrentWeight'] += 10
        sql_updatearmorpoints = "UPDATE ACCOUNTS SET ARMOR_POINTS = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourArmor'], SAVE_dict['YourName'])
        sql_updatearmorname = "UPDATE ACCOUNTS SET ARMOR_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['ArmorName'], SAVE_dict['YourName'])
        cursor.execute(sql_updatearmorpoints)
        db.commit()
        cursor.execute(sql_updatearmorname)
        db.commit()
        print("You selected the Light-Armor set.\n")
        time.sleep(1)
    elif startingArmorSet == "2":
        SAVE_dict['YourArmor'] = 13
        SET_dict['ArmorName'] = "Medium-Armor Set"
        SAVE_dict['CurrentWeight'] += 15
        sql_updatearmorpoints = "UPDATE ACCOUNTS SET ARMOR_POINTS = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourArmor'], SAVE_dict['YourName'])
        sql_updatearmorname = "UPDATE ACCOUNTS SET ARMOR_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['ArmorName'], SAVE_dict['YourName'])
        cursor.execute(sql_updatearmorpoints)
        db.commit()
        cursor.execute(sql_updatearmorname)
        db.commit()
        print("You selected the Medium-Armor set.\n")
        time.sleep(1)
    elif startingArmorSet == "3":
        SAVE_dict['YourArmor'] = 17
        SET_dict['ArmorName'] = "Heavy-Armor Set"
        SAVE_dict['CurrentWeight'] += 20
        sql_updatearmorpoints = "UPDATE ACCOUNTS SET ARMOR_POINTS = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourArmor'], SAVE_dict['YourName'])
        sql_updatearmorname = "UPDATE ACCOUNTS SET ARMOR_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['ArmorName'], SAVE_dict['YourName'])
        cursor.execute(sql_updatearmorpoints)
        db.commit()
        cursor.execute(sql_updatearmorname)
        db.commit()
        print("You selected the Heavy-Armor set.\n")
        time.sleep(1)
    else:
        print("You're punished for not selecting the right number specified. No armor given.\n")

    if SAVE_dict['YourClass'] == "Warrior":
        print("1. Rusty Sword, +5 Weapon Power - CAN parry but CANNOT block CANNOT execute skills that require a shield equipped, adds +10 Equipment Weight.\n2. Rusty Sword and Cracked Wooden Shield, +5 Weapon Power - CAN block and execute skills that require a shield equipped but CANNOT parry, adds +20 Equipment Weight.\n3. Rusty Sword and Rusty Sword (dual-wield), +10 Weapon Power - CANNOT parry, CANNOT block, CANNOT execute skills that require a shield equipped, adds +18 Equipment Weight.\n")
        startingWeapon = input("Select one from the above, " + SAVE_dict['YourName'] + ". (Type 1, 2 or 3): ")
        if startingWeapon == "1":
            SAVE_dict['YourWeaponPower'] = 5
            SAVE_dict['temp_weaponPower'] = 5
            SAVE_dict['Parry'] = 1
            SAVE_dict['Block'] = 0
            SAVE_dict['ShieldEquipped'] = 0
            SET_dict['WeaponName'] = "Rusty Sword"
            sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
            SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
            sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
            SET_dict['WeaponName'], SAVE_dict['YourName'])
            cursor.execute(sql_updateweaponpoints)
            db.commit()
            cursor.execute(sql_updateweaponname)
            db.commit()
            SAVE_dict['CurrentWeight'] += 10
            print("You selected to equip the Rusty Sword.\n")
            time.sleep(1)
        elif startingWeapon == "2":
            SAVE_dict['YourWeaponPower'] = 5
            SAVE_dict['temp_weaponPower'] = 5
            SAVE_dict['Parry'] = 0
            SAVE_dict['Block'] = 1
            SAVE_dict['ShieldEquipped'] = 1
            SET_dict['WeaponName'] = "Rusty Sword and Cracked Wooden Shield"
            sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
            SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
            sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
            SET_dict['WeaponName'], SAVE_dict['YourName'])
            cursor.execute(sql_updateweaponpoints)
            db.commit()
            cursor.execute(sql_updateweaponname)
            db.commit()
            SAVE_dict['CurrentWeight'] += 20
            print("You selected to equip the Rusty Sword and Cracked Wooden Shield.\n")
            time.sleep(1)
        elif startingWeapon == "3":
            SAVE_dict['YourWeaponPower'] = 10
            SAVE_dict['temp_weaponPower'] = 10
            SAVE_dict['Parry'] = 0
            SAVE_dict['Block'] = 0
            SAVE_dict['ShieldEquipped'] = 0
            SET_dict['WeaponName'] = "Rusty Swords (Dual-Wield)"
            sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
            SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
            sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
            SET_dict['WeaponName'], SAVE_dict['YourName'])
            cursor.execute(sql_updateweaponpoints)
            db.commit()
            cursor.execute(sql_updateweaponname)
            db.commit()
            SAVE_dict['CurrentWeight'] += 18
            print("You selected to equip the Rusty Sword and Rusty Sword (dual-wield).\n")
            time.sleep(1)
        else:
            print("You're punished for not selecting the right number specified. No weapon given.\n")
            SAVE_dict['YourWeaponPower'] = 1
            SET_dict['WeaponName'] = "Bare-Handed"
            sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
            SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
            sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
            SET_dict['WeaponName'], SAVE_dict['YourName'])
            cursor.execute(sql_updateweaponpoints)
            db.commit()
            cursor.execute(sql_updateweaponname)
            db.commit()
            SAVE_dict['temp_weaponPower'] = 1
            time.sleep(1)

    if SAVE_dict['YourClass'] == "Rogue":
        print("By default, the Rogue class is equipped with a Rusty Dagger, which gives you +6 Weapon Power - CAN execute Stealth.")
        SAVE_dict['YourWeaponPower'] = 6
        SAVE_dict['temp_weaponPower'] = 6
        SET_dict['WeaponName'] = "Rusty Dagger"
        sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
        sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['WeaponName'], SAVE_dict['YourName'])
        cursor.execute(sql_updateweaponpoints)
        db.commit()
        cursor.execute(sql_updateweaponname)
        db.commit()
        SAVE_dict['CurrentWeight'] += 10
        time.sleep(1)

    if SAVE_dict['YourClass'] == "Archer":
        print("By default, the Archer class is equipped with a Wooden Bow and Wooden Arrows, which give you +10 Weapon Power.")
        SAVE_dict['YourWeaponPower'] = 10
        SAVE_dict['temp_weaponPower'] = 10
        SET_dict['WeaponName'] = "Wooden Bow and Wooden Arrows"
        sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
        sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['WeaponName'], SAVE_dict['YourName'])
        cursor.execute(sql_updateweaponpoints)
        db.commit()
        cursor.execute(sql_updateweaponname)
        db.commit()
        SAVE_dict['CurrentWeight'] += 12
        time.sleep(1)

    if SAVE_dict['YourClass'] == "Mage":
        print("By default, the Mage class is equipped with a Wooden Staff and a Basic Book of Magics, which give you +10 Weapon Power.")
        SAVE_dict['YourWeaponPower'] = 10
        SAVE_dict['temp_weaponPower'] = 10
        SET_dict['WeaponName'] = "Wooden Staff and a Basic Book of Magics"
        sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
        sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['WeaponName'], SAVE_dict['YourName'])
        cursor.execute(sql_updateweaponpoints)
        db.commit()
        cursor.execute(sql_updateweaponname)
        db.commit()
        SAVE_dict['CurrentWeight'] += 12
        time.sleep(1)

    if SAVE_dict['YourClass'] == "Healer":
        print("By default, the Healer class is equipped with a Wooden Wand, which gives you +5 Weapon Power")
        SAVE_dict['YourWeaponPower'] = 5
        SAVE_dict['temp_weaponPower'] = 5
        SET_dict['WeaponName'] = "Wooden Wand"
        sql_updateweaponpoints = "UPDATE ACCOUNTS SET WEAPON_POWER = '%d' WHERE CHARACTER_NAME = '%s'" % (
        SAVE_dict['YourWeaponPower'], SAVE_dict['YourName'])
        sql_updateweaponname = "UPDATE ACCOUNTS SET WEAPON_NAME = '%s' WHERE CHARACTER_NAME = '%s'" % (
        SET_dict['WeaponName'], SAVE_dict['YourName'])
        cursor.execute(sql_updateweaponpoints)
        db.commit()
        cursor.execute(sql_updateweaponname)
        db.commit()
        SAVE_dict['CurrentWeight'] += 10
        time.sleep(1)

    print("Equipment Weight: " + str(SAVE_dict['CurrentWeight']) + "/" + str(SAVE_dict['TotalWeight']) + ".")
    time.sleep(2)

    SAVEGAME()
    SAVE_dict['InTown'] = 1
    print("Entering your first town..\n")
    mixer.music.fadeout(1500)
    time.sleep(2)
    blockType_function()


def lootChance():
    global lootItems
    global lootWeapons
    global lootArmor
    global SAVE_dict
    global INVENTORY_dict
    global SET_dict
    global equipWeapon_select
    global equipArmor_select

    itemChance = random.randint(1, 11)  # 1,3 for testing, 1,11 for release.

    weaponChance = random.randint(1, 16)  # 1,3 for testing, 1,16 for release.

    armorChance = random.randint(1, 18)  # 1,3 for testing, 1,18 for release.

    if itemChance in range(1, 3):
        itemLooted = random.choice(lootItems)
        print("GAME: You've looted a " + itemLooted + ".")
        INVENTORY_dict[itemLooted] += 1
        print("GAME: You now have " + str(INVENTORY_dict[itemLooted]) + " " + itemLooted)
        time.sleep(2)
        rollLoot_cost = 50 * (SAVE_dict['YourLevel'] / 1.8)
        print("Current gold: " + str(SAVE_dict['YourGold']))
        rollLoot = input("GAME: Do you want to roll the dices to get the same item one more time? (Costs " + str(
            round(rollLoot_cost)) + " gold) [Y/N]: ")
        if rollLoot == "N" or rollLoot == "n":
            time.sleep(1)
            pass
        elif rollLoot == "Y" or rollLoot == "y":
            if SAVE_dict['YourGold'] >= rollLoot_cost:
                SAVE_dict['YourGold'] -= rollLoot_cost
                print(SAVE_dict['YourName'] + " rolls the dice and gets:\n")
                time.sleep(1)
                die1 = random.randint(1, 6)
                print("First die: " + str(die1))
                die2 = random.randint(1, 6)
                print("Second die: " + str(die2))
                print("\n")
                result = die1 + die2
                if (result == 12):
                    print("Congratulations! You earned another " + itemLooted + "!")
                    INVENTORY_dict[itemLooted] += 1
            elif SAVE_dict['YourGold'] < rollLoot_cost:
                print("GAME: You don't have enough gold to roll the dices.")
                time.sleep(2.5)
        itemLooted = ""

    if weaponChance in range(1, 3):
        if SAVE_dict['YourClass'] == "Warrior":
            weaponLooted_name = random.choice(lootWeapons_Warrior)
        elif SAVE_dict['YourClass'] == "Rogue":
            weaponLooted_name = random.choice(lootWeapons_Rogue)
        elif SAVE_dict['YourClass'] == "Archer":
            weaponLooted_name = random.choice(lootWeapons_Archer)
        elif SAVE_dict['YourClass'] == "Mage":
            weaponLooted_name = random.choice(lootWeapons_Mage)
        elif SAVE_dict['YourClass'] == "Healer":
            weaponLooted_name = random.choice(lootWeapons_Healer)
        weaponLooted_power = random.randint(6, 7 + (SAVE_dict['YourLevel'] * 2))
        if weaponLooted_power > SAVE_dict['YourWeaponPower']:
            print(currentEnemyName + " has dropped " + weaponLooted_name + " and it has " + str(
                weaponLooted_power) + " Weapon Power and your " + SET_dict['WeaponName'] + " has " + str(
                SAVE_dict['YourWeaponPower']) + ".")
            time.sleep(1)
            equipWeapon_select = input("Do you want to equip it? [Y/N]: ")
            if equipWeapon_select == "Y" or equipWeapon_select == "y":
                weaponLooted_weight = (SAVE_dict['YourLevel'] * 3) + random.randint(2, 5)
                weightSystem(weaponLooted_name, weaponLooted_weight,
                             weaponLooted_power)  # Executes weightSystem() function with weaponLooted_name as itemToEquip parameter, weaponLooted_weight as itemWeight parameter
            elif equipWeapon_select == "N" or equipWeapon_select == "n":
                time.sleep(1)
                pass
            equipWeapon_select = ""

    if armorChance in range(1, 3):
        if SAVE_dict['YourClass'] == "Warrior":
            armorLooted_name = random.choice(lootArmor_Warrior)
        elif SAVE_dict['YourClass'] == "Rogue":
            armorLooted_name = random.choice(lootArmor_Rogue)
        elif SAVE_dict['YourClass'] == "Archer":
            armorLooted_name = random.choice(lootArmor_Archer)
        elif SAVE_dict['YourClass'] == "Mage":
            armorLooted_name = random.choice(lootArmor_Mage)
        elif SAVE_dict['YourClass'] == "Healer":
            armorLooted_name = random.choice(lootArmor_Healer)
        armorLooted_armor = random.randint(12, 13 + (SAVE_dict['YourLevel'] * 2))
        if armorLooted_armor > SAVE_dict['YourArmor']:
            print(currentEnemyName + " has dropped " + armorLooted_name + " and it has " + str(
                armorLooted_armor) + " Armor Points and your " + SET_dict['ArmorName'] + " has " + str(
                SAVE_dict['YourArmor']) + ".")
            time.sleep(1)
            equipArmor_select = input("Do you want to equip it? [Y/N]: ")
            if equipArmor_select == "Y" or equipArmor_select == "y":
                armorLooted_weight = (SAVE_dict['YourLevel'] * 3) + random.randint(4, 8)
                weightSystem(armorLooted_name, armorLooted_weight, armorLooted_armor)
            elif equipArmor_select == "N" or equipArmor_select == "n":
                time.sleep(1)
                pass
            equipArmor_select = ""

    if itemChance not in range(1, 3) and weaponChance not in range(1, 3) and armorChance not in range(1, 3):
        print("GAME: No loot acquired.\n")
        time.sleep(1)


def questCompletion():
    global QUESTS_dict
    global SAVE_dict
    global currentEnemyName
    if QUESTS_dict['active1'] == 1 and currentEnemyName == "Black Ninja":
        for completion in range(0, 11):
            QUESTS_dict['killed10BN'] += 1
            print("Killed " + str(QUESTS_dict['killed10BN']) + "/10 Black Ninjas.")
            currentEnemyName = ""
            time.sleep(2)
            break
        if QUESTS_dict['killed10BN'] == 10:
            QUESTS_dict['active1'] = 2  # 0 for disabled, 1 for enabled, 2 for completed
            print("You have killed 10 Black Ninjas and thus completed the quest for it. You are awarded with 1.5 EXP and 13 Gold.")
            SAVE_dict['YourExp'] += 3
            SAVE_dict['YourGold'] += 30
            SAVE_dict['TotalGoldAcquired'] += 30
            time.sleep(2)
    if QUESTS_dict['active2'] == 1 and currentEnemyName == "White Ninja":
        for completion in range(0, 6):
            QUESTS_dict['killed5WN'] += 1
            print("Killed " + str(QUESTS_dict['killed5WN']) + "/5 White Ninjas.")
            currentEnemyName = ""
            time.sleep(2)
            break
        if QUESTS_dict['killed5WN'] == 5:
            QUESTS_dict['active2'] = 2  # 0 for disabled, 1 for enabled, 2 for completed
            print("You have killed 5 White Ninjas and thus completed the quest for it. You are awarded with 2.75 and 17 Gold.")
            SAVE_dict['YourExp'] += 5
            SAVE_dict['YourGold'] += 35
            SAVE_dict['TotalGoldAcquired'] += 35
            time.sleep(2)


def expGain():
    global SAVE_dict
    global weather
    global area

    if SAVE_dict['YourLevel'] in range(1, 31):

        #        if SAVE_dict['YourLevel'] == 1:
        #            expGained = (SAVE_dict['YourLevel'] / 2) * 1.1
        #        elif SAVE_dict['YourLevel'] in range(2,7):
        #            expGained = (SAVE_dict['YourLevel'] / 2.65) * 1.1
        #        elif SAVE_dict['YourLevel'] in range(7,14):
        #            expGained = (SAVE_dict['YourLevel'] / 2.81) * 1.08
        #        elif SAVE_dict['YourLevel'] in range(14,25):
        #            expGained = (SAVE_dict['YourLevel'] / 2.89) * 1.06
        #        elif SAVE_dict['YourLevel'] in range(25,31):
        #            expGained = (SAVE_dict['YourLevel'] / 2.97) * 1.1

        #        if SAVE_dict['YourLevel'] == 1:
        #            totalExpNeeded = (SAVE_dict['YourLevel'] * 2.75)
        #        elif SAVE_dict['YourLevel'] in range(2,3):
        #            totalExpNeeded = (SAVE_dict['YourLevel'] * 3.25)
        #        elif SAVE_dict['YourLevel'] in range(3,9):
        #            totalExpNeeded = (SAVE_dict['YourLevel'] * 7.3)
        #        elif SAVE_dict['YourLevel'] in range(9,15):
        #            totalExpNeeded = (SAVE_dict['YourLevel'] * 10)
        #        else:
        #            totalExpNeeded = (SAVE_dict['YourLevel'] * 12.5)

        # -------- vv EXPERIMENTAL NEW EXP SYSTEM vv ---------

        if SAVE_dict['YourLevel'] == 1:
            totalExpNeeded = 100
            expGained = 20 + random.randint(1, 5)
        else:
            totalExpNeeded = 101 + (12 * SAVE_dict['YourLevel'])
            expGained = (20 + SAVE_dict['YourLevel']) + random.randint(1, 6)

        SAVE_dict['YourExp'] += expGained

        if SAVE_dict['YourExp'] >= totalExpNeeded:
            SAVE_dict['YourLevel'] += 1  # Adds +1 Level to your Level.
            SAVE_dict['YourMana'] += 4  # Adds +4 Mana to your Mana.
            SAVE_dict['YourHealth'] += 6  # Adds +6 Health to your Health.
            SAVE_dict['YourWeaponPower'] += 2  # Adds +2 Weapon Power to your Weapon Power.
            SAVE_dict['YourArmor'] += 2  # Adds +2 Armor Points to your Armor Points.
            SAVE_dict['TotalWeight'] += 2  # Adds +2 to Maximum Weight.
            print("GAME: LEVEL UP! You are now Level " + str(SAVE_dict['YourLevel']))
            time.sleep(3)
            print("GAME: You gained +4 Mana, (" + str(SAVE_dict['YourMana']) + " in total).")
            print("GAME: You gained +6 Health, (" + str(SAVE_dict['YourHealth']) + " in total).")
            print("GAME: You gained +2 Weapon Power, (" + str(SAVE_dict['YourWeaponPower']) + " in total).")
            print("GAME: You gained +2 Armor Points, (" + str(SAVE_dict['YourArmor']) + " in total).")
            print("GAME: You gained +2 Maximum Weight (" + str(SAVE_dict['TotalWeight']) + " in total).")
            cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
            db.commit()
            sql_updatelevel = "UPDATE ACCOUNTS SET LEVEL = '%d' WHERE CHARACTER_NAME = '%s'" % (SAVE_dict['YourLevel'], SAVE_dict['YourName'])
            cursor.execute(sql_updatelevel)
            db.commit()
            time.sleep(3)
            if SAVE_dict['YourLevel'] == 30:
                print("Be careful, " + SAVE_dict['YourClass'] + ", the Harbringer is out to get you and who knows who else..")
                time.sleep(1)
        else:
            print("GAME: You have defeated " + currentEnemyName + ". You now have " + str(round(SAVE_dict['YourExp'], 3)) + " EXP in total (gained +" + str(round(expGained, 3)) + "). You need " + str(totalExpNeeded) + " EXP in total to Level Up.")
        questCompletion()
        SAVEGAME()
        time.sleep(1)

    elif SAVE_dict['YourLevel'] in range(10, 51) and CONT2_dict['TravelledCONT2'] == 1:  # ------------ S E C O N D . C O N T I N E N T . L E V E L S . U P . T O . 50 . --------------

        if SAVE_dict['YourLevel'] == 10:
            expGained = (SAVE_dict['YourLevel'] / 2.81) * 1.05
        elif SAVE_dict['YourLevel'] in range(11, 23):
            expGained = (SAVE_dict['YourLevel'] / 2.92) * 1.05
        elif SAVE_dict['YourLevel'] in range(23, 31):
            expGained = (SAVE_dict['YourLevel'] / 3) * 1.07
        elif SAVE_dict['YourLevel'] in range(31, 41):
            expGained = (SAVE_dict['YourLevel'] / 3.12) * 1.08
        elif SAVE_dict['YourLevel'] in range(41, 51):
            expGained = (SAVE_dict['YourLevel'] / 3.3) * 1.09

        if SAVE_dict['YourLevel'] == 10:
            totalExpNeeded = (SAVE_dict['YourLevel'] * 11)
        elif SAVE_dict['YourLevel'] in range(11, 23):
            totalExpNeeded = (SAVE_dict['YourLevel'] * 14)
        elif SAVE_dict['YourLevel'] in range(23, 31):
            totalExpNeeded = (SAVE_dict['YourLevel'] * 16)
        elif SAVE_dict['YourLevel'] in range(31, 41):
            totalExpNeeded = (SAVE_dict['YourLevel'] * 18)
        elif SAVE_dict['YourLevel'] in range(41, 51):
            totalExpNeeded = (SAVE_dict['YourLevel'] * 20)

        SAVE_dict['YourExp'] += expGained

        if SAVE_dict['YourExp'] >= totalExpNeeded:
            SAVE_dict['YourLevel'] += 1  # Adds +1 Level to your Level.
            SAVE_dict['YourMana'] += 4  # Adds +4 Mana to your Mana.
            SAVE_dict['YourHealth'] += 6  # Adds +6 Health to your Health.
            SAVE_dict['YourWeaponPower'] += 2  # Adds +2 Weapon Power to your Weapon Power.
            SAVE_dict['YourArmor'] += 2  # Adds +2 Armor Points to your Armor Points.
            SAVE_dict['TotalWeight'] += 2  # Adds +2 to Maximum Weight.
            print("GAME: LEVEL UP! You are now Level " + str(SAVE_dict['YourLevel']))
            time.sleep(1)
            print("GAME: You gained +4 Mana, (" + str(SAVE_dict['YourMana']) + " in total).")
            print("GAME: You gained +6 Health, (" + str(SAVE_dict['YourHealth']) + " in total).")
            print("GAME: You gained +2 Weapon Power, (" + str(SAVE_dict['YourWeaponPower']) + " in total).")
            print("GAME: You gained +2 Armor Points, (" + str(SAVE_dict['YourArmor']) + " in total).")
            print("GAME: You gained +2 Maximum Weight (" + str(SAVE_dict['TotalWeight']) + " in total).")
            cursor.execute("SELECT * FROM ACCOUNTS WHERE CHARACTER_NAME = '" + SAVE_dict['YourName'] + "'")
            db.commit()
            sql_updatelevel = "UPDATE ACCOUNTS SET LEVEL = '%d' WHERE CHARACTER_NAME = '%s'" % (SAVE_dict['YourLevel'], SAVE_dict['YourName'])
            cursor.execute(sql_updatelevel)
            db.commit()
            time.sleep(3)
        else:
            print("GAME: You have defeated " + currentEnemyName + ". You now have " + str(round(SAVE_dict['YourExp'], 3)) + " EXP in total (gained +" + str(round(expGained, 3)) + "). You need " + str(totalExpNeeded) + " EXP in total to Level Up.")
        questCompletion()
        SAVEGAME()
        time.sleep(1)


def exitBoat():
    print("Exiting the boat and going into the town..")
    SAVE_dict['InTown'] = 0
    SAVE_dict['InTown'] = 1
    time.sleep(2)
    blockType_Safe()


def show_classes():
    print("\n".join(class_list) + "\n")


def show_warriorskills():
    print("\n".join(warrior_skills) + "\n")


def show_rogueskills():
    print("\n".join(rogue_skills) + "\n")


def show_stealthed_rogueskills():
    print("\n".join(rogueS_skills) + "\n")


def show_archerskills():
    print("\n".join(archer_skills) + "\n")


def show_fire_archerskills():
    print("\n".join(archerF_skills) + "\n")


def show_mageskills():
    print("\n".join(mage_skills) + "\n")


def show_healerskills():
    print("\n".join(healer_skills) + "\n")


def show_npcnames():
    global SAVE_dict

    print("1. Sullivan the Mage")
    print("2. Bryan the Blacksmith")
    print("3. Wally the Potionmaker")
    print("4. Kyle the Armorsmith")
    print("5. Bob the Craftsman")
    print("6. Colin the Captain (Story Quests)")
    print("7. Helena the Captain's Daughter")
    print("8. Takashi the Fisherman (Side Quests)")
    print("9. Ken the Musician (SAVE GAME)")
    print("10. Matthew the Boatskeeper (250 Gold fee)")
    print("11. View Stats (Consumes 1 SAFE Turn)")
    if SAVE_dict['Mail'] == 0:
        print("12. Your Mailbox")
    elif SAVE_dict['Mail'] == 1:
        print("12. Your Mailbox (1 NEW MESSAGE")
    elif SAVE_dict['Mail'] > 1:
        print("12. Your Mailbox (" + str(SAVE_dict['Mail']) + " NEW MESSAGES")
    print("0. Leave the town")


def show_npcnames2():
    global SAVE_dict

    print("1. Magnar the Mage")
    print("2. Titus the Blacksmith")
    print("3. Cromwell the Potionmaker")
    print("4. Adam the Armorsmith")
    print("5. Aaron the Craftsman")
    print("6. Guild Headquarters")
    if SAVE_dict['YourLevel'] >= 30 and SAVE_dict['YourClass'] == "Rogue":
        print("7. Ralph's Tavern (Class Advancement Quest Available)")
    else:
        print("7. Ralph's Tavern")
    print("8. A Mysterious Man (Story Quests)")
    print("9. Higar's Arena (Player vs Player)")
    print("10. Sebastian the Musician (SAVE GAME)")
    print("11. Finn the Boatskeeper (250 Gold fee)")
    print("12. View Stats (Consumes 1 SAFE Turn)")
    print("13. View Leaderboards (Consumes 1 SAFE Turn)")
    print("0. Leave the town")


def Weather():
    global SAVE_dict
    global CONT2_dict
    global weather
    global area
    global areaChanged

    n = 5

    if SAVE_dict['InTown'] == 0:
        SAVE_dict['temp_visitedTown'] += 1
    elif SAVE_dict['InTown'] == 1:

        SAVE_dict['YourWeaponPower'] = SAVE_dict['temp_weaponPower']
        if not weather:
            pass
        else:
            print("You are recovering from the weather.\n")
        time.sleep(2)

    if SAVE_dict['temp_visitedTown'] % n == 0 and SAVE_dict['InTown'] == 0:
        WeatherChance = random.randint(0, 100)
        if WeatherChance in range(0, 21):
            weather = "Snow"
            print("Current Weather: " + weather)
        elif WeatherChance in range(21, 41):
            weather = "Sunny"
            print("Current Weather: " + weather)
        elif WeatherChance in range(41, 61):
            weather = "Windy"
            print("Current Weather: " + weather)
        elif WeatherChance in range(61, 81):
            weather = "Stormy"
            print("Current Weather: " + weather)
        elif WeatherChance in range(81, 101):
            weather = "Foggy"
            print("Current Weather: " + weather)
    else:
        pass

    if weather == "Snow" and SAVE_dict['InTown'] == 0:
        if SAVE_dict['YourClass'] == "Warrior":
            print("You are not affected by this weather type.\n")
            time.sleep(3)
        elif SAVE_dict['YourClass'] == "Rogue":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
        elif SAVE_dict['YourClass'] == "Archer":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
        elif SAVE_dict['YourClass'] == "Mage":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower

    elif weather == "Sunny" and SAVE_dict['InTown'] == 0:
        if SAVE_dict['YourClass'] == "Warrior":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            lost_armor = SAVE_dict['YourArmor'] / 2
            print("You are affected by this weather type. You lose " + str(lost_armor) + " Armor and " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_armor'] = SAVE_dict['YourArmor']
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourArmor'] -= lost_armor
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
        elif SAVE_dict['YourClass'] == "Rogue":
            print("You are not affected by this weather type.\n")
            time.sleep(3)
        elif SAVE_dict['YourClass'] == "Archer":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
        elif SAVE_dict['YourClass'] == "Mage":
            print("You are not affected by this weather type.")
            time.sleep(3)

    elif weather == "Windy" and SAVE_dict['InTown'] == 0:
        if SAVE_dict['YourClass'] == "Warrior":
            lost_armor = SAVE_dict['YourArmor'] / 2
            print("You are affected by this weather type. You lose " + str(lost_armor) + " Armor.\n")
            time.sleep(3)
            SAVE_dict['temp_armor'] = SAVE_dict['YourArmor']
            SAVE_dict['YourArmor'] -= lost_armor
        elif SAVE_dict['YourClass'] == "Rogue":
            print("You are not affected by this weather type.\n")
            time.sleep(3)
        elif SAVE_dict['YourClass'] == "Archer":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
        elif SAVE_dict['YourClass'] == "Mage":
            print("You are not affected by this weather type.\n")
            time.sleep(3)

    elif weather == "Stormy" and SAVE_dict['InTown'] == 0:
        if SAVE_dict['YourClass'] == "Warrior":
            lost_armor = SAVE_dict['YourArmor'] / 2
            print("You are affected by this weather type. You lose " + str(lost_armor) + " Armor.\n")
            time.sleep(3)
            SAVE_dict['temp_armor'] = SAVE_dict['YourArmor']
            SAVE_dict['YourArmor'] -= lost_armor
        elif SAVE_dict['YourClass'] == "Rogue":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
            print("temp: " + str(SAVE_dict['temp_weaponPower']))
            print("weapon power: " + str(SAVE_dict['YourWeaponPower']))
        elif SAVE_dict['YourClass'] == "Archer":
            lost_weaponPower = random.randint(3, (SAVE_dict['YourWeaponPower'] - 2))
            print("You are affected by this weather type. You lose " + str(lost_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] -= lost_weaponPower
        elif SAVE_dict['YourClass'] == "Mage":
            print("You are not affected by this weather type.\n")
            time.sleep(3)

    elif weather == "Foggy" and SAVE_dict['InTown'] == 0:
        if SAVE_dict['YourClass'] == "Warrior":
            print("You are not affected by this weather type.\n")
            time.sleep(3)
        elif SAVE_dict['YourClass'] == "Rogue":
            gained_weaponPower = random.randint(3, 6)
            print("You are affected by this weather type. You gain " + str(gained_weaponPower) + " Weapon Power.\n")
            time.sleep(3)
            SAVE_dict['temp_weaponPower'] = SAVE_dict['YourWeaponPower']
            SAVE_dict['YourWeaponPower'] += gained_weaponPower
            print("temp: " + str(SAVE_dict['temp_weaponPower']))
            print("weapon power: " + str(SAVE_dict['YourWeaponPower']))


def ChangeArea():
    global weather
    global area
    global areaChanged

    n = 5

    print("WARNING! Timespace anomaly!")
    time.sleep(3)

    areaChance = random.randint(0, 160)
    if areaChance in range(0, 21):
        area = "Desert"
        if weather == "Snow":
            area = "Snowy Desert"

    elif areaChance in range(20, 41):
        area = "Glacier"
        if weather == "Sunny":
            area = "Melting Glacier"
        elif weather == "Snow":
            weather = "Cold Snap"
        elif weather == "Windy":
            weather = "Blinding Snow"
        elif weather == "Stormy":
            weather = "Deadly Cold"
        elif weather == "Foggy":
            weather = "Snow Drift"

    elif areaChance in range(40, 61):
        area = "Underground"

    elif areaChance in range(60, 81):
        area = "Active Volcano"
        if weather == "Sunny":
            weather = "Searing Heat"
        elif weather == "Windy":
            weather = "Ashfall"
        elif weather == "Stormy":
            weather = "Ash Hail"
        elif weather == "Foggy":
            weather = "Dust Cloud"

    elif areaChance in range(80, 101):
        area = "Forest"
        if weather == "Stormy":
            area = "Rainforest"

    elif areaChance in range(100, 121):
        area = "Swamp"
        if weather == "Stormy":
            area = "Drowning Swamp"
        if weather == "Sunny":
            print("The mud of the swamp gets harder.")

    elif areaChance in range(120, 141):
        area = "Mountaintop"
        if weather == "Snow":
            weather = "Blizzard"

    elif areaChance in range(140, 161):
        area = "Isthmus bridge"

    areaChanged = 1


def blockType_Safe():
    global SAVE_dict
    global QUESTS_dict
    global SKILLS_dict
    global SET_dict
    global CONT2_dict
    global ACHIEVEMENTS_dict

    # Recover from Weather
    Weather()

    # Check for any achievements completed
    achievementSystem()

    # How many times you have visited the town
    SAVE_dict['times_VisitedTown'] += 1

    # Play the town ambience sound
    if config.get('General', 'music') == "On":
        mixer.music.load(town_ambient)
        mixer.music.play(-1)
    else:
        mixer.music.stop()

    # Critical Rate Upgrade
    criticalRateCost = ((SAVE_dict['YourLevel'] + 12) * SAVE_dict['YourLevel']) + 9

    # Weight Expansion Upgrade
    weightExpansionCost = ((SAVE_dict['YourLevel'] + 19) * SAVE_dict['YourLevel']) + 5

    # Upgrade Weapon
    upgradeWeaponCost = 70 * SAVE_dict['YourLevel']

    # Warrior Upgrades
    dChargeUpgradeCost = (SAVE_dict['YourLevel'] + 4) * SAVE_dict['YourLevel']
    sBashUpgradeCost = (SAVE_dict['YourLevel'] + 6) * SAVE_dict['YourLevel']
    dSlashUpgradeCost = (SAVE_dict['YourLevel'] + 10) * SAVE_dict['YourLevel']
    sHellUpgradeCost = (SAVE_dict['YourLevel'] + 16) * SAVE_dict['YourLevel']

    # Rogue Upgrades
    bDaggerUpgradeCost = (SAVE_dict['YourLevel'] + 5) * SAVE_dict['YourLevel'] + 3
    sFangsUpgradeCost = ((SAVE_dict['YourLevel'] + 23) * SAVE_dict['YourLevel'])

    # Archer Upgrades
    oRollUpgradeCost = (SAVE_dict['YourLevel'] + 5) * SAVE_dict['YourLevel']
    hArrowsUpgradeCost = (SAVE_dict['YourLevel'] + 8) * SAVE_dict['YourLevel']
    fArrowsUpgradeCost = (SAVE_dict['YourLevel'] + 11) * SAVE_dict['YourLevel']
    sPhoenixUpgradeCost = (SAVE_dict['YourLevel'] + 17) * SAVE_dict['YourLevel']

    # Mage Upgrades
    aPentagramUpgradeCost = (SAVE_dict['YourLevel'] + 11) * SAVE_dict['YourLevel']
    cElementsUpgradeCost = (SAVE_dict['YourLevel'] + 18) * SAVE_dict['YourLevel']

    # Healer Upgrades
    hLightUpgradeCost = (SAVE_dict['YourLevel'] + 7) * SAVE_dict['YourLevel']
    lHammerUpgradeCost = (SAVE_dict['YourLevel'] + 12) * SAVE_dict['YourLevel']

    if CONT2_dict['AtMasgra'] == 0:
        for town_safeturns in range(1, 4):
            show_npcnames()
            print("SAFE Turn: " + str(town_safeturns))
            town_npcselection = input("Select one to meet from the above: ")
            if town_npcselection == "1":
                entering_shop = mixer.Channel(0)
                print("You're walking towards Sullivan the Mage.")
                entering_shop.play(mixer.Sound(entering_shop_sound))
                time.sleep(2.8)
                town_npcselect = input("Sullivan the Mage: Hello, what can I do for you?\n1. Shop\n2. Talk\n3. Exit the shop\nSelect one from the above: ")
                if town_npcselect == "1":
                    print("You have " + str(round(SAVE_dict['YourGold'])) + " gold.")
                    if SAVE_dict['YourClass'] == "Warrior":
                        print("1. Upgrade Devastating Charge (Requires " + str(dChargeUpgradeCost) + " gold.)\n2. Upgrade Shield Bash (Requires " + str(sBashUpgradeCost) + " gold.)\n3. Upgrade Decapitating Slash (Requires " + str(dSlashUpgradeCost) + " gold.)\n4. Upgrade Thousand Spiritual Swords of Hell (Requires " + str(sHellUpgradeCost) + " gold.)")
                    elif SAVE_dict['YourClass'] == "Rogue":
                        print("1. Upgrade Bleeding Dagger (Requires " + str(bDaggerUpgradeCost) + " gold.)\n2. Upgrade Shadow Fangs (Requires " + str(sFangsUpgradeCost) + " gold.)")
                    elif SAVE_dict['YourClass'] == "Archer":
                        print("1. Upgrade Offensive Roll (Requires " + str(oRollUpgradeCost) + " gold.)\n2. Upgrade Hail of Arrows (Requires " + str(hArrowsUpgradeCost) + " gold.)\n3. Upgrade Fire-Enhanced Arrows (Requires " + str(fArrowsUpgradeCost) + " gold.)\n4. Upgrade Summon Phoenix (Fire-Enhanced skill) (Requires " + str(sPhoenixUpgradeCost) + " gold.)")
                    elif SAVE_dict['YourClass'] == "Mage":
                        print("1. Upgrade Arcane Pentagram (Requires " + str(aPentagramUpgradeCost) + " gold.)\n2. Upgrade Call of the Elements (Requires " + str(cElementsUpgradeCost) + " gold.)")
                    elif SAVE_dict['YourClass'] == "Healer":
                        print("1. Upgrade Hand of Light (Requires " + str(hLightUpgradeCost) + " gold.)\n2. Upgrade Light Hammer (Requires " + str(lHammerUpgradeCost) + " gold.)")
                    print("5. Upgrade Critical Rate (Requires " + str(criticalRateCost) + " gold.)")
                    print("6. Upgrade Maximum Weight Expansion (Requires " + str(weightExpansionCost) + " gold.)")
                    sullivan_select = input("Select one from the above: ")
                    if sullivan_select == "5":  # Critical Rate Upgrade
                        if SAVE_dict['YourGold'] >= criticalRateCost:
                            SAVE_dict['YourGold'] -= criticalRateCost
                            SAVE_dict['CriticalRate'] += 1
                            time.sleep(1)
                            print("You upgraded your Critical Rate and now its total rate is now " + str(SAVE_dict['CriticalRate']) + ".")
                            time.sleep(2)
                            SAVEGAME()
                        else:
                            print("You don't have enough gold to purchase this upgrade.\n")
                            time.sleep(1)
                    if sullivan_select == "6":  # Weight Expansion Upgrade
                        if SAVE_dict['YourGold'] >= weightExpansionCost:
                            SAVE_dict['YourGold'] -= weightExpansionCost
                            SAVE_dict['TotalWeight'] += 4
                            time.sleep(1)
                            print("You upgraded your Maximum Weight and now its in total " + str(SAVE_dict['TotalWeight']) + ".")
                            weightExpansionCost += SAVE_dict['YourLevel']
                            time.sleep(2)
                            SAVEGAME()
                        else:
                            print("You don't have enough gold to purchase this upgrade.\n")
                            time.sleep(1)
                    if SAVE_dict['YourClass'] == "Warrior":  # Warrior Upgrades
                        if sullivan_select == "1":
                            if SAVE_dict['YourGold'] >= dChargeUpgradeCost:
                                SAVE_dict['YourGold'] -= dChargeUpgradeCost
                                SKILLS_dict['dChargePower'] = SKILLS_dict['dChargePower'] + random.randint(2, 3)
                                time.sleep(1)
                                print("You upgraded Devastating Charge and now its additional power is in total " + str(SKILLS_dict['dChargePower']))
                                dChargeUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "2":
                            if SAVE_dict['YourGold'] >= sBashUpgradeCost:
                                SAVE_dict['YourGold'] -= sBashUpgradeCost
                                SKILLS_dict['sBashPower'] = SKILLS_dict['sBashPower'] + random.randint(2, 3)
                                time.sleep(1)
                                print("You upgraded Shield Bash and now its additional power is in total " + str(SKILLS_dict['sBashPower']))
                                sBashUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "3":
                            if SAVE_dict['YourGold'] >= dSlashUpgradeCost:
                                SAVE_dict['YourGold'] -= dSlashUpgradeCost
                                SKILLS_dict['dSlashPower'] = SKILLS_dict['dSlashPower'] + random.randint(2, 3)
                                time.sleep(1)
                                print("You upgraded Decapitating Slash and now its additional power is in total " + str(SKILLS_dict['dSlashPower']))
                                dSlashUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "4":
                            if SAVE_dict['YourGold'] >= sHellUpgradeCost:
                                SAVE_dict['YourGold'] -= sHellUpgradeCost
                                SKILLS_dict['sHellPower'] = SKILLS_dict['sHellPower'] + 2
                                print("You upgraded Thousand Spiritual Swords of Hell and now its additional power is in total " + str(SKILLS_dict['sHellPower']))
                                sHellUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                    elif SAVE_dict['YourClass'] == "Rogue":  # Rogue Upgrades
                        if sullivan_select == "1":
                            if SAVE_dict['YourGold'] >= bDaggerUpgradeCost:
                                SAVE_dict['YourGold'] -= bDaggerUpgradeCost
                                SKILLS_dict['bDaggerPower'] = SKILLS_dict['bDaggerPower'] + random.randint(2, 3)
                                print("You upgraded Bleeding Dagger and now its additional power is in total " + str(SKILLS_dict['bDaggerPower']))
                                bDaggerUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "2":
                            if SAVE_dict['YourGold'] >= sFangsUpgradeCost:
                                SAVE_dict['YourGold'] -= sFangsUpgradeCost
                                SKILLS_dict['sFangsPower'] = SKILLS_dict['sFangsPower'] + 2
                                print("You upgraded Shadow Fangs and now its additional power is in total " + str(SKILLS_dict['sFangsPower']))
                                sFangsUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                    elif SAVE_dict['YourClass'] == "Archer":  # Archer Upgrades
                        if sullivan_select == "1":
                            if SAVE_dict['YourGold'] >= oRollUpgradeCost:
                                SAVE_dict['YourGold'] -= oRollUpgradeCost
                                SKILLS_dict['oRollPower'] = SKILLS_dict['oRollPower'] + random.randint(2, 3)
                                print("You upgraded Offensive Roll and now its additional power is in total " + str(SKILLS_dict['oRollPower']))
                                oRollUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "2":
                            if SAVE_dict['YourGold'] >= hArrowsUpgradeCost:
                                SAVE_dict['YourGold'] -= hArrowsUpgradeCost
                                SKILLS_dict['hArrowsPower'] = SKILLS_dict['hArrowsPower'] + random.randint(2, 3)
                                print("You upgraded Hail of Arrows and now its additional power is in total " + str(SKILLS_dict['hArrowsPower']))
                                hArrowsUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "3":
                            if SAVE_dict['YourGold'] >= fArrowsUpgradeCost:
                                SAVE_dict['YourGold'] -= fArrowsUpgradeCost
                                SKILLS_dict['fArrowsPower'] = SKILLS_dict['fArrowsPower'] + random.randint(2, 3)
                                print("You upgraded Fire-Enhanced Arrows and now its additional power is in total " + str(SKILLS_dict['fArrowsPower']))
                                fArrowsUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "4":
                            if SAVE_dict['YourGold'] >= sPhoenixUpgradeCost:
                                SAVE_dict['YourGold'] -= sPhoenixUpgradeCost
                                SKILLS_dict['sPhoenixPower'] = SKILLS_dict['sPhoenixPower'] + 2
                                print("You upgraded Summon Phoenix and now its additional power is in total " + str(SKILLS_dict['sPhoenixPower']))
                                sPhoenixUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                    elif SAVE_dict['YourClass'] == "Mage":  # Mage Upgrades
                        if sullivan_select == "1":
                            if SAVE_dict['YourGold'] >= aPentagramUpgradeCost:
                                SAVE_dict['YourGold'] -= aPentagramUpgradeCost
                                SKILLS_dict['aPentagramPower'] = SKILLS_dict['aPentagramPower'] + random.randint(2, 3)
                                print("You upgraded Arcane Pentagram and now its additional power is in total " + str(SKILLS_dict['aPentagramPower']))
                                aPentagramUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "2":
                            if SAVE_dict['YourGold'] >= cElementsUpgradeCost:
                                SAVE_dict['YourGold'] -= cElementsUpgradeCost
                                SKILLS_dict['cElementsPower'] = SKILLS_dict['cElementsPower'] + 2
                                print("You upgraded Call of the Elements and now its additional power is in total " + str(SKILLS_dict['cElementsPower']))
                                cElementsUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                    elif SAVE_dict['YourClass'] == "Healer":  # Healer Upgrades
                        if sullivan_select == "1":
                            if SAVE_dict['YourGold'] >= hLightUpgradeCost:
                                SAVE_dict['YourGold'] -= hLightUpgradeCost
                                SKILLS_dict['hLightPower'] = SKILLS_dict['hLightPower'] + random.randint(2, 3)
                                print("You upgraded Hand of Light and now its additional power is in total " + str(SKILLS_dict['hLightPower']))
                                hLightUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                        if sullivan_select == "2":
                            if SAVE_dict['YourGold'] >= lHammerUpgradeCost:
                                SAVE_dict['YourGold'] -= lHammerUpgradeCost
                                SKILLS_dict['lHammerPower'] = SKILLS_dict['lHammerPower'] + 2
                                print("You upgraded lHammer and now its additional power is in total " + str(SKILLS_dict['lHammerPower']))
                                lHammerUpgradeCost += SAVE_dict['YourLevel']
                                time.sleep(2)
                                SAVEGAME()
                            else:
                                print("You don't have enough gold to purchase this upgrade.\n")
                                time.sleep(1)
                elif town_npcselect == "2":
                    if SAVE_dict['YourClass'] == "Mage":
                        print("Sullivan the Mage: You're a Mage but not yet an Archmage. But ah well, you're not strong enough. I got to be an Archmage when I was slightly older than you but boy was I strong! Every warrior in Colin's army was afraid of me, but for a good cause. Being strong is fantastic, but with great power comes great responsibility.")
                        time.sleep(7)
                    elif SAVE_dict['YourClass'] == "Archmage":
                        print("Sullivan the Mage: You finally became an Archmage I see. Now I can trust you with some ol' secrets. Did you know there's a hidden Lightspeed Gate somewhere in Masgra? Only 3 were ever made. One of them got corrupted by the Harbinger of Deadly Light, the second one broke after Higar's rage rained down upon us and the last one.. is still intact. Not many survived the Gate, but those who did.. well, find that yourself.")
                        time.sleep(10)
                    else:
                        print("Sullivan the Mage: You're not a Mage but.. I can see you got potential in you. Do you ever look at that beautiful land that hides behind the fog, far away to the North-West of here? That's Masgra. The land where kids with potential go to and unlock their Inner Strength. And by saying \"kids\" I mean people younger than me.")
                        time.sleep(8)
            elif town_npcselection == "2":
                entering_shop = mixer.Channel(0)
                print("You're walking towards Bryan the Blacksmith.")
                entering_shop.play(mixer.Sound(entering_shop_sound))
                time.sleep(2.8)
                town_npcselect = input("Bryan the Blacksmith: Hm, another one in need of my services. If you pay well, alright then.\n1. Craft weapons\n2. Talk\n3. Exit the shop\nSelect one from the above: ")
                if town_npcselect == "1":

                    if SAVE_dict['YourClass'] == "Warrior":
                        firstChoice = random.choice(lootWeapons_Warrior)
                        secondChoice = random.choice(lootWeapons_Warrior)
                        thirdChoice = random.choice(lootWeapons_Warrior)
                    elif SAVE_dict['YourClass'] == "Rogue":
                        firstChoice = random.choice(lootWeapons_Rogue)
                        secondChoice = random.choice(lootWeapons_Rogue)
                        thirdChoice = random.choice(lootWeapons_Rogue)
                    elif SAVE_dict['YourClass'] == "Archer":
                        firstChoice = random.choice(lootWeapons_Archer)
                        secondChoice = random.choice(lootWeapons_Archer)
                        thirdChoice = random.choice(lootWeapons_Archer)
                    elif SAVE_dict['YourClass'] == "Mage":
                        firstChoice = random.choice(lootWeapons_Mage)
                        secondChoice = random.choice(lootWeapons_Mage)
                        thirdChoice = random.choice(lootWeapons_Mage)

                    print("Bryan the Blacksmith: Alright, we have a " + SAVE_dict['YourClass'] + " here. Let's fetch you the list of weapons suitable for you.")
                    time.sleep(3)
                    print("Bryan the Blacksmith: Here you go.")
                    time.sleep(1)

                    print("Equipment Weight: " + str(SAVE_dict['CurrentWeight']) + "/" + str(SAVE_dict['TotalWeight']) + ".\n")
                    print("Your Weapon Power: " + str(SAVE_dict['YourWeaponPower']) + "\n")

                    first_power = random.randint((SAVE_dict['YourLevel'] + random.randint(10, 12)),(SAVE_dict['YourLevel'] + random.randint(20, 22)))
                    second_power = random.randint((SAVE_dict['YourLevel'] + random.randint(15, 17)),(SAVE_dict['YourLevel'] + random.randint(25, 27)))
                    third_power = random.randint((SAVE_dict['YourLevel'] + random.randint(20, 24)),(SAVE_dict['YourLevel'] + random.randint(30, 34)))

                    first_price = 30 * SAVE_dict['YourLevel']
                    second_price = 35 * SAVE_dict['YourLevel']
                    third_price = 50 * SAVE_dict['YourLevel']

                    first_weight = 8 + SAVE_dict['YourLevel']
                    second_weight = 11 + SAVE_dict['YourLevel']
                    third_weight = 14 + SAVE_dict['YourLevel']

                    print("1. " + firstChoice + ". Can give you Weapon Power that has " + str(first_power) + ". Requires 5 Shattered Blades, 3 Steel and " + str(first_price) + " gold.")
                    print("2. " + secondChoice + ". Can give you Weapon Power that has " + str(second_power) + ". Requires 7 Shattered Blades, 5 Steel and " + str(second_price) + " gold.")
                    print("3. " + thirdChoice + ". Can give you Weapon Power that has " + str(third_power) + ". Requires 10 Shattered Blades, 6 Steel and " + str(third_price) + " gold.")
                    forge_weapon = input("Choose one from the above or press 0 to return back to town: ")
                    if forge_weapon == "1":
                        if (SAVE_dict['CurrentWeight'] + first_weight) <= SAVE_dict['TotalWeight']:
                            if SAVE_dict['YourGold'] >= first_price and INVENTORY_dict['Shattered Blade'] >= 5 and INVENTORY_dict['Steel'] >= 3:
                                print("Bryan the Blacksmith: Ah, this is nothing but a fine weapon. Let's do this.")
                                SAVE_dict['YourGold'] -= first_price
                                INVENTORY_dict['Shattered Blade'] -= 5
                                INVENTORY_dict['Steel'] -= 3
                                print("You have equipped " + firstChoice + ".")
                                SET_dict['WeaponLevel'] = 0
                                SAVE_dict['CurrentWeight'] += first_weight
                                SAVE_dict['YourWeaponPower'] = first_power
                                SET_dict['WeaponName'] = firstChoice
                                time.sleep(1)
                                print("Equipment Weight: " + str(SAVE_dict['CurrentWeight']) + "/" + str(SAVE_dict['TotalWeight']) + ".")
                                time.sleep(1)
                        elif (SAVE_dict['CurrentWeight'] + first_weight) > SAVE_dict['TotalWeight']:
                            print("You cannot equip " + firstChoice + " because your Current Equipment Weight is " + str(SAVE_dict['CurrentWeight']) + " out of " + str(SAVE_dict['TotalWeight']) + ".")
                            time.sleep(2)
                    if forge_weapon == "2":
                        if (SAVE_dict['CurrentWeight'] + second_weight) <= SAVE_dict['TotalWeight']:
                            if SAVE_dict['YourGold'] >= second_price and INVENTORY_dict['Shattered Blade'] >= 7 and INVENTORY_dict['Steel'] >= 5:
                                print("Bryan the Blacksmith: Ah, " + secondChoice + ". A fine piece. Gimme space, let me work.")
                                SAVE_dict['YourGold'] -= second_price
                                INVENTORY_dict['Shattered Blade'] -= 7
                                INVENTORY_dict['Steel'] -= 5
                                print("You have equipped " + secondChoice + ".")
                                SET_dict['WeaponLevel'] = 0
                                SAVE_dict['CurrentWeight'] += second_weight
                                SAVE_dict['YourWeaponPower'] = second_power
                    if forge_weapon == "3":
                        if (SAVE_dict['CurrentWeight'] + third_weight) <= SAVE_dict['TotalWeight']:
                            if SAVE_dict['YourGold'] >= third_price and INVENTORY_dict['Shattered Blade'] >= 7 and INVENTORY_dict['Steel'] >= 5:
                                print("Bryan the Blacksmith: Ah, " + thirdChoice + ". A fine piece. Gimme space, let me work.")
                                SAVE_dict['YourGold'] -= third_price
                                INVENTORY_dict['Shattered Blade'] -= 10
                                INVENTORY_dict['Steel'] -= 6
                                print("You have equipped " + thirdChoice + ".")
                                SET_dict['WeaponLevel'] = 0
                                SAVE_dict['CurrentWeight'] += third_weight
                                SAVE_dict['YourWeaponPower'] = third_power
                elif town_npcselect == "2":
                    pass
            elif town_npcselection == "3":
                show_classes()
            elif town_npcselection == "4":
                show_classes()
            elif town_npcselection == "5":
                entering_shop = mixer.Channel(0)
                print("You're walking towards Bob the Craftsman.")
                entering_shop.play(mixer.Sound(entering_shop_sound))
                time.sleep(2.8)
                town_npcselect = input("Bob the Craftsman: Ah, a fine day to craft, am I right, fellow " + SAVE_dict['YourClass'] + "?\n1. Crafting Station\n2. Talk\n3. Masgra Map\n4. Exit the shop\nSelect one from the above: ")
                if town_npcselect == "1":
                    if SAVE_dict['YourLevel'] >= 2:
                        print("Bob the Craftsman: So, you chose to craft something better. Hammer time!")
                        time.sleep(1)
                        print("1. Upgrade Weapon (Requires " + str(upgradeWeaponCost) + " gold and an Enhancement Stone).")
                        bob_select = input("Select an option from the above or type 0 to go back: ")
                        if bob_select == "1":
                            if INVENTORY_dict['Enhancement Stone'] != 0:
                                if SAVE_dict['YourGold'] >= upgradeWeaponCost:
                                    SAVE_dict['YourGold'] -= upgradeWeaponCost
                                    INVENTORY_dict['Enhancement Stone'] -= 1
                                    print("Bob the Craftsman: Alright then, let's upgrade this fine " + SET_dict['WeaponName'] + ". This will take me a little bit, hang on..")
                                    time.sleep(3)
                                    print("Bob the Craftsman: This, into this..")
                                    time.sleep(4)
                                    print("Bob the Craftsman: And this, into that..")
                                    time.sleep(3)
                                    print("Bob the Craftsman: Aha! Masterpiece!")
                                    time.sleep(2)
                                    SET_dict['WeaponLevel'] += 1
                                    print("GAME: You have upgraded " + SET_dict['WeaponName'] + " to " + SET_dict['WeaponName'] + "+" + str(SET_dict['WeaponLevel']) + ".")
                                    time.sleep(2)
                                    if SET_dict['WeaponLevel'] in range(1, 4):  # Up to 3
                                        weaponPowerLevelChance = random.randint(2, 4)
                                    elif SET_dict['WeaponLevel'] in range(4, 8):  # Up to 7
                                        weaponPowerLevelChance = random.randint(4, 6)
                                    elif SET_dict['WeaponLevel'] == 8:
                                        weaponPowerLevelChance = random.randint(5, 7)
                                    elif SET_dict['WeaponLevel'] == 9:
                                        weaponPowerLevelChance = random.randint(7, 9)
                                    SAVE_dict['YourWeaponPower'] += weaponPowerLevelChance
                                    print("GAME: This gave your weapon +" + str(
                                        weaponPowerLevelChance) + " Weapon Power.")
                                    time.sleep(1)
                                    SAVEGAME()
                                else:
                                    print("Bob the Craftsman: You don't have enough gold, son. Get some more gold to bring and I'll do your bidding.")
                                    time.sleep(2)
                            else:
                                print("Bob the Craftsman: You can't upgrade your " + SET_dict['WeaponName'] + " if you don't have an Enhancement Stone.")
                                time.sleep(2)
                        if bob_select == "3":  # Craft Map
                            if CONT2_dict['MasgraMap'] == 1:
                                print("Bob the Craftsman: You already have the damn map, you dingus.")
                                time.sleep(3)
                            else:
                                if INVENTORY_dict['Upper-Left Map Piece'] != 0:
                                    print("Bob the Craftsman: There's the Upper-Left Map Piece, alright..")
                                    CONT2_dict['ULMapPiece'] = 1
                                    time.sleep(1)
                                else:
                                    print("Bob the Craftsman: Are you kidding me? You don't have the first piece, the Upper-Left Map Piece!")
                                    time.sleep(2)
                                    print("GAME: You're missing the Upper-Left Map Piece. Acquire it and then come back again.")
                                    time.sleep(2)
                                    continue
                                if INVENTORY_dict['Upper-Right Map Piece'] != 0:
                                    print("Bob the Craftsman: Upper-Right Map Piece is right here, so both Upper Pieces are here..")
                                    CONT2_dict['URMapPiece'] = 1
                                    time.sleep(2)
                                else:
                                    print("Bob the Craftsman: You're missing the second piece, the Upper-Right Map Piece, are we really gonna waste more time?")
                                    time.sleep(2)
                                    print("GAME: You're missing the Upper-Right Map Piece. Acquire it and then come back again.")
                                    time.sleep(2)
                                    continue
                                if INVENTORY_dict['Lower-Left Map Piece'] != 0:
                                    print("Bob the Craftsman: Lower-Left Map Piece, check.")
                                    CONT2_dict['LLMapPiece'] = 1
                                    time.sleep(1)
                                else:
                                    print("Bob the Craftsman: You're missing a piece here, mate. Getting it would, you know, make my job tons easier.")
                                    time.sleep(2)
                                    print("GAME: You're missing the Lower-Left Map Piece. Acquire it and then come back.")
                                    time.sleep(2)
                                    continue
                                if INVENTORY_dict['Lower-Right Map Piece'] != 0:
                                    print("Bob the Craftsman: Great, the Lower-Right Map Piece is here as well.")
                                    CONT2_dict['LRMapPiece'] = 1
                                    time.sleep(1)
                                else:
                                    print("Bob the Craftsman: The final part is missing, which is the Lower-Right Map Piece. Find it and I'll make that map for you that you so want.")
                                    time.sleep(2)
                                    print("GAME: You're missing the Lower-Right Map Piece. Acquire it and then come back.")
                                    time.sleep(2)
                                    continue
                                if CONT2_dict['ULMapPiece'] == 1 and CONT2_dict['URMapPiece'] == 1 and CONT2_dict['LLMapPiece'] == 1 and CONT2_dict['LRMapPiece'] == 1:
                                    print("Bob the Craftsman: Let us proceed then.")
                                    time.sleep(2)
                                    print("Bob the Craftsman: This will take me a bit, kid. Hold on and let me do my job.")
                                    time.sleep(5)
                                    print("Bob the Craftsman: Just.. give me a minute, I'll uh.. I'll figure it out.")
                                    time.sleep(4)
                                    print("Bob the Craftsman: Ah, there! It's ready! It's a Map of Masgra. Masgra is the continent North-West of ours and you can travel there by boat. Why don't you give that ol' boatkeeper Matthew a visit? I'm sure he knows better than I do.")
                                    time.sleep(2)
                                    CONT2_dict['MasgraMap'] = 1
                    else:
                        print("Bob the Craftsman: Hmm.. it seems like you're not strong enough to even carry a blade. Get stronger, kiddo.")
                        time.sleep(1)
                        print("GAME: You have to be Level 2 and above to use the Crafting Station.")
                        time.sleep(2)
            elif town_npcselection == "6":
                entering_shop = mixer.Channel(0)
                print("You're walking towards Colin the Captain.")
                entering_shop.play(mixer.Sound(entering_shop_sound))
                time.sleep(2.8)
                town_npcselect = input("Colin the Captain: Hello young lad, make it quick as I'm busy right now.\n1. Quest\n2. Talk\n3. Exit\nSelect one from the above: ")
                if town_npcselect == "1":
                    if SAVE_dict['YourLevel'] >= 2:
                        if QUESTS_dict['active1'] == 0:
                            print("Colin the Captain: Alright then, you want to make my day? As my soldiers do not meet my needs anymore these days, I'll ask it from you. Go and kill 10 Black Ninjas outside the town and I'll award you greatly for your efforts.")
                            QUESTS_dict['active1'] = 1
                            time.sleep(2)
                            print("You have acquired a Story Quest: Kill 10 Black Ninjas.")
                            time.sleep(1)
                            SAVEGAME()
                        elif QUESTS_dict['active1'] == 1:
                            print("Colin the Captain: I've already given you my orders, lad. Go and do as I told you, don't waste more of my time.")
                            time.sleep(2)
                    elif SAVE_dict['YourLevel'] < 2:
                        print("Colin the Captain: Sorry boy, you're not strong enough yet to follow my orders.")
                        time.sleep(2)
                        print("GAME: This Story Quest requires you to be Level 2 and above.")
                        time.sleep(1)
                    if QUESTS_dict['active1'] == 2:
                        if SAVE_dict['YourLevel'] >= 4:
                            print("Colin the Captain: So, I see you've gotten stronger now and you succesfully completed my last mission. As an extra bonus, you didn't waste my time, that's always a plus. Now, " +SAVE_dict['YourName'] + ", I want you to go kill 5 White Ninjas for me. They've been setting up ambushes all around the towns and they always scare the citizens. Pricks.. You'll be rewarded for your efforts, just go.")
                            time.sleep(3)
                            QUESTS_dict['active2'] = 1
                            print("You have acquired a Story Quest: Kill 5 White Ninjas.")
                            time.sleep(1)
                            SAVEGAME()
                        elif QUESTS_dict['active2'] == 1:
                            print("Colin the Captain: Boy, don't waste my time. I'm busy enough to keep my own thoughts in my head, so just go.")
                            time.sleep(2)
                        elif SAVE_dict['YourLevel'] < 4:
                            print("Colin the Captain: You're not strong enough for my next task. Get stronger and then come meet me again.")
                            time.sleep(2)
                            print("GAME: This Story Quest requires you to be Level 4 and above.")
                            time.sleep(1)
                elif town_npcselect == "2":
                    if SAVE_dict['YourLevel'] == 1:
                        print("Colin the Captain: What? You want me to make you a cup of tea and tell you a story? How about you just SCRAM, kid.")
                    elif SAVE_dict['YourLevel'] == 2:
                        print("Colin the Captain: Say.. you're quite doing well for yourself, aren't you? Keep it up and you might just make it through the ranks.")

                    time.sleep(3)
                elif town_npcselect == "3":
                    pass
            elif town_npcselection == "7":
                show_classes()
            elif town_npcselection == "8":
                show_classes()
            elif town_npcselection == "9":
                SAVEGAME()
            elif town_npcselection == "10":
                mixer.music.load(harbor_ambient)
                mixer.music.fadeout(1000)
                mixer.music.play(-1)
                print("You're walking towards Matthew the Boatskeeper..")
                if SAVE_dict['YourLevel'] >= 10 and CONT2_dict['TravelledCONT2'] == 0:
                    if SAVE_dict['YourGold'] >= 250 and CONT2_dict['MasgraMap'] == 1:
                        print("Matthew the Boatskeeper: Hmm.. I see. You want to head out to the North, ay? I see you're a strong fighter but that's for our standards only, mate. Over there lie enemies much stronger than you are and sometimes even fight in packs, the whole place sounds terrifying to new adventurers and fighters but you.. I fear not that you will succeed. You might even make some friends, who knows, ay?")
                        time.sleep(4)
                        travel_cont2 = input("Matthew the Boatskeeper: So, ya ready?")
                        if travel_cont2 == "Y" or travel_cont2 == "y":
                            mixer.music.fadeout(1000)
                            time.sleep(0.3)
                            print("Matthew the Boatskeeper: Alright then, let's go.")
                            SAVE_dict['YourGold'] -= 250
                            mixer.music.load(seastorm)
                            time.sleep(1)
                            print("Matthew the Boatskeeper: This trip might be a bit long so how about ya take a nap or somethin'?")
                            time.sleep(2)
                            mixer.music.play(-1)
                            time.sleep(55)
                            mixer.music.fadeout(2900)
                            time.sleep(2.1)
                            print("Matthew the Boatskeeper: Ay, " + SAVE_dict['YourClass'] + ", wake up. We're here, at Masgra. Off you go lad and best of luck to you. May the Gods turn a blind eye to your actions.")
                            CONT2_dict['TravelledCONT2'] = 1
                            CONT2_dict['AtMasgra'] = 1
                            time.sleep(4)
                            SAVEGAME()
                            exitBoat()


                        elif travel_cont2 == "N" or travel_cont2 == "n":
                            print("Matthew the Boatskeeper: I see. Not ready yet or made ya scared? Either way, take your time.\n")
                            time.sleep(2)
                            mixer.music.fadeout(1300)
                            mixer.music.load(town_ambient)
                            mixer.music.play(-1)
                    elif SAVE_dict['YourGold'] < 250:
                        print("Matthew the Boatskeeper: Got no gold to pay ol' Matthew? Ah, ye bastard. Come back when you got enough gold, ay?\n")
                        time.sleep(2)
                        mixer.music.fadeout(1300)
                        mixer.music.load(town_ambient)
                        mixer.music.play(-1)
                    elif SAVE_dict['YourGold'] >= 250 and CONT2_dict['MasgraMap'] == 0:
                        print("Matthew the Boatskeeper: You got the gold there buddy, but a map? You don't have a map? I may be a captain but I don't need to have a map, yer donkey!\n")
                        time.sleep(2)
                        mixer.music.fadeout(1300)
                        mixer.music.load(town_ambient)
                        mixer.music.play(-1)

                elif SAVE_dict['YourLevel'] < 10:
                    print("Matthew the Boatskeeper: Where do you think YOU are going? You're a fiddle, mate, get back to yer training boy.\n")
                    time.sleep(3)
                    mixer.music.fadeout(1300)
                    mixer.music.load(town_ambient)
                    mixer.music.play(-1)
                elif CONT2_dict['TravelledCONT2'] == 1:
                    if SAVE_dict['YourGold'] >= 250:
                        travel_backcont2 = input("Matthew the Boatskeeper: Going back to Masgra? [Y/N]: ")
                        if travel_backcont2 == "Y" or travel_backcont2 == "y":
                            print("Matthew the Boatskeeper: Okay, travelling back to Masgra ay? Hop on matey, we got seas to slice!")
                            mixer.music.fadeout(1000)
                            time.sleep(0.3)
                            print("Matthew the Boatskeeper: You know the drill, lay back and relax, take a nap while you're at it, ay. Captain Matthew on the steering wheel!")
                            SAVE_dict['YourGold'] -= 250
                            mixer.music.load(seastorm)
                            mixer.music.play(-1)
                            time.sleep(55)
                            mixer.music.fadeout(2900)
                            time.sleep(2.1)
                            print("Matthew the Boatskeeper: Land ho, " + SAVE_dict['YourClass'] + ". Best of luck to your journey.")
                            CONT2_dict['AtMasgra'] = 1
                            time.sleep(3)
                            SAVEGAME()
                            exitBoat()
                        elif travel_backcont2 == "N" or travel_backcont2 == "n":
                            print("Matthew the Boatskeeper: Okay then, I'll be here when you're ready mate, take yer damn time.\n")
                            time.sleep(2)
                            mixer.music.fadeout(1300)
                            mixer.music.load(town_ambient)
                            mixer.music.play(-1)

            elif town_npcselection == "11":
                print("You walk towards the Town Hall's magic wall..")
                time.sleep(2)
                print("Level: " + str(SAVE_dict['YourLevel']))
                print("Current EXP: " + str(round(SAVE_dict['YourExp'], 2)))
                print("Max Health: " + str(SAVE_dict['YourHealth']))
                print("Max Mana: " + str(SAVE_dict['YourMana']))
                print("Weapon Power: " + str(SAVE_dict['YourWeaponPower']))
                print("Armor: " + str(SAVE_dict['YourArmor']))
                print("Your Gold: " + str(SAVE_dict['YourGold']))
                print("Current Equipment Weight: " + str(SAVE_dict['CurrentWeight']) + " out of " + str(SAVE_dict['TotalWeight']))
                print("Weapon Equipped: " + SET_dict['WeaponName'])
                print("Armor Equipped: " + SET_dict['ArmorName'])
                if QUESTS_dict['active1'] == 1:
                    print("Active Quests: Kill 10 Black Ninjas, progress " + str(QUESTS_dict['killed10BN']) + "/10 Black Ninjas.")
                elif QUESTS_dict['active2'] == 1:
                    print("Active Quests: Kill 5 White Ninjas, progress " + str(QUESTS_dict['killed5WN']) + "/5 White Ninjas.")
                print("Your Inventory: " + str(INVENTORY_dict))
                print("Times Visited Town: " + str(SAVE_dict['times_VisitedTown']))
                print("Enemies Killed: " + str(SAVE_dict['EnemiesKilled']))
                print("Times died: " + str(SAVE_dict['TimesDied']))
                print("Total Gold Acquired: " + str(SAVE_dict['TotalGoldAcquired']))
                print("Achivements Completed: " + str(ACHIEVEMENTS_dict['AchievementsCompleted']) + "/10")
                time.sleep(6)
            elif town_npcselection == "0":
                time.sleep(0.5)
                break
            else:
                print("You exited the town as a punishment for not selecting from one of the options specified.")
                time.sleep(2)
                break
    elif CONT2_dict['AtMasgra'] == 1:  # If at Masgra, enter here
        for town2_safeturns in range(1, 4):
            show_npcnames2()
            print("SAFE Turn: " + str(town2_safeturns))
            town2_npcselection = input("Select one to meet from the above: ")
            if town2_npcselection == "1":
                pass
            elif town2_npcselection == "2":
                pass
            elif town2_npcselection == "3":
                pass
            elif town2_npcselection == "4":
                pass
            elif town2_npcselection == "5":
                pass
            elif town2_npcselection == "6":
                pass
            elif town2_npcselection == "7":
                pass
            elif town2_npcselection == "8":
                pass
            elif town2_npcselection == "9":
                print("You walk towards the gate of Higar's Arena..")

            elif town2_npcselection == "10":
                pass
            elif town2_npcselection == "11":
                pass
            elif town2_npcselection == "12":
                pass
            elif town2_npcselection == "13":
                select_leaderboard = input("View Level leaderboard or view Golden Diamonds leaderboard? [1/2]: ")
                if select_leaderboard == "1":
                    cursor.execute("SELECT CHARACTER_NAME, LEVEL FROM ACCOUNTS ORDER BY LEVEL DESC")
                    results = cursor.fetchall()
                    for row in results:
                        charname = row[0]
                        charlevel = row[1]
                        print("LEVEL - GLOBAL LEADERBOARD - DESCENDING ORDER")
                        time.sleep(1)
                        print("Name: " + charname + " -|- Level: " + str(charlevel))
                elif select_leaderboard == "2":
                    cursor.execute("SELECT CHARACTER_NAME, BALANCE FROM ACCOUNTS ORDER BY BALANCE DESC")
                    results = cursor.fetchall()
                    for row in results:
                        charname = row[0]
                        charbalance = row[1]
                        print("GOLDEN DIAMONDS - GLOBAL LEADERBOARD - DESCENDING ORDER")
                        time.sleep(1)
                        print("Name: " + charname + " -|- Golden Diamonds: " + str(charbalance))
                leave_leaderboard = input("Done? (Press ENTER): ")
                time.sleep(1)
            elif town2_npcselection == "0":
                time.sleep(2)
                break
            else:
                print("You exited the town as a punishment for not selecting from one of the options specified.")
                time.sleep(2)
                break

    print("\nYou exited the town.\n")
    mixer.music.fadeout(1000)
    SAVE_dict['InTown'] = 0
    time.sleep(1)
    Weather()  # Weather System
    enemyChance()


def blockType_function():
    global SAVE_dict
    global CONT2_dict
    if SAVE_dict['InTown'] == 1:
        if not SAVE_dict['CurrentTownName']:
            SAVE_dict['CurrentTownName'] = random.choice(town_names)
            print("You just entered " + SAVE_dict['CurrentTownName'] + ". The next 3 turns are SAFE")
            blockType_Safe()
        else:
            print("You just entered " + SAVE_dict['CurrentTownName'] + ". The next 3 turns are SAFE")
            blockType_Safe()
    if SAVE_dict['InTown'] == 1 and CONT2_dict['TravelledCONT2'] == 1:  # --------------------------------------------- S E C O N D . C O N T I N E N T . N A M E S . ----------------------------------------------
        if not SAVE_dict['CurrentTownName']:
            SAVE_dict['CurrentTownName'] = random.choice(town_names_CONT2)
            print("You just entered " + SAVE_dict['CurrentTownName'] + ". The next 3 turns are SAFE")
            blockType_Safe()


def combat():
    global playerHealth
    global enemyHealth
    global manaPoints
    global enemy_isAlert
    global gold
    global game_class
    global bossBattle
    global e_weaponPower
    enemyAlive = 1
    yourTurn = 1
    playerHealth = SAVE_dict['YourHealth']
    manaPoints = SAVE_dict['YourMana']
    armorPoints = SAVE_dict['YourArmor']
    boss_weaponPower = ((SAVE_dict['YourLevel'] * 5) + (SAVE_dict['YourLevel'] + random.randint(3, 5))) / 1.6
    critical = random.randint(1, 130)
    if config.get('General', 'music') == "On":
        mixer.music.load(combat_music)
        mixer.music.play(-1)
    else:
        mixer.music.stop()
    while enemyAlive == 1:
        while yourTurn == 1:
            if SAVE_dict['YourClass'] == "Warrior":  # WARRIOR CLASS
                show_warriorskills()
                print("5. Normal Attack\n")
                print("Your HP: " + str(playerHealth) + "\nEnemy HP: " + str(enemyHealth))
                print("Mana: " + str(manaPoints))
                skill_selection = input("Select a skill from the above: ")
                if skill_selection == "1":
                    if manaPoints >= 5 and SAVE_dict['ShieldEquipped'] == 1:
                        manaPoints -= 5
                        print("Devastating Charge!")
                        time.sleep(1)
                        dc_damage = ((SAVE_dict['YourWeaponPower'] + (SAVE_dict['YourLevel'] * 1.55)) + random.randint(1, 5)) + SKILLS_dict['dChargePower']  # Devastating Charge damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            dc_critical = dc_damage * 2
                            print("You deal " + str(round(dc_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= dc_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            dc_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(dc_damage, 3)) + " damage.")
                            enemyHealth -= dc_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana and/or you don't have a shield equipped.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "2":
                    if manaPoints >= 10 and SAVE_dict['ShieldEquipped'] == 1:
                        manaPoints -= 10
                        print("Shield Bash!")
                        time.sleep(1)
                        sb_damage = ((SAVE_dict['YourWeaponPower'] + 2) + (SAVE_dict['YourLevel'] * 2) + random.randint(2, 6)) + SKILLS_dict['sBashPower']  # Shield Bash damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            sb_critical = sb_damage * 2
                            print("You deal " + str(round(sb_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= sb_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            sb_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(sb_damage, 3)) + " damage.")
                            enemyHealth -= sb_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana and/or you don't have a shield equipped.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "3":
                    if manaPoints >= 20:
                        manaPoints -= 20
                        print("Decapitating Slash!")
                        time.sleep(1)
                        ds_damage = ((SAVE_dict['YourWeaponPower'] + 3) + (SAVE_dict['YourLevel'] * 1.8) + random.randint(4, 13)) + SKILLS_dict['dSlashPower']  # Decapitating Slash damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            ds_critical = ds_damage * 2
                            print("You deal " + str(round(ds_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= ds_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            ds_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(ds_damage, 3)) + " damage.")
                            enemyHealth -= ds_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "4":
                    if manaPoints >= 60:
                        manaPoints -= 60
                        print("Thousand Spiritual Swords of Hell!")
                        time.sleep(1)
                        tssoh_damage = ((SAVE_dict['YourWeaponPower'] + 10) + (SAVE_dict['YourLevel'] * 2) + random.randint(9, 22) + 7) + SKILLS_dict['sHellPower']  # Thousand Spiritual Swords of Hell damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            tssoh_critical = tssoh_damage * 2
                            print("You deal " + str(round(tssoh_critical, 3)) + " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= tssoh_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            tssoh_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(tssoh_damage, 3)) + " damage.")
                            enemyHealth -= tssoh_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "5":
                    print("Normal Attack!")
                    time.sleep(1)
                    na_damage = SAVE_dict['YourWeaponPower'] + random.randint(1, 3)
                    if critical in range(1, SAVE_dict['CriticalRate']):
                        na_critical = na_damage * 2
                        print("You deal " + str(round(na_critical, 3)) * " damage.")
                        time.sleep(1)
                        print("Critical Hit!")
                        enemyHealth -= na_critical
                        print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                        time.sleep(1)
                        na_critical = 0
                        yourTurn = 0
                    else:
                        print("You deal " + str(round(na_damage, 3)) + " damage.")
                        enemyHealth -= na_damage
                        print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                        time.sleep(1)
                        yourTurn = 0
                else:
                    print("You skipped your turn for not selecting from one of the options specified.\n")
                    time.sleep(1)
                    yourTurn = 0

            elif SAVE_dict['YourClass'] == "Rogue":  # ROGUE CLASS
                if enemy_isAlert == 1:  # If Rogue is in Stealthed state, do the following
                    show_stealthed_rogueskills()
                    print("3. Normal/Ambush Attack - This Normal Attack is SPECIAL because you're in Stealthed state.\n")
                    print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                    print("Mana: " + str(manaPoints))
                    skill_selection = input("Select a skill from the above: ")
                    if skill_selection == "1":
                        if manaPoints >= 10:
                            manaPoints -= 10
                            skill_selection = ""
                            print("Backstab!")
                            time.sleep(1)
                            backstab_damage = (SAVE_dict['YourWeaponPower'] + random.randint(4, 11)) + random.randint(3,9) + 2  # Backstab damage calculation
                            if critical in range(1, SAVE_dict['CriticalRate']):
                                backstab_critical = backstab_damage * 2
                                print("You deal " + str(round(backstab_critical, 3)) * " damage.")
                                time.sleep(1)
                                print("Critical Hit!")
                                enemyHealth -= backstab_critical
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                backstab_critical = 0
                                yourTurn = 0
                            else:
                                print("You deal " + str(round(backstab_damage, 3)) + " damage.")
                                enemyHealth -= backstab_damage
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                yourTurn = 0
                            enemy_isAlert = 0
                        else:
                            print("You don't have enough mana.\n")
                            time.sleep(1)
                            continue
                    elif skill_selection == "2":
                        if manaPoints >= 25:
                            manaPoints -= 25
                            print("Swift Assault!")
                            time.sleep(1)
                            ss_damage = (SAVE_dict['YourWeaponPower'] + random.randint(5, 12) + random.randint(5,9)) + (SAVE_dict['YourLevel'] * 1.66) / 0.3 + 3  # Swift Assault damage calculation
                            if critical in range(1, SAVE_dict['CriticalRate']):
                                ss_critical = ss_damage * 2
                                print("You deal " + str(round(ss_critical, 3)) * " damage.")
                                time.sleep(1)
                                print("Critical Hit!")
                                enemyHealth -= ss_critical
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                ss_critical = 0
                                yourTurn = 0
                            else:
                                print("You deal " + str(round(ss_damage, 3)) + " damage.")
                                enemyHealth -= ss_damage
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                yourTurn = 0
                            enemy_isAlert = 0
                        else:
                            print("You don't have enough mana.\n")
                            time.sleep(1)
                            continue
                    elif skill_selection == "3":
                        print("Ambush Attack!")
                        time.sleep(1)
                        ambush_damage = (SAVE_dict['YourWeaponPower'] + random.randint(1, 3)) + random.randint(1,4)  # Ambush Attack damage calculation (Normal Attack but SPECIAL)
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            ambush_critical = ambush_damage * 2
                            print("You deal " + str(round(ambush_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= ambush_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            ambush_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(ambush_damage, 3)) + " damage.")
                            enemyHealth -= ambush_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                        enemy_isAlert = 0


                else:  # If Rogue isn't in Stealthed state, do the following
                    show_rogueskills()
                    print("5. Normal Attack\n")
                    print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                    print("Mana: " + str(manaPoints))
                    skill_selection = input("Select a skill from the above: ")
                    if skill_selection == "1":
                        if manaPoints >= 10:
                            manaPoints -= 10
                            print("You become one with the shadows of the environment around you.")
                            time.sleep(1)
                            yourTurn = 0
                        else:
                            print("You don't have enough mana.\n")
                            time.sleep(1)
                            continue
                    elif skill_selection == "2":
                        if manaPoints >= 10:
                            manaPoints -= 10
                            print("Bleeding Dagger!")
                            time.sleep(1)
                            bd_damage = ((SAVE_dict['YourWeaponPower'] + 4) + (SAVE_dict['YourLevel'] * 2) + random.randint(3, 7) + 3) + SKILLS_dict['bDaggerPower']  # Bleeding Dagger damage calculation
                            if critical in range(1, SAVE_dict['CriticalRate']):
                                bd_critical = bd_damage * 2
                                print("You deal " + str(round(bd_critical, 3)) + " damage.")
                                time.sleep(1)
                                print("Critical Hit!")
                                enemyHealth -= bd_critical
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                bd_critical = 0
                                yourTurn = 0
                            else:
                                print("You deal " + str(round(bd_damage, 3)) + " damage.")
                                enemyHealth -= bd_damage
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                yourTurn = 0
                        else:
                            print("You don't have enough mana.\n")
                            time.sleep(1)
                            continue
                    elif skill_selection == "3":  # R   E   W   O   R   K     -   -   -   -
                        if manaPoints >= 15:
                            manaPoints -= 15
                            print("Dangerous Game!")
                            time.sleep(1)
                            dgame_chance = random.randint(1, 100)
                            if dgame_chance in range(1, 21):
                                print("Dangerous Game activates \"Venom Taste of Steel\"!")
                                dgame1_damage = ((SAVE_dict['YourWeaponPower'] + SAVE_dict['YourLevel']) + random.randint(4, 6)) * random.randint(2, 3)
                                time.sleep(1)
                                if critical in range(1, SAVE_dict['CriticalRate']):
                                    dgame1_critical = dgame1_damage * 2
                                    print("You deal " + str(round(dgame1_critical, 3)) + " damage.")
                                    time.sleep(1)
                                    print("Critical Hit!")
                                    enemyHealth -= dgame1_critical
                                    print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                    time.sleep(1)
                                    dgame1_critical = 0
                                    yourTurn = 0
                                else:
                                    print("You deal " + str(round(dgame1_damage, 3)) + " damage.")
                                    enemyHealth -= dgame1_damage
                                    print("Your HP: " + str(round(playerHealth, 3)) + " \nEnemy HP: " + str(round(enemyHealth, 3)))
                                    time.sleep(1)
                                    yourTurn = 0
                            elif dgame_chance in range(21, 66):
                                print("Dangerous Game activates \"Bloody Crystal Blade\"!")
                                dgame2_damage = (SAVE_dict['YourWeaponPower'] + SAVE_dict['YourLevel']) * random.randint(1, 3)
                                bcb_chance = random.randint(1, 3)
                                time.sleep(1)
                                if bcb_chance == 1:
                                    bcb1_damage1 = dgame2_damage + random.randint(1, 3)
                                    print("You attack " + currentEnemyName + " with " + str(bcb1_damage1) + " damage.")
                                    enemyHealth -= bcb1_damage1
                                    time.sleep(1)
                                    bcb1_damage2 = dgame2_damage + random.randint(1, 5)
                                    print("You attack YOURSELF with " + str(bcb1_damage2) + " damage.")
                                    playerHealth -= bcb1_damage2 - (armorPoints / 5)
                                    time.sleep(1)
                                    bcb1_damage3 = dgame2_damage + random.randint(1, 7)
                                    print("You attack " + currentEnemyName + " with " + str(bcb1_damage3) + " damage.")
                                    enemyHealth -= bcb1_damage3
                                    time.sleep(1)
                                    print("Your HP: " + str(round(playerHealth, 3)) + " \nEnemy HP: " + str(round(enemyHealth, 3)))
                                    time.sleep(1)
                                    yourTurn = 0
                                elif bcb_chance == 2:
                                    bcb2_damage1 = dgame2_damage + random.randint(1, 3)
                                    print("You attack YOURSELF with " + str(bcb2_damage1) + " damage.")
                                    playerHealth -= bcb2_damage1 - (armorPoints / 5)
                                    time.sleep(1)
                                    bcb2_damage2 = dgame2_damage + random.randint(1, 3)
                                    print("You attack YOURSELF with " + str(bcb2_damage2) + " damage.")
                                    playerHealth -= bcb2_damage2 - (armorPoints / 5)
                                    time.sleep(1)
                                    bcb2_damage3 = dgame2_damage + random.randint(1, 16)
                                    print("You attack " + currentEnemyName + " with " + str(bcb2_damage3) + " damage.")
                                    enemyHealth -= bcb2_damage3
                                    time.sleep(1)
                                    print("Your HP: " + str(round(playerHealth, 3)) + " \nEnemy HP: " + str(round(enemyHealth, 3)))
                                    time.sleep(1)
                                    yourTurn = 0
                                elif bcb_chance == 3:
                                    bcb3_damage1 = dgame2_damage + random.randint(1, 14)
                                    print("You attack YOURSELF with " + str(bcb3_damage1) + " damage.")
                                    playerHealth -= bcb3_damage1 - (armorPoints / 5)
                                    time.sleep(1)
                                    bcb3_damage2 = dgame2_damage + random.randint(4, 17)
                                    print("You attack " + currentEnemyName + " with " + str(bcb3_damage2) + " damage.")
                                    enemyHealth -= bcb3_damage2
                                    time.sleep(1)
                                    print("Your HP: " + str(round(playerHealth, 3)) + " \nEnemy HP: " + str(round(enemyHealth, 3)))
                                    time.sleep(1)
                                    yourTurn = 0
                            elif dgame_chance in range(66, 100):
                                print("Dangerous Game activates \"Dagger Blossom\"!")
                                dgame3_damage1 = SAVE_dict['YourWeaponPower'] + random.randint(1, 11)
                                time.sleep(1)
                                print("You attack " + currentEnemyName + " with " + str(dgame3_damage1) + " damage.")
                                enemyHealth -= dgame3_damage1
                                time.sleep(1)
                                print("Your HP: " + str(round(playerHealth, 3)) + " \nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                yourTurn = 0
                            elif dgame_chance == 100:
                                print("Dangerous Game activates \"Spacetime Slash\"!")
                                dgame4_damage = enemyHealth / random.uniform(2.90, 3.20)
                                time.sleep(1)
                                print("You attack " + currentEnemyName + " with " + str(round(dgame4_damage, 3)) + " damage.")
                                enemyHealth -= dgame4_damage
                                time.sleep(1)
                                print("Your HP: " + str(round(playerHealth, 3)) + " \nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                yourTurn = 0
                        else:
                            print("You don't have enough mana.\n")
                            time.sleep(1)
                            continue
                    elif skill_selection == "4":
                        if manaPoints >= 70:
                            manaPoints -= 70
                            print("Shadow Fangs!")
                            time.sleep(1)
                            sf_damage_first = ((SAVE_dict['YourWeaponPower'] + 8) + (SAVE_dict['YourLevel'] * 2) + random.randint(6, 18) + 3) + SKILLS_dict['sFangsPower']  # 1st Shadow Fangs damage calculation
                            print("You deal " + str(round(sf_damage_first, 3)) + " damage.")
                            time.sleep(1)
                            enemyHealth -= sf_damage_first
                            sf_damage_second = ((SAVE_dict['YourWeaponPower'] + 7) + (SAVE_dict['YourLevel'] * 2) + random.randint(4, 15) + 3) + SKILLS_dict['sFangsPower']  # 2nd Shadow Fangs damage calculation
                            print("You deal " + str(round(sf_damage_second, 3)) + " damage.")
                            time.sleep(1)
                            enemyHealth -= sf_damage_second
                            sf_damage_sum = sf_damage_first + sf_damage_second
                            if critical in range(1, SAVE_dict['CriticalRate']):
                                sf_critical = sf_damage_sum * 2
                                print("You deal " + str(round(sf_critical, 3)) * " damage.")
                                time.sleep(1)
                                print("Critical Hit!")
                                enemyHealth -= sf_critical
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                sf_critical = 0
                                yourTurn = 0
                            else:
                                print("You deal " + str(round(sf_damage_sum, 3)) + " damage.")
                                enemyHealth -= sf_damage_sum
                                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                                time.sleep(1)
                                yourTurn = 0
                        else:
                            print("You don't have enough mana.\n")
                            time.sleep(1)
                            continue
                    elif skill_selection == "5":
                        print("Normal Attack!")
                        time.sleep(1)
                        na_damage = SAVE_dict['YourWeaponPower'] + random.randint(1, 3)
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            na_critical = na_damage * 2
                            print("You deal " + str(round(na_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= na_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            na_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(na_damage, 3)) + " damage.")
                            enemyHealth -= na_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You skipped your turn for not selecting from one of the options specified.\n")
                        time.sleep(1)
                        yourTurn = 0

            elif SAVE_dict['YourClass'] == "Archer":  # ARCHER CLASS
                show_archerskills()
                print("5. Normal Attack\n")
                print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                print("Mana: " + str(manaPoints))
                skill_selection = input("Select a skill from the above: ")
                if skill_selection == "1":
                    if manaPoints >= 5:
                        manaPoints -= 5
                        print("Offensive Roll!")
                        time.sleep(1)
                        of_damage = ((SAVE_dict['YourWeaponPower'] + SAVE_dict['YourLevel'] * 1.55) + random.randint(1,5)) + SKILLS_dict['oRollPower']  # Offensive Roll damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            of_critical = of_damage * 2
                            print("You deal " + str(round(of_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= of_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            of_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(of_damage, 3)) + " damage.")
                            enemyHealth -= of_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "2":
                    if manaPoints >= 10:
                        manaPoints -= 10
                        print("Hail of Arrows!")
                        time.sleep(1)
                        hoa_damage = ((SAVE_dict['YourWeaponPower'] + SAVE_dict['YourLevel'] * 2) + random.randint(3,9) + 1) + SKILLS_dict['hArrowsPower']  # Hail of Arrows damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            hoa_critical = hoa_damage * 2
                            print("You deal " + str(round(hoa_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= hoa_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            hoa_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(hoa_damage, 3)) + " damage.")
                            enemyHealth -= hoa_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "3":
                    if manaPoints >= 20:
                        manaPoints -= 20
                        print("Fire-Enhanced Arrows!")
                        fireenhanced = 1
                        time.sleep(1)
                        fea_damage = ((SAVE_dict['YourWeaponPower'] + SAVE_dict['YourLevel'] * 2) + random.randint(2,6) / 0.2 + 3) + SKILLS_dict['fArrowsPower']  # Fire-Enhanced Arrows damage calculation
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            fea_critical = fea_damage * 2
                            print("You deal " + str(round(fea_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= fea_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            fea_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(fea_damage, 3)) + " damage.")
                            enemyHealth -= fea_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "4":
                    if manaPoints >= 60:
                        manaPoints -= 60
                        print("Triple Offensive Roll!")
                        time.sleep(1)
                        tor1_damage = (SAVE_dict['YourWeaponPower'] + (SAVE_dict['YourLevel'] * 1.55) + random.randint(1, 5)) + 2  # 1st Offensive Roll damage calculation
                        print("First Offensive Roll: " + str(tor1_damage))
                        time.sleep(1)
                        tor2_damage = (SAVE_dict['YourWeaponPower'] + (SAVE_dict['YourLevel'] * 1.55) + random.randint(1, 5)) + 2  # 2nd Offensive Roll damage calculation
                        print("Second Offensive Roll: " + str(tor2_damage))
                        time.sleep(1)
                        tor3_damage = (SAVE_dict['YourWeaponPower'] + (SAVE_dict['YourLevel'] * 1.5) + random.randint(1,4)) + 1  # 3rd Offensive Roll damage calculation
                        print("Third Offensive Roll: " + str(tor3_damage))
                        tor_damagesum = tor1_damage + tor2_damage + tor3_damage
                        if critical in range(1, SAVE_dict['CriticalRate']):
                            tor_critical = tor_damagesum * 2
                            print("You deal " + str(round(tor_critical, 3)) * " damage.")
                            time.sleep(1)
                            print("Critical Hit!")
                            enemyHealth -= tor_critical
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            tor_critical = 0
                            yourTurn = 0
                        else:
                            print("You deal " + str(round(tor_damage, 3)) + " damage.")
                            enemyHealth -= tor_damage
                            print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                            time.sleep(1)
                            yourTurn = 0
                    else:
                        print("You don't have enough mana.\n")
                        time.sleep(1)
                        continue
                elif skill_selection == "5":
                    print("Normal Attack!")
                    time.sleep(1)
                    na_damage = SAVE_dict['YourWeaponPower'] + random.randint(1, 3)
                    if critical in range(1, SAVE_dict['CriticalRate']):
                        na_critical = na_damage * 2
                        print("You deal " + str(round(na_critical, 3)) * " damage.")
                        time.sleep(1)
                        print("Critical Hit!")
                        enemyHealth -= na_critical
                        print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                        time.sleep(1)
                        na_critical = 0
                        yourTurn = 0
                    else:
                        print("You deal " + str(round(na_damage, 3)) + " damage.")
                        enemyHealth -= na_damage
                        print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                        time.sleep(1)
                        yourTurn = 0
                else:
                    print("You skipped your turn for not selecting from one of the options specified.\n")
                    time.sleep(1)
                    yourTurn = 0

            elif SAVE_dict['YourClass'] == "Mage":  # MAGE CLASS
                show_mageskills()
                print("Mana: " + str(manaPoints))
                skill_selection = input("Select a skill from the above: ")

            elif SAVE_dict['YourClass'] == "Healer":  # HEALER CLASS
                show_healerskills()
                print("Mana: " + str(manaPoints))
                skill_selection = input("Select a skill from the above: ")

            if enemyHealth <= 0:  # If the enemy you're fighting dies, do this
                enemyAlive = 0
                gold_gained = 0
                if SAVE_dict['YourLevel'] in range(1, 4):  # Until Level 3
                    gold_gained = random.randint(5, 10)
                elif SAVE_dict['YourLevel'] in range(4, 9):  # Until Level 8
                    gold_gained = random.randint(6, 12)
                elif SAVE_dict['YourLevel'] in range(9, 16):  # Until Level 15
                    gold_gained = random.randint(8, 14)
                elif SAVE_dict['YourLevel'] in range(16, 31):  # Until Level 30
                    gold_gained = random.randint(11, 20)
                elif SAVE_dict['YourLevel'] == 30:
                    gold_gained = random.randint(13, 21)
                SAVE_dict['YourGold'] += gold_gained
                SAVE_dict['TotalGoldAcquired'] += gold_gained
                print("\nYou gained " + str(gold_gained) + " Gold.")
                SAVE_dict['EnemiesKilled'] += 1
                mixer.music.fadeout(1300)
                lootChance()
                expGain()
                continueOrTown()

            if enemyHealth <= 0 and playerHealth <= 0:  # If both enemy and player died, do this
                enemyAlive = 0
                print("GAME: Both combatants died, therefore you do not lose any gold.")
                mixer.music.fadeout(1300)
                time.sleep(1)
                SAVEGAME()
                time.sleep(1)
                SAVE_dict['TimesDied'] += 1
                SAVE_dict['InTown'] = 1
                print("\n" * 5)  # Clear screen
                blockType_function()
                break

            if enemyHealth <= 0 and currentEnemyName == "Harbringer of Deadly Light":
                harbringer_phase2 = 1
                print(currentEnemyName + ": " + random.choice(harbringer_death1_quotes))
                time.sleep(4)

        while yourTurn == 0 and enemyAlive == 1:  # If it's no longer your turn, then it's your enemy's turn to attack
            harbringerAttack_chance = random.randint(1, 100)
            while bossBattle == 1:
                if currentEnemyName == "Harbringer of Deadly Light" and harbringer_phase2 == 0:  # \/ \/ \/ Harbringer of Deadly Light AI (FIRST PHASE)
                    if SAVE_dict['YourClass'] == "Rogue" and skill_selection == "1":
                        print(currentEnemyName + ": " + random.choice(harbringerS_quotes))
                        skill_selection = 0
                        time.sleep(1)
                    if harbringerAttack_chance == 100:  # Trail of Death
                        print(currentEnemyName + ": Trail of Death!")
                        time.sleep(1)
                        print("The Harbringer of Deadly Light draws a blood-red pentagram with his now dripping from blood Scythe beneath your feet.")
                        time.sleep(2)
                        print(currentEnemyName + ": DIE!")
                        time.sleep(1)
                        trailOfDeath_attack = (boss_weaponPower * 1.33) + (random.randint(2, 8) + (3 + random.randint(1,9)))  # Trail of Death damage calculation, see boss_weaponPower top of combat()
                        print("GAME: " + currentEnemyName + " deals to " + SAVE_dict['YourName'] + " " + str(trailOfDeath_attack) + " damage.")
                        time.sleep(1)
                        playerHealth -= trailOfDeath_attack - (armorPoints / 4)
                        print("Your HP: " + playerHealth + "\nEnemy HP: " + enemyHealth)
                        harbringerAttack_chance = 0
                    elif harbringerAttack_chance in range(70, 100):  # Lightbreak Slash
                        print(currentEnemyName + ": Lightbreak Slash!")
                        time.sleep(1)
                        print(currentEnemyName + ": Stay still now, mortal. You're about to witness something unreal.")
                        time.sleep(2)
                        print("The Harbringer of Deadly Light's Scythe flashes a blinding white as he cuts through your armor like silk.")
                        time.sleep(1)
                        lightbreak_armorReduced = random.randint(3, 7)  # Lightbreak Slash armor reduce calculation
                        lightbreak_attack = (boss_weaponPower / random.uniform(0.77, 1.2)) + random.randint(1,7)  # Lightbreak Slash damage calculation
                        print("GAME: " + currentEnemyName + " deals to " + SAVE_dict['YourName'] + " " + str(lightbreak_attack) + " damage and reduced his Armor Points by " + str(lightbreak_armorReduced))
                        time.sleep(1)
                        armorPoints = armorPoints - lightbreak_armorReduced
                        playerHealth -= lightbreak_attack - (armorPoints / 4)
                        print("Your HP: " + str(playerHealth) + "\nEnemyHP: " + str(enemyHealth))
                        harbringerAttack_chance = 0
                    elif harbringerAttack_chance in range(50, 70):  # Force of a Thousand Souls
                        print(currentEnemyName + ": Force of a Thousand Souls!")
                        time.sleep(1)
                        print(currentEnemyName + ": Let the souls be heard!")
                        time.sleep(2)
                        print("The Harbringer of Deadly Light swipes his Scythe from the ground to the skies and after it, a wave of thousands blue-tinted ghost hands run towards you and hit you while they try to bring you down.")
                        time.sleep(2)
                        force_thousandsouls_attack1st = ((boss_weaponPower / random.uniform(0.78, 1.14)) + (SAVE_dict['YourLevel'] * random.uniform(1.1, 1.17))) + random.randint(1,4)  # Force of a Thousand Souls 1st hit damage calculation
                        print("GAME: " + currentEnemyName + " deals to " + SAVE_dict['YourName'] + " " + str(force_thousandsouls_attack1st) + " damage. (FIRST HIT)")
                        time.sleep(1)
                        force_thousandsouls_attack2nd = ((boss_weaponPower / random.uniform(0.76, 1.12)) + (SAVE_dict['YourLevel'] * random.uniform(1.1, 1.16))) + random.randint(1,3)  # Force of a Thousand Souls 2nd hit damage calculation
                        print("GAME: " + currentEnemyName + " deals to " + SAVE_dict['YourName'] + " " + str(force_thousandsouls_attack2nd) + " damage. (SECOND HIT)")
                        time.sleep(1)
                        if random.randint(1, 100) > 80:
                            force_thousandsouls_attackFinal = ((boss_weaponPower / 1.27) + (SAVE_dict['YourLevel'] * 1.14)) + random.randint(1,2)  # Force of a Thousand Souls final damage calculation
                            print("GAME: " + currentEnemyName + " deals to " + SAVE_dict['YourName'] + " " + str(force_thousandsouls_attackFinal) + " damage. (LUCKY HIT)")
                            time.sleep(1)
                            force_thousandsouls_sum = force_thousandsouls_attack1st + force_thousandsouls_attack2nd + force_thousandsouls_attackFinal
                            print("GAME: " + currentEnemyName + " dealt to " + SAVE_dict['YourName'] + " " + str(force_thousandsouls_sum) + " damage in total.")
                            time.sleep(2)
                            playerHealth -= force_thousandsouls_sum
                            print("Your HP: " + str(playerHealth) + "\nEnemy HP: " + str(enemyHealth))
                            harbringerAttack_chance = 0
                        else:
                            force_thousandsouls_sum = force_thousandsouls_attack1st + force_thousandsouls_attack2nd
                            print("GAME: " + currentEnemyName + " dealt to " + SAVE_dict['YourName'] + " " + str(force_thousandsouls_sum) + " damage in total.")
                            time.sleep(2)
                            playerHealth -= force_thousandsouls_sum - (armorPoints / 4)
                            print("Your HP: " + str(playerHealth) + "\nEnemy HP: " + str(enemyHealth))
                            harbringerAttack_chance = 0
                    elif harbringerAttack_chance in range(36, 50):  # Control: Blood
                        print(currentEnemyName + ": Control: Blood!")
                        time.sleep(1)
                        print(currentEnemyName + ": You feel that burning sensation in your nerves?")
                        time.sleep(2)
                        controlblood_attack = ((boss_weaponPower / 1.33) + (SAVE_dict['YourLevel'] * 1.12)) + random.randint(1,5)  # Control: Blood damage calculation
                        print("GAME: " + currentEnemyName + " deals to " + SAVE_dict['YourName'] + " " + str(controlblood_attack) + " damage.")
                        time.sleep(2)
                        playerHealth -= controlblood_attack - (armorPoints / 4)
                        print("Your HP: " + str(playerHealth) + "\nEnemy HP: " + str(enemyHealth))
                        time.sleep(1)
                        harbringerAttack_chance = 0


                    elif harbringerAttack_chance in range(20, 36):  # Death Sentence
                        print(currentEnemyName + ": Death Sentence!")
                        time.sleep(1)




                    elif harbringerAttack_chance in range(1, 20):  # Scythe Swipe
                        print(currentEnemyName + ": Scythe Swipe!")
                        time.sleep(1)


                elif currentEnemyName == "Harbringer of Deadly Light" and harbringer_phase2 == 1:  # \/ \/ \/ Harbringer of Deadly Light AI (SECOND PHASE)
                    print(currentEnemyName + ": Now.. WITNESS TRUE POWER, MORTAL!")
                    time.sleep(2)
                    print("The Harbringer of Deadly Light then unleashes a huge battlecry that was audible from all over the cosmos. His Scythe's true potential has now been unlocked.")
                    time.sleep(4)
                    if harbringerAttack_chance == 100:  # Death
                        print(currentEnemyName + ": " + harbringer_phase2_deathAttack)

                if playerHealth <= 0:  # If player dies to Harbringer, do this
                    print(currentEnemyName + ": " + random.choice(harbringer_playerDied_quotes_phase1))
                    time.sleep(2)
                    enemyAlive = 0
                    print("GAME: You have died and will now be revived in a town.")
                    time.sleep(4)
                    SAVE_dict['TimesDied'] += 1
                    SAVE_dict['InTown'] = 1
                    print("\n" * 6)  # Clear screen
                    blockType_function()
                    break

                    time.sleep(1)
                    yourTurn = 1
                    break

                elif currentEnemyName == "Guardian of Wind and Thunder":  # \/ \/ \/ Guardian of Wind and Thunder AI
                    if SAVE_dict['YourClass'] == "Rogue" and skill_selection == "1":
                        print(currentEnemyName + ": Wait.. where did he go? How did he vanish?!")
                        time.sleep(1)
                        print(currentEnemyName + ": Hmmm.. I'll find you!")
                        time.sleep(3)
                        if random.randint(1, 100) > 95:
                            print(currentEnemyName + ": HA! Found you!")
                            if random.randint(1, 100) > 25:
                                time.sleep(1)
                                yourTurn = 1
                        else:
                            print(currentEnemyName + ": Damn! I lost him!")
                            enemy_isAlert = 1
                            time.sleep(1)
                            yourTurn = 1
                            break

                    time.sleep(1)
                    yourTurn = 1

            else:
                print(currentEnemyName + ": My turn!")  # Normal enemy, Rogue used Stealth
                if SAVE_dict['YourClass'] == "Rogue" and skill_selection == "1":
                    print(currentEnemyName + ": Wait.. where did he go? How did he vanish?!")
                    time.sleep(1)
                    print(currentEnemyName + ": Hmmm.. I'll find you!")
                    time.sleep(3)
                    if random.randint(1, 100) > 95:
                        print(currentEnemyName + ": HA! Found you!")
                        print(currentEnemyName + ": " + random.choice(enemy_attacks) + "!")
                        e_attack = e_weaponPower + random.randint(4, 10)
                        minusArmor = e_attack - (armorPoints / 5)
                        print(currentEnemyName + " dealt to " + SAVE_dict['YourName'] + " " + str(round(minusArmor, 3)) + " damage.")
                        playerHealth -= e_attack - (armorPoints / 5)
                        print("Your HP: " + str(round(playerHealth)) + "\nEnemy HP: " + str(round(enemyHealth)))
                        time.sleep(1)
                        yourTurn = 1
                    else:
                        print(currentEnemyName + ": Damn! I lost him!")
                        enemy_isAlert = 1
                    time.sleep(1)
                    yourTurn = 1
                    break

                else:
                    print(currentEnemyName + ": " + random.choice(enemy_attacks) + "!")  # Normal enemy
                    e_attack = e_weaponPower + random.randint(4, 10)
                    minusArmor = e_attack - (armorPoints / 5)
                    print(currentEnemyName + " dealt to " + SAVE_dict['YourName'] + " " + str(round(minusArmor, 3)) + " damage.")
                    time.sleep(1)
                    playerHealth -= e_attack - (armorPoints / 5)
                    print("Your HP: " + str(round(playerHealth, 3)) + "\nEnemy HP: " + str(round(enemyHealth, 3)))
                    time.sleep(1)

                    yourTurn = 1

                if playerHealth <= 0:  # If player dies, do this
                    print(currentEnemyName + ": " + random.choice(enemy_playerDied))
                    time.sleep(2)
                    mixer.music.fadeout(1300)
                    enemyAlive = 0
                    if SAVE_dict['YourLevel'] <= 5:
                        print("GAME: You have died and will now be revived in a town. As a death penalty, you've lost 2 Gold.")
                        SAVE_dict['YourGold'] -= 2
                        time.sleep(1)
                        print("GAME: Total Gold: " + str(SAVE_dict['YourGold']))
                    elif SAVE_dict['YourLevel'] <= 20:
                        print("GAME: You have died and will now be revived in a town. As a death penalty, you've lost 5 Gold.")
                        SAVE_dict['YourGold'] -= 5
                        time.sleep(1)
                        print("GAME: Total Gold: " + str(SAVE_dict['YourGold']))
                    time.sleep(1)
                    SAVEGAME()
                    time.sleep(1)
                    SAVE_dict['TimesDied'] += 1
                    SAVE_dict['InTown'] = 1
                    print("\n" * 5)  # Clear screen
                    blockType_function()
                    break

                break


def enemyChance():
    global currentEnemyName
    global enemyHealth
    global bossBattle
    global e_weaponPower
    global QUESTS_dict
    global ACHIEVEMENTS_dict
    global SAVE_dict

    if QUESTS_dict['active1'] == 1 or QUESTS_dict['active2'] == 1 or QUESTS_dict['active3'] == 1 or QUESTS_dict['active4'] == 1:
        currentEnemyName = random.choice(quest_enemyNames)
        print(currentEnemyName + " has appeared.\n")
        enemyHealth = (SAVE_dict['YourLevel'] * 5) + 100
        e_weaponPower = ((SAVE_dict['YourLevel'] * 4) + (SAVE_dict['YourLevel'] + random.randint(2, 6))) / 1.47
        combat()
    if SAVE_dict['YourLevel'] >= 30:
        if random.randint(1, 100) == 1:  # 2 for debugging purposes, 100 for 1 in 122% chance
            currentEnemyName = random.choice(enemyboss_name)
            if currentEnemyName == "Harbringer of Deadly Light" and ACHIEVEMENTS_dict['A11'] == 0:
                print("The skies above you darken..")
                time.sleep(2)
                print("And the ground shakes violently as a mysteriously black portal opens in front of you..")
                time.sleep(2)
                print("From the portal, emerges a ghost in flames with glowing white eyes, wearing a black robe, holding the Angel of Death's scythe, walking towards you patiently..")
                time.sleep(2)
                print("He was only rumoured as a legend..")
                time.sleep(2)
                print(currentEnemyName + ": " + random.choice(harbringer_startquotes))
                time.sleep(2)
                print("The " + currentEnemyName + " has appeared.\n")
                time.sleep(1)
                bossBattle = 1
                enemyHealth = (SAVE_dict['YourLevel'] * 28) + 350
                combat()
            # elif currentEnemyName == "Guardian of Wind and Thunder":
            # print("Rain..")
            # time.sleep(2)
            # print("Wind..")
            # time.sleep(2)
            # print("The wind picks up violently and a ghost made of wind and shiny dark-blue metallic armor appears in front of you..")
            # time.sleep(2)
            # print(currentEnemyName + ": " + random.choice(guardian_startquotes))
            # time.sleep(2)
            # print("The " + currentEnemyName + " has appeared.\n")
            # time.sleep(1)
            # bossBattle = 1
            # enemyHealth = (SAVE_dict['YourLevel'] * 27) + 330
            # combat()
        else:
            if random.randint(0, 100) > 72:
                currentEnemyName = random.choice(enemy_names)
                print(currentEnemyName + " has appeared.\n")
                enemyHealth = (SAVE_dict['YourHealth'] + (SAVE_dict['YourLevel'] * 2))
                e_weaponPower = SAVE_dict['YourWeaponPower'] + random.randint((SAVE_dict['YourLevel'] + 3),(SAVE_dict['YourLevel'] + 7))
                combat()
            else:
                print("GAME: No enemies here.\n")
                continueOrTown()
    elif SAVE_dict['YourLevel'] <= 5:
        if random.randint(0, 100) > 71:
            currentEnemyName = random.choice(enemy_names)
            print(currentEnemyName + " has appeared.\n")
            enemyHealth = (SAVE_dict['YourLevel'] * 5) + 95
            e_weaponPower = ((SAVE_dict['YourLevel'] * 3.47) + (SAVE_dict['YourLevel'] + random.randint(2, 6))) / 1.55
            combat()
        else:
            print("GAME: No enemies here.\n")
            continueOrTown()


def LoginSystem(success_login):
    cursor.execute("SELECT USERNAME FROM ACCOUNTS")
    accounts = cursor.fetchall()
    for user_row in accounts:
        db_username = user_row[0]

    LoggedIn = 0

    while LoggedIn == 0:

        USERNAME_LOGIN = input("Username: ")
        USERNAME_PASSWORD = input("Password: ")

        print("\nAuthenticating..\n")

        if USERNAME_LOGIN in db_username:
            if (cursor.execute("SELECT * FROM ACCOUNTS WHERE USERNAME = '" + USERNAME_LOGIN + "' AND PASSWORD = '" + USERNAME_PASSWORD + "'")):
                print("Correct username, correct password")
                LoggedIn = 1
                print("Passed the successful login | DEBUG - LoggedIn value: " + str(LoggedIn))
                return USERNAME_LOGIN
            else:
                print("Correct username, wrong password")
        else:
            print("Wrong username")
    else:
        print("Logged on")


# --------- START ---------

config = ConfigParser()
if not os.path.isfile("prefs.ini"):
    config.add_section('General')
    config['General']['music'] = "On"
    config['General']['sound'] = "On"
    config['General']['language'] = "ENG"
    with open("prefs.ini", 'w') as configfile:
        config.write(configfile)
else:
    config.read('prefs.ini')

if config.get('General', 'language') == "ENG":
    print("Connecting..")
elif config.get('General', 'language') == "GR":
    print("Γίνεται σύνδεση..")
db = pymysql.connect("xxx", "xxx", "xxx", "xxx")
cursor = db.cursor()
if config.get('General', 'language') == "ENG":
    print("Connected")
    print("Loading game files..")
elif config.get('General', 'language') == "GR":
    print("Πραγματοποιήθηκε σύνδεση")
    print("Φόρτωση αρχείων παιχνιδιού..")

song = "GameData/1.dat"
seastorm = "GameData/2.dat"
sword_slash = "GameData/3.wav"
bDagger_sound = "GameData/4.wav"
town_ambient = "GameData/5.dat"
entering_shop_sound = "GameData/6.wav"
harbor_ambient = "GameData/7.dat"
combat_music = "GameData/8.dat"
arena_gate_sound = "GameData/9.wav"
levelup_sound = "GameData/10.wav"
select_sound = "GameData/11.wav"

if not os.path.exists("./Profiles/"):
    os.makedirs("./Profiles/")
if not os.path.exists("./Progress/"):
    os.makedirs("./Progress/")
if not os.path.exists("./Progress/SETS/"):
    os.makedirs("./Progress/SETS/")
if not os.path.exists("./Skills/"):
    os.makedirs("./Skills/")
if not os.path.exists("./Action Logs/"):
    os.makedirs("./Action Logs/")
appdatafolder = os.getenv('APPDATA') + "/From Darkness"
if not os.path.exists(appdatafolder):
    os.makedirs(appdatafolder)

gameVer = open("version.txt", "w")
gameVer.write("Early Build 0.3.81-GitHub Release")
gameVer.close()

mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
mixer.music.load(song)

if config.get('General', 'language') == "ENG":
    print("Loaded\n")
elif config.get('General', 'language') == "GR":
    print("Η φόρτωση ολοκληρώθηκε\n")

if not os.path.isfile(appdatafolder + "/key"):
     ftp = ftplib.FTP('xxx', 'xxx', 'xxx')
     authkey = BytesIO()
     ftp.cwd("/FromDarkness/")
     ftp.retrbinary('RETR authkeys.txt', authkey.write)
     string_authkey = authkey.getvalue()
     ftp.quit()
     del authkey
     string_final = string_authkey.decode('UTF-8')
     del string_authkey
     auth_input = input("Input your activation code: ")
     if auth_input in string_final:
         del string_final
         print("--- You have successfully activated From Darkness: Twin Worlds. Thank you for your purchase, enjoy! ---")
         time.sleep(1.5)
         print("(The game will start shortly..)")
         licensekey_file = open(appdatafolder + "/key", "w")
         licensekey_file.write(auth_input)
         licensekey_file.close()
         del auth_input
         del appdatafolder
         time.sleep(5)
     else:
         while not auth_input in string_final:
             auth_input = input("Incorrect activation code. Try again: ")
         else:
             del string_final
             print("--- You have successfully activated From Darkness: Twin Worlds. Thank you for your purchase, enjoy! ---")
             time.sleep(1.5)
             print("(The game will start shortly..)")
             licensekey_file = open(appdatafolder + "/key", "w")
             licensekey_file.write(auth_input)
             licensekey_file.close()
             del auth_input
             del appdatafolder
             time.sleep(5)
else:
    del appdatafolder

time.sleep(0.5)
os.system('cls')
time.sleep(1.3)

SideThreads()

newgame_answer = ""
while not newgame_answer == "1" or newgame_answer == "2":
    if config.get('General', 'music') == "On":
        mixer.music.play(-1)
    else:
        mixer.music.stop()
    print("----- From Darkness: Twin Worlds -----")
    if config.get('General', 'language') == "ENG":
        newgame_answer = input("\n1. New Game\n2. Load Game\n3. Settings\n4. Exit\nInput your selection: ")
    elif config.get('General', 'language') == "GR":
        newgame_answer = input("\n1. Καινούργιο παιχνίδι\n2. Φόρτωση παιχνιδιού\n3. Ρυθμίσεις\n4. Έξοδος\nΔώστε την επιλογή σας: ")
    if newgame_answer == "2":  # Registration
        startingPoint()
    elif newgame_answer == "1":  # Login
        USER_LOGGEDIN = ""
        USER_LOGGEDIN = LoginSystem(USER_LOGGEDIN)

        print("Connecting to FTP server..")
        ftp = ftplib.FTP('xxx', 'xxx', 'xxx')
        print("Connected")
        print("Downloading save data..")  # Download
        ftp.cwd("/PROFILES/")
        filetoreceive = open(USER_LOGGEDIN + ".dat", 'wb')
        ftp.retrbinary('RETR ' + USER_LOGGEDIN + ".dat", filetoreceive.write)
        filetoreceive.close()

        ##            if os.path.isfile("Profiles/" + USER_LOGGEDIN + ".dat"):
        ##                os.remove("Profiles/" + USER_LOGGEDIN + ".dat")
        ##                os.rename(USER_LOGGEDIN + ".dat", "Profiles/" + USER_LOGGEDIN + ".dat")
        ##            else:
        ##                os.rename(USER_LOGGEDIN + ".dat", "Profiles/" + USER_LOGGEDIN + ".dat")

        filetoreceive2 = open(USER_LOGGEDIN + "_Skills.set", 'wb')
        ftp.retrbinary('RETR ' + USER_LOGGEDIN + "_Skills.set", filetoreceive2.write)
        filetoreceive2.close()

        ##            if os.path.isfile("Skills/" + USER_LOGGEDIN + "_Skills.set"):
        ##                os.remove("Profiles/" + USER_LOGGEDIN + ".dat")
        ##                os.rename(USER_LOGGEDIN + ".dat", "Profiles/" + USER_LOGGEDIN + ".dat")
        ##            else:
        ##                os.rename(USER_LOGGEDIN + ".dat", "Profiles/" + USER_LOGGEDIN + ".dat")

        filetoreceive3 = open(USER_LOGGEDIN + "_Progress.dat", 'wb')
        ftp.retrbinary('RETR ' + USER_LOGGEDIN + "_Progress.dat", filetoreceive3.write)
        filetoreceive3.close()

        filetoreceive4 = open(USER_LOGGEDIN + "_Set.set", 'wb')
        ftp.retrbinary('RETR ' + USER_LOGGEDIN + "_Set.set", filetoreceive4.write)
        filetoreceive4.close()

        filetoreceive5 = open(USER_LOGGEDIN + ".inv", 'wb')
        ftp.retrbinary('RETR ' + USER_LOGGEDIN + ".inv", filetoreceive5.write)
        filetoreceive5.close()

        print("Downloaded")
        ftp.quit()
        print("Disconnected from the FTP server")
        time.sleep(1)
        mixer.music.fadeout(1400)
        LOADGAME(USER_LOGGEDIN)
    elif newgame_answer == "3": # Settings
        config_input = ""
        while not config_input == "4":
            if config.get('General', 'language') == "ENG":
                print("\nMusic: " + str(config.get('General', 'music')))
                print("Sound: " + str(config.get('General', 'sound')))
                print("Language: " + config.get('General', 'language'))
                config_input = input("\n1. Change music setting to on/off\n2. Change sound setting to on/off\n3. Change language to English/Greek\n4. Save settings and go back\nInput your selection: ")
                if config_input == "1":
                    if config.get('General', 'music') == "On": #If music setting is set to ON
                        config.set('General', 'music', 'Off')
                        print("Changed music setting")
                    elif config.get('General', 'music') == "Off": #If music setting is set to OFF
                        config.set('General', 'music', 'On')
                        print("Changed music setting")
                elif config_input == "2":
                    if config.get('General', 'sound') == "On": #If sound setting is set to ON
                        config.set('General', 'sound', 'Off')
                        print("Changed sound setting")
                    elif config.get('General', 'sound') == "Off": #If sound setting is set to OFF
                        config.set('General', 'sound', 'On')
                        print("Changed sound setting")
                elif config_input == "3":
                    if config.get('General', 'language') == "ENG":
                        config.set('General', 'language', 'GR')
                        print("Changed the language to Greek")
                    elif config.get('General', 'language') == "GR":
                        config.set('General', 'language', 'ENG')
                        print("Changed the language to English")
                elif config_input == "4":
                    with open('prefs.ini', 'w') as configfile:
                        config.write(configfile)
                    time.sleep(0.33)
                    os.system('cls')
                else:
                    pass
            elif config.get('General', 'language') == "GR":
                print("\nΜουσική: " + str(config.get('General', 'music')))
                print("Ήχος: " + str(config.get('General', 'sound')))
                print("Γλώσσα: " + config.get('General', 'language'))
                config_input = input("\n1. Αλλαγή ρύθμισης της μουσικής σε οn/οff\n2. Αλλαγή ρύθμισης του ήχου σε on/off\n3. Αλλαγή ρύθμισης της γλώσσας σε Αγγλικά/Ελληνικά\n4. Αποθήκευση αλλαγών και πηγαίντε πίσω\nΔώστε την επιλογή σας: ")
                if config_input == "1":
                    if config.get('General', 'music') == "On": #If music setting is set to ON
                        config.set('General', 'music', 'Off')
                        print("Πραγματοποιήθηκε η ρύθμιση αλλαγής μουσικής")
                    elif config.get('General', 'music') == "Off": #If music setting is set to OFF
                        config.set('General', 'music', 'On')
                        print("Πραγματοποιήθηκε η ρύθμιση αλλαγής μουσικής")
                elif config_input == "2":
                    if config.get('General', 'sound') == "On": #If sound setting is set to ON
                        config.set('General', 'sound', 'Off')
                        print("Πραγματοποιήθηκε η ρύθμιση αλλαγής ήχου")
                    elif config.get('General', 'sound') == "Off": #If sound setting is set to OFF
                        config.set('General', 'sound', 'On')
                        print("Πραγματοποιήθηκε η ρύθμιση αλλαγής ήχου")
                elif config_input == "3":
                    if config.get('General', 'language') == "ENG":
                        config.set('General', 'language', 'GR')
                        print("Changed the language to Greek")
                    elif config.get('General', 'language') == "GR":
                        config.set('General', 'language', 'ENG')
                        print("Changed the language to English")
                elif config_input == "4":
                    with open('prefs.ini', 'w') as configfile:
                        config.write(configfile)
                    time.sleep(0.33)
                    os.system('cls')
                else:
                    pass
    elif newgame_answer == "4": # Exit
        quit()